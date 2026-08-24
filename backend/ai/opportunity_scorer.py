import uuid

class OpportunityScorer:
    def __init__(self, themes: list[dict], barriers: dict, wishlist: dict, research: dict):
        self.themes = themes
        self.barriers = barriers
        self.wishlist = wishlist
        self.research = research

    def generate_opportunities(self) -> list[dict]:
        opportunities = []
        
        # We derive opportunities from the Top Barriers identified in Phase 5
        top_barriers = self.barriers.get("top_barriers", {})
        
        for barrier_text, freq in top_barriers.items():
            # Basic dummy extraction of evidence for barriers since they don't natively carry the text array here
            # In a real run, we'd map it back to phase3_signals.json
            evidence = [f"User reported: {barrier_text}"]
            opp = self._score_opportunity(barrier_text, freq, is_barrier=True, evidence=evidence)
            if opp:
                opportunities.append(opp)
                
        # Also derive from high-frequency Themes that aren't explicit barriers (e.g., UX/UI themes)
        for theme in self.themes:
            # If the theme has a high frequency but wasn't caught as a pure "barrier"
            if theme.get("frequency", 0) > 2:
                # Basic dedup check
                already_exists = any(o["problem"] == theme["theme_name"] for o in opportunities)
                if not already_exists:
                    opp = self._score_opportunity(theme["theme_name"], theme["frequency"], is_barrier=False, evidence=theme.get("supporting_evidence", []))
                    if opp:
                        opportunities.append(opp)
                        
        # Sort by opportunity score descending
        opportunities.sort(key=lambda x: x["opportunity_score"], reverse=True)
        return opportunities

    def _score_opportunity(self, base_text: str, frequency: int, is_barrier: bool, evidence: list[str]) -> dict:
        # Heuristic Scoring (1-5)
        
        # Frequency Score: Logarithmic scaling for MVP (if freq > 10 it's a 5, else mapped)
        freq_score = min(5, max(1, frequency))
        
        # Wishlist Relevance: If barrier correlates with wishlist abandonment
        wishlist_rel = 5 if is_barrier and self.wishlist.get("total_wishlist_mentions", 0) > 0 else 3
        
        # Purchase Impact: Barriers directly block purchases
        purch_impact = 5 if is_barrier else 3
        
        # User Pain: Explicit pain points score highest
        user_pain = 5 if is_barrier else 2
        
        # Cross Source
        sources = self.barriers.get("by_source", {}).keys()
        cross_source = 5 if len(sources) > 1 else 3
        
        # Evidence Confidence
        evidence_conf = min(5, len(evidence) + 1 if evidence else 2)
        
        # Calculate Weighted Score
        # Heavily weight wishlist_rel (x2) and purch_impact (x2)
        total_weight = 1 + 2 + 2 + 1 + 1 + 1 # 8
        weighted_sum = (
            (freq_score * 1) +
            (wishlist_rel * 2) +
            (purch_impact * 2) +
            (user_pain * 1) +
            (cross_source * 1) +
            (evidence_conf * 1)
        )
        final_score = round(weighted_sum / total_weight, 1)
        
        # Opportunity formulation
        opp_name = f"Resolve: {base_text[:30]}..." if is_barrier else f"Enhance: {base_text}"
        
        return {
            "opportunity_name": opp_name,
            "problem": base_text,
            "affected_segment": "General Shopper", # Can be dynamically mapped if dataset was larger
            "journey_stage": "Evaluation / Purchase Postponement" if is_barrier else "Discovery",
            "scores": {
                "frequency": freq_score,
                "wishlist_relevance": wishlist_rel,
                "purchase_impact": purch_impact,
                "user_pain": user_pain,
                "cross_source_consistency": cross_source,
                "evidence_confidence": evidence_conf
            },
            "opportunity_score": final_score,
            "supporting_evidence": evidence,
            "key_uncertainty": "Requires deeper segment breakdown at scale"
        }
