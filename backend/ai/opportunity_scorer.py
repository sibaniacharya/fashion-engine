class OpportunityScorer:
    def __init__(self, themes: list[dict], barriers: dict, segments: dict):
        self.themes = themes
        self.barriers = barriers
        self.segments = segments

    def generate_opportunities(self) -> list[dict]:
        opportunities = []

        # 1. From Barriers (High Purchase Impact)
        top_barriers = self.barriers if isinstance(self.barriers, dict) else {}
        for barrier_text, data in top_barriers.items():
            freq = data.get("total_mentions", 0)
            if freq == 0:
                continue

            evidence = data.get("quotes_detail", [])
            unique_records = data.get("unique_records", 0)
            gp = data.get("google_play_count", 0)
            yt = data.get("youtube_count", 0)
            stage = data.get("journey_stage", "Evaluation")

            outcome = "Abandonment" if freq > 3 else "Postponement"
            problem_stmt = f"Users experiencing strong product interest may postpone or abandon their purchase when they encounter '{barrier_text}' during the {stage} stage."

            opp = self._score_opportunity(
                base_text=barrier_text,
                problem_stmt=problem_stmt,
                frequency=freq,
                is_barrier=True,
                evidence=evidence,
                unique_records=unique_records,
                gp_count=gp,
                yt_count=yt,
                stage=stage,
            )
            if opp:
                opportunities.append(opp)

        # 2. From Themes (Discovery / UX Impact)
        for theme in self.themes:
            if theme.get("theme_name") == "INSUFFICIENT_EVIDENCE":
                continue

            freq = theme.get("unique_record_count", 0)
            if freq > 1:
                # Deduplicate loosely based on name
                already_exists = any(
                    o["problem"] == theme["theme_name"] for o in opportunities
                )
                if not already_exists:
                    problem_stmt = f"Users evaluating the platform encounter friction from '{theme['theme_name']}' during the Discovery stage, which may disrupt their shopping journey."

                    evidence_raw = theme.get("representative_quotes", [])
                    evidence = []
                    for q in evidence_raw:
                        if isinstance(q, dict):
                            evidence.append(q)
                        else:
                            evidence.append(
                                {
                                    "quote": q,
                                    "source": "Unknown",
                                    "trace_id": "Unknown",
                                    "date": "Unknown",
                                }
                            )

                    opp = self._score_opportunity(
                        base_text=theme["theme_name"],
                        problem_stmt=problem_stmt,
                        frequency=freq,
                        is_barrier=False,
                        evidence=evidence,
                        unique_records=freq,
                        gp_count=theme.get("google_play_count", 0),
                        yt_count=theme.get("youtube_count", 0),
                        stage="Discovery",
                    )
                    if opp:
                        opportunities.append(opp)

        # Sort by opportunity score descending
        opportunities.sort(key=lambda x: x["opportunity_score"], reverse=True)
        return opportunities

    def _score_opportunity(
        self,
        base_text: str,
        problem_stmt: str,
        frequency: int,
        is_barrier: bool,
        evidence: list,
        unique_records: int,
        gp_count: int,
        yt_count: int,
        stage: str,
    ) -> dict:
        # Differentiated Scoring

        # 1. Frequency (1-5)
        if frequency > 20:
            freq_score = 5
        elif frequency > 10:
            freq_score = 4
        elif frequency > 5:
            freq_score = 3
        elif frequency > 2:
            freq_score = 2
        else:
            freq_score = 1

        # Check evidence for actual purchase/wishlist intent
        intent_keywords = [
            "wishlist",
            "cart",
            "buy",
            "purchas",
            "order",
            "save",
            "later",
            "compar",
            "decid",
            "look",
            "want",
        ]
        intent_matches = 0
        for e in evidence:
            text = (e.get("quote", "") if isinstance(e, dict) else str(e)).lower()
            if any(kw in text for kw in intent_keywords):
                intent_matches += 1

        # Classify Post-Purchase correctly
        complaint_themes = [
            "Return and Refund Friction",
            "App Performance / UX Issues",
            "Delivery / Shipping Friction",
            "Returns / Exchange Friction",
            "INSUFFICIENT_EVIDENCE",
        ]
        if base_text in complaint_themes:
            stage = "POST_PURCHASE"

        # 2. Wishlist Relevance (1-5)
        wishlist_rel = 1
        if intent_matches > 0:
            wishlist_rel = min(5, 2 + intent_matches)

        if stage in ["EVALUATION", "COMPARISON", "POSTPONEMENT", "ABANDONMENT"]:
            wishlist_rel = max(wishlist_rel, 3)
        elif stage == "WISHLIST":
            wishlist_rel = max(wishlist_rel, 4)

        if stage == "POST_PURCHASE" and intent_matches == 0:
            wishlist_rel = 1

        # 3. Purchase Impact (1-5)
        purch_impact = 5 if is_barrier else 3

        # 4. User Pain (1-5)
        user_pain = 5 if is_barrier else 3

        # 5. Cross Source Consistency (1-5)
        sources_with_issue = sum(1 for x in [gp_count, yt_count] if x > 0)
        cross_source = 5 if sources_with_issue > 1 else 2

        # 6. Evidence Confidence (1-5)
        if unique_records >= 10:
            evidence_conf = 5
        elif unique_records >= 5:
            evidence_conf = 4
        elif unique_records >= 3:
            evidence_conf = 3
        elif unique_records == 2:
            evidence_conf = 2
        else:
            evidence_conf = 1

        # Weighted Final Score
        total_weight = 10
        weighted_sum = (
            (freq_score * 1)
            + (wishlist_rel * 2)
            + (purch_impact * 3)
            + (user_pain * 2)
            + (cross_source * 1)
            + (evidence_conf * 1)
        )
        final_score = round(weighted_sum / total_weight, 1)

        # Enforce max score limits for low evidence signals
        if unique_records == 1:
            final_score = min(final_score, 1.9)
        elif unique_records < 5:
            final_score = min(final_score, 3.5)

        # Classification based on thresholds
        if unique_records >= 10 and evidence_conf >= 4 and wishlist_rel >= 3:
            classification = "HIGH_CONFIDENCE_OPPORTUNITY"
        elif unique_records >= 5:
            classification = "OPPORTUNITY"
        elif unique_records >= 2:
            classification = "EMERGING_SIGNAL"
        else:
            classification = "SIGNAL"

        opp_name = (
            f"Resolve: {base_text[:30]}"
            if is_barrier
            and classification in ["OPPORTUNITY", "HIGH_CONFIDENCE_OPPORTUNITY"]
            else f"Signal: {base_text[:30]}"
        )

        # Format structural trace evidence properly
        formatted_evidence = []
        for e in evidence:
            if isinstance(e, dict):
                formatted_evidence.append(e)
            else:
                formatted_evidence.append(
                    {
                        "quote": str(e),
                        "source": "Unknown",
                        "trace_id": "Unknown",
                        "date": "Unknown",
                    }
                )

        # Find affected segments
        affected = []
        for seg in self.segments.get("segments", []):
            if base_text in seg.get("purchase_barriers", []) or base_text in seg.get(
                "dominant_themes", []
            ):
                affected.append(seg.get("segment_name"))
        affected_str = ", ".join(affected) if affected else "Broadly applicable"

        return {
            "opportunity_name": opp_name,
            "problem": base_text,
            "structured_statement": problem_stmt,
            "affected_segment": affected_str,
            "journey_stage": stage,
            "classification": classification,
            "wishlist_purchase_relevance": wishlist_rel,
            "unique_evidence_records": unique_records,
            "google_play_count": gp_count,
            "youtube_count": yt_count,
            "source_coverage": sources_with_issue,
            "scores": {
                "frequency": freq_score,
                "wishlist_relevance": wishlist_rel,
                "purchase_impact": purch_impact,
                "user_pain": user_pain,
                "cross_source_consistency": cross_source,
                "evidence_confidence": evidence_conf,
            },
            "opportunity_score": final_score,
            "supporting_evidence": formatted_evidence,
        }
