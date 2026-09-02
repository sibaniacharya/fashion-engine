import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime
from ai.batch_processor import BatchProcessor
from ai.extractor import LLMParseError
from pydantic import ValidationError
from models import NormalizedFeedback, ExtractedSignal
from tenacity import RetryError, Future


class MockLastAttempt:
    def __init__(self, e):
        self.e = e

    def exception(self):
        return self.e


class MockRetryError(RetryError):
    def __init__(self, e):
        self.last_attempt = MockLastAttempt(e)


@pytest.fixture
def mock_db_session():
    with patch("ai.batch_processor.SessionLocal") as mock_session_class:
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session

        # Setup mock valid records
        mock_record1 = MagicMock(spec=NormalizedFeedback)
        mock_record1.raw_id = "rec_1"
        mock_record1.source = "YOUTUBE"
        mock_record1.normalized_text = "test 1"

        mock_record2 = MagicMock(spec=NormalizedFeedback)
        mock_record2.raw_id = "rec_2"
        mock_record2.source = "YOUTUBE"
        mock_record2.normalized_text = "test 2"

        mock_session.query.return_value.filter.return_value.all.return_value = [
            mock_record1,
            mock_record2,
        ]

        # Setup empty previous extracted signals
        mock_session.query.return_value.all.return_value = []

        yield mock_session


def test_successful_response(mock_db_session):
    processor = BatchProcessor()
    processor.extractor = MagicMock()

    processor.extractor.extract_signals_batch.return_value = {
        "rec_1": {"status": "ANALYZED"},
        "rec_2": {"status": "ANALYZED"},
    }

    # Mock time.sleep to run instantly
    with patch("time.sleep"):
        res = processor.process_all(batch_limit=2)

    assert res["processed"] == 2
    assert res["failed"] == 0


def test_429_quota_exhausted_outer(mock_db_session):
    processor = BatchProcessor()
    processor.extractor = MagicMock()

    # Simulate a RetryError raising a daily quota exception
    mock_e = Exception("Rate limit reached... tokens per day")
    processor.extractor.extract_signals_batch.side_effect = MockRetryError(mock_e)

    with patch("time.sleep"):
        res = processor.process_all(batch_limit=2)

    # Ensure it added DEFERRED_QUOTA
    added_signals = []
    for call in mock_db_session.add.call_args_list:
        added_signals.append(call[0][0])

    assert len(added_signals) == 2
    for s in added_signals:
        assert s.signals["status"] == "DEFERRED_QUOTA"
        assert "tokens per day" in s.signals["error"]


def test_429_rate_limit_individual(mock_db_session):
    processor = BatchProcessor()
    processor.extractor = MagicMock()

    def mock_extract(batch):
        if len(batch) > 1:
            # Batch fails with a generic missing error, forcing individual retry
            return {}
        else:
            # Individual retry hits 429
            raise Exception("Rate limit reached")

    processor.extractor.extract_signals_batch.side_effect = mock_extract

    with patch("time.sleep"):
        res = processor.process_all(batch_limit=2)

    # Should catch the 429 bubbling up and mark remaining as DEFERRED_RATE_LIMIT
    added_signals = []
    for call in mock_db_session.add.call_args_list:
        added_signals.append(call[0][0])

    assert len(added_signals) == 2
    for s in added_signals:
        assert s.signals["status"] == "DEFERRED_RATE_LIMIT"


def test_schema_validation_failure(mock_db_session):
    processor = BatchProcessor()
    processor.extractor = MagicMock()

    def mock_extract(batch):
        if len(batch) > 1:
            return {}
        else:
            raise LLMParseError("Malformed JSON")

    processor.extractor.extract_signals_batch.side_effect = mock_extract

    with patch("time.sleep"):
        res = processor.process_all(batch_limit=2)

    added_signals = []
    for call in mock_db_session.add.call_args_list:
        added_signals.append(call[0][0])

    assert len(added_signals) == 2
    for s in added_signals:
        assert s.signals["status"] == "FAILED"
        assert s.signals["failure_reason"] == "LLM_PARSE_ERROR"


if __name__ == "__main__":
    pytest.main(["-v", __file__])
