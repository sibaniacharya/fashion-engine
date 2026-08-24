import os
import sys
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai.opportunity_scorer import OpportunityScorer

def load_json(filename: str):
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'analyzed', filename))
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def run_phase6():
    print("Loading Phase 4 and Phase 5 artifacts...")
    themes = load_json("themes.json")
    barriers = load_json("purchase_barriers.json")
    wishlist = load_json("wishlist_behavior.json")
    research = load_json("external_information_seeking.json")
    
    if not isinstance(themes, list):
        themes = []
        
    scorer = OpportunityScorer(themes, barriers, wishlist, research)
    opportunities = scorer.generate_opportunities()
    
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'analyzed'))
    os.makedirs(output_dir, exist_ok=True)
    
    export_path = os.path.join(output_dir, "opportunities.json")
    with open(export_path, "w", encoding="utf-8") as f:
        json.dump(opportunities, f, indent=2, ensure_ascii=False)
        
    print(f"\n--- Phase 6 Complete ---")
    print(f"Generated {len(opportunities)} Opportunity Areas.")
    print(f"Scores dynamically weighted towards wishlist relevance & purchase impact.")
    print(f"Saved to: {export_path}")

if __name__ == "__main__":
    run_phase6()
