import json
from collections import defaultdict

class BehaviorAnalyzer:
    def __init__(self, signals: list[dict]):
        self.signals = signals

    def _extract_base_metrics(self, record: dict) -> dict:
        ext = record.get("extracted_signals", {})
        return {
            "source": record.get("source", "UNKNOWN"),
            "segment": ext.get("user_segment") or "Unknown Segment",
            "theme": ext.get("theme_candidate") or "Unclassified"
        }

    def analyze_wishlist_behavior(self) -> dict:
        analysis = {
            "total_wishlist_mentions": 0,
            "bookmarking_vs_intent": {"bookmarking": 0, "purchase_intent": 0},
            "postponement_reasons": defaultdict(int),
            "by_source": defaultdict(lambda: {"total": 0, "intents": []}),
            "by_segment": defaultdict(lambda: {"total": 0, "intents": []}),
            "by_theme": defaultdict(lambda: {"total": 0, "intents": []})
        }
        
        for r in self.signals:
            ext = r.get("extracted_signals", {})
            wish_intent = ext.get("wishlist_intent")
            if wish_intent:
                analysis["total_wishlist_mentions"] += 1
                base = self._extract_base_metrics(r)
                
                # Classify simple bookmarking vs intent based on keyword heuristics
                lower_intent = wish_intent.lower()
                if "buy later" in lower_intent or "purchase" in lower_intent or "save for" in lower_intent:
                    analysis["bookmarking_vs_intent"]["purchase_intent"] += 1
                else:
                    analysis["bookmarking_vs_intent"]["bookmarking"] += 1
                    
                # Postponement
                if ext.get("purchase_stage") == "postponement" and ext.get("pain_point"):
                    analysis["postponement_reasons"][ext.get("pain_point")] += 1
                
                # Distribute
                analysis["by_source"][base["source"]]["total"] += 1
                analysis["by_source"][base["source"]]["intents"].append(wish_intent)
                
                analysis["by_segment"][base["segment"]]["total"] += 1
                analysis["by_theme"][base["theme"]]["total"] += 1
                
        return analysis

    def analyze_purchase_barriers(self) -> dict:
        analysis = {
            "total_barriers_identified": 0,
            "top_barriers": defaultdict(int),
            "top_uncertainties": defaultdict(int),
            "by_source": defaultdict(lambda: {"total": 0, "barriers": []}),
            "by_segment": defaultdict(lambda: {"total": 0, "barriers": []}),
            "by_theme": defaultdict(lambda: {"total": 0, "barriers": []}),
            "correlation_with_comparison": 0
        }
        
        for r in self.signals:
            ext = r.get("extracted_signals", {})
            barrier = ext.get("purchase_barrier")
            pain = ext.get("pain_point")
            uncertainty = ext.get("uncertainty")
            
            active_barrier = barrier or pain
            if active_barrier:
                analysis["total_barriers_identified"] += 1
                analysis["top_barriers"][active_barrier] += 1
                
                if uncertainty:
                    analysis["top_uncertainties"][uncertainty] += 1
                    
                if ext.get("comparison_behavior"):
                    analysis["correlation_with_comparison"] += 1
                    
                base = self._extract_base_metrics(r)
                analysis["by_source"][base["source"]]["total"] += 1
                analysis["by_source"][base["source"]]["barriers"].append(active_barrier)
                
                analysis["by_segment"][base["segment"]]["total"] += 1
                analysis["by_theme"][base["theme"]]["total"] += 1
                
        return analysis

    def analyze_external_research(self) -> dict:
        analysis = {
            "total_external_research_events": 0,
            "information_sought": defaultdict(int),
            "alternatives_considered": [],
            "by_source": defaultdict(int),
            "by_segment": defaultdict(int),
            "by_theme": defaultdict(int)
        }
        
        for r in self.signals:
            ext = r.get("extracted_signals", {})
            research = ext.get("external_research_behavior")
            info = ext.get("information_sought")
            comp = ext.get("comparison_behavior")
            
            if research or info or comp:
                analysis["total_external_research_events"] += 1
                
                if info:
                    analysis["information_sought"][info] += 1
                if comp:
                    analysis["alternatives_considered"].append(comp)
                    
                base = self._extract_base_metrics(r)
                analysis["by_source"][base["source"]] += 1
                analysis["by_segment"][base["segment"]] += 1
                analysis["by_theme"][base["theme"]] += 1
                
        return analysis
