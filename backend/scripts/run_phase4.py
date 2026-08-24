import os
import sys
import json
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai.cluster import ThemeClusterer
from ai.theme_generator import ThemeSynthesizer

def run_phase4():
    # Load Phase 3 signals
    input_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'analyzed', 'phase3_signals.json'))
    
    if not os.path.exists(input_path):
        print(f"Error: Could not find Phase 3 signals at {input_path}")
        return
        
    with open(input_path, 'r', encoding='utf-8') as f:
        records = json.load(f)
        
    if not records:
        print("Error: Phase 3 signals file is empty.")
        return

    print(f"Loaded {len(records)} records for Theme Discovery.")
    
    # 1. Cluster Records
    clusterer = ThemeClusterer()
    clusters = clusterer.cluster_records(records)
    print(f"Generated {len(clusters)} clusters.")
    
    # 2. Synthesize Themes
    synthesizer = ThemeSynthesizer()
    final_themes = []
    
    for i, cluster in enumerate(clusters):
        print(f"Synthesizing Theme {i+1}/{len(clusters)} (Cluster Size: {len(cluster)})")
        try:
            theme = synthesizer.synthesize_cluster(cluster)
            final_themes.append(theme)
            time.sleep(15) # Respect rate limits (15s for 5 RPM limit)
        except Exception as e:
            print(f"Failed to synthesize theme for cluster {i+1}: {e}")
            
    # Sort themes by frequency descending
    final_themes.sort(key=lambda x: x["frequency"], reverse=True)
            
    # 3. Export
    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'analyzed', 'themes.json'))
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final_themes, f, indent=2, ensure_ascii=False)
        
    print(f"\n--- Phase 4 Complete ---")
    print(f"Discovered {len(final_themes)} themes.")
    print(f"Saved to: {output_path}")

if __name__ == "__main__":
    run_phase4()
