from abc import ABC, abstractmethod
from typing import List, Dict, Any

class IngestionAdapter(ABC):
    """Base interface for all ingestion adapters."""

    @abstractmethod
    def fetch_data(self) -> List[Dict[str, Any]]:
        """
        Fetches data from the source and returns it as a list of dictionaries
        matching the RawFeedback model fields.
        """
        pass
