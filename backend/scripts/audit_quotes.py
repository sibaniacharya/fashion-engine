import os
import json
import random


def load_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def audit_themes(base_dir):
    records = load_json(os.path.join(base_dir, "output", "analysis_records.json"))
    themes = load_json(os.path.join(base_dir, "output", "themes.json"))

    if not themes or not records:
        return

    for t in themes:
        theme_name = t.get("theme_name", "").lower()
        # Find records that match this theme exactly
        matching = [
            r
            for r in records
            if r.get("theme", "").lower() == theme_name
            and r.get("analysis_status") in ["ANALYZED", "ANALYZED_FALLBACK"]
        ]

        # Filter matching records to those that actually mention related keywords
        valid_quotes = []
        theme_keywords = theme_name.split()

        # Add some domain synonyms to avoid overly strict filtering
        if "return" in theme_name:
            theme_keywords.extend(["refund", "exchange", "pickup", "delivery boy"])
        if "size" in theme_name:
            theme_keywords.extend(["fit", "small", "large", "baggy", "tight"])
        if "price" in theme_name:
            theme_keywords.extend(["expensive", "cost", "money", "waste", "cheap"])
        if "delivery" in theme_name:
            theme_keywords.extend(["shipping", "late", "courier", "never came"])

        for r in matching:
            text = r.get("text", "").lower()
            if any(kw in text for kw in theme_keywords):
                valid_quotes.append(r.get("text"))

        # If we couldn't find strictly keyword matching ones, fall back to longer reviews which are usually more descriptive
        if not valid_quotes:
            valid_quotes = [
                r.get("text") for r in matching if len(r.get("text", "")) > 20
            ]

        if not valid_quotes:
            valid_quotes = [r.get("text") for r in matching]

        t["representative_quotes"] = valid_quotes[:3]

    save_json(themes, os.path.join(base_dir, "output", "themes.json"))


def audit_barriers(base_dir):
    records = load_json(os.path.join(base_dir, "output", "analysis_records.json"))
    barriers = load_json(os.path.join(base_dir, "output", "barriers.json"))

    if not barriers or not records:
        return

    for barrier_name, data in barriers.items():
        b_lower = barrier_name.lower()

        # Get matching records (via our map or direct string match)
        # Note: the barriers logic maps raw outputs using a semantic map.
        # But we can just search all records where purchase_barrier maps to this.
        from ai.analyzer import map_barrier

        matching = [
            r
            for r in records
            if map_barrier(r.get("purchase_barrier", "")).lower() == b_lower
        ]

        valid_quotes = []
        kw_list = b_lower.split()
        if "support" in b_lower:
            kw_list.extend(["customer care", "help", "contact", "reply"])
        if "return" in b_lower:
            kw_list.extend(["refund", "exchange"])

        for r in matching:
            text = r.get("text", "").lower()
            if any(kw in text for kw in kw_list):
                valid_quotes.append(
                    {
                        "quote": r.get("text"),
                        "source": r.get("source"),
                        "trace_id": r.get("record_id", r.get("trace_id", "Unknown")),
                        "date": r.get("date", "Unknown"),
                    }
                )

        if not valid_quotes:
            valid_quotes = [
                {
                    "quote": r.get("text"),
                    "source": r.get("source"),
                    "trace_id": r.get("record_id", "Unknown"),
                    "date": r.get("date", "Unknown"),
                }
                for r in matching
                if len(r.get("text", "")) > 20
            ]

        if not valid_quotes:
            valid_quotes = [
                {
                    "quote": r.get("text"),
                    "source": r.get("source"),
                    "trace_id": r.get("record_id", "Unknown"),
                    "date": r.get("date", "Unknown"),
                }
                for r in matching
            ]

        data["quotes_detail"] = valid_quotes[:3]
        data["representative_quotes"] = [q["quote"] for q in valid_quotes[:3]]

    save_json(barriers, os.path.join(base_dir, "output", "barriers.json"))


if __name__ == "__main__":
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    audit_themes(base)
    audit_barriers(base)
    print("Audited themes and barriers.")
