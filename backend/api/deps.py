import os
import json
from fastapi import HTTPException
from functools import lru_cache

# We read the JSON on every request in MVP to ensure data stays fresh.
# In production this would query the DB.


def get_analyzed_data(filename: str):
    # Check output directory first
    path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "output", filename)
    )
    if not os.path.exists(path):
        # Fallback to analyzed
        path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__), "..", "..", "data", "analyzed", filename
            )
        )
        if not os.path.exists(path):
            # Fallback to normalized
            path = os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    "..",
                    "..",
                    "data",
                    "normalized",
                    filename,
                )
            )
            if not os.path.exists(path):
                raise HTTPException(
                    status_code=404, detail=f"Data file {filename} not found."
                )

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail=f"Error decoding {filename}.")
