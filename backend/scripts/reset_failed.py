import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), "..", "discovery_engine.db")
conn = sqlite3.connect(db_path)
conn.execute(
    "DELETE FROM extracted_signal WHERE json_extract(signals, '$.status') = 'FAILED' OR json_extract(signals, '$.status') = 'ANALYZED_FALLBACK' OR json_extract(signals, '$.model_used') = 'FALLBACK'"
)
conn.commit()
print(f"Deleted {conn.total_changes} failed records.")
conn.close()
