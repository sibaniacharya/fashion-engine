import os
import json
from fastapi import HTTPException
from functools import lru_cache

# We use lru_cache for MVP so it doesn't do File I/O on every single API hit, 
# but in production this would query the DB.

@lru_cache(maxsize=10)
def get_analyzed_data(filename: str):
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'analyzed', filename))
    if not os.path.exists(path):
        # Fallback to normalized data dir for Data Quality report
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'normalized', filename))
        if not os.path.exists(path):
            raise HTTPException(status_code=404, detail=f"Data file {filename} not found.")
            
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail=f"Error decoding {filename}.")
