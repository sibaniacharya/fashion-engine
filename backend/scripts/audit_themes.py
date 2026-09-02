import os
import json
import random


def run_audit():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    themes_path = os.path.join(base_dir, "output", "themes.json")
    records_path = os.path.join(base_dir, "output", "analysis_records.json")

    if not os.path.exists(themes_path) or not os.path.exists(records_path):
        print("Required files not found.")
        return

    with open(themes_path, "r", encoding="utf-8") as f:
        themes = json.load(f)

    with open(records_path, "r", encoding="utf-8") as f:
        records = json.load(f)

    # Group records by theme
    records_by_theme = {}
    for r in records:
        if r.get("analysis_status") == "ANALYZED":
            t = r.get("theme")
            if t and t != "UNKNOWN":
                if t not in records_by_theme:
                    records_by_theme[t] = []
                records_by_theme[t].append(r)

    keywords_by_theme = {
        "Return and Refund Friction": [
            "return",
            "refund",
            "replace",
            "exchange",
            "money",
            "fake",
            "defective",
            "scam",
            "customer service",
        ],
        "App Performance / UX Issues": [
            "app",
            "slow",
            "crash",
            "filter",
            "load",
            "bug",
            "glitch",
            "update",
            "working",
        ],
        "Delivery / Shipping Friction": [
            "deliver",
            "delay",
            "missing",
            "cancel",
            "order",
            "receive",
            "courier",
            "pack",
        ],
        "Fit / Size Uncertainty": [
            "size",
            "fit",
            "small",
            "large",
            "dimension",
            "baggy",
            "loose",
            "tight",
            "measure",
        ],
        "Seeking Authentic Product Reviews": [
            "review",
            "fake",
            "real",
            "authentic",
            "trust",
            "honest",
        ],
    }

    for theme in themes:
        theme_name = theme.get("theme_name")
        valid_records = records_by_theme.get(theme_name, [])

        # Filter valid records based on keywords and length to avoid generic quotes
        kws = keywords_by_theme.get(theme_name, [])
        strong_candidates = []
        for r in valid_records:
            text = r.get("text", "")
            if len(text.split()) > 4:  # Not too short
                if not kws or any(kw in text.lower() for kw in kws):
                    strong_candidates.append(r)

        # Sort by length descending, pick top ones
        strong_candidates.sort(key=lambda x: len(x.get("text", "")), reverse=True)

        new_quotes = []
        for c in strong_candidates[:5]:
            new_quotes.append(
                {
                    "quote": c.get("text"),
                    "source": c.get("source"),
                    "trace_id": c.get("internal_id"),
                    "date": c.get("date"),
                }
            )

        if new_quotes:
            theme["representative_quotes"] = new_quotes
            theme["supporting_evidence"] = new_quotes

    with open(themes_path, "w", encoding="utf-8") as f:
        json.dump(themes, f, indent=2, ensure_ascii=False)

    print("Theme evidence audit complete.")


if __name__ == "__main__":
    run_audit()
