import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, RawFeedback
from ingestion.manager import IngestionManager
from ingestion.base import IngestionAdapter

# Mock adapter for testing
class MockAdapter(IngestionAdapter):
    def fetch_data(self):
        return [
            {
                "internal_id": "test-uuid-1",
                "source": "MOCK",
                "source_id": "mock-1",
                "date": None,
                "title": "Mock Title",
                "text": "Mock text.",
                "rating": 5.0,
                "url": "http://mock",
                "category": "Mock",
                "metadata_": {}
            },
            {
                "internal_id": "test-uuid-2",
                "source": "MOCK",
                "source_id": "mock-2",
                "date": None,
                "title": "Mock Title 2",
                "text": "Mock text 2.",
                "rating": 4.0,
                "url": "http://mock",
                "category": "Mock",
                "metadata_": {}
            }
        ]

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_ingestion_manager(db_session):
    manager = IngestionManager(db_session)
    # Replace real adapters with mock
    manager.adapters = [MockAdapter()]
    manager.is_postgres = False
    
    results = manager.run_ingestion()
    
    assert results["MockAdapter"]["fetched"] == 2
    assert results["MockAdapter"]["saved"] == 2
    
    # Test duplicate prevention
    results2 = manager.run_ingestion()
    assert results2["MockAdapter"]["fetched"] == 2
    assert results2["MockAdapter"]["saved"] == 0
    
    # Check db
    count = db_session.query(RawFeedback).count()
    assert count == 2
