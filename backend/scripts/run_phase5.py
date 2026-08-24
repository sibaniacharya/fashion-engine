import os
import sys
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai.analyzer import BehaviorAnalyzer

def run_phase5():
    input_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'analyzed', 'phase3_signals.json'))
    
    if not os.path.exists(input_path):
        print(f"Error: Could not find Phase 3 signals at {input_path}")
        return
        
    with open(input_path, 'r', encoding='utf-8') as f:
        records = json.load(f)
        
    if not records:
        print("Error: Phase 3 signals file is empty.")
        return

    print(f"Loaded {len(records)} records for Phase 5 Analysis.")
    
    analyzer = BehaviorAnalyzer(records)
    
    wishlist_behavior = analyzer.analyze_wishlist_behavior()
    purchase_barriers = analyzer.analyze_purchase_barriers()
    external_research = analyzer.analyze_external_research()
    
    # Export
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'analyzed'))
    os.makedirs(output_dir, exist_ok=True)
    
    paths = {
        "wishlist_behavior.json": wishlist_behavior,
        "purchase_barriers.json": purchase_barriers,
        "external_information_seeking.json": external_research
    }
    
    for filename, data in paths.items():
        export_path = os.path.join(output_dir, filename)
        with open(export_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Saved {filename}")

    print("\n--- Phase 5 Complete ---")

if __name__ == "__main__":
    run_phase5()
