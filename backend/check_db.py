import sqlite3

conn = sqlite3.connect("discovery_engine.db")
c = conn.cursor()
print(f"Extracted: {c.execute('SELECT COUNT(1) FROM extracted_signal').fetchone()[0]}")
print(
    f"Normalized: {c.execute('SELECT COUNT(1) FROM normalized_feedback WHERE is_valid=1').fetchone()[0]}"
)
