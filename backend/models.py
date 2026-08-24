import uuid
from sqlalchemy import Column, String, Text, Float, DateTime, JSON, Boolean, ForeignKey
from database import Base

def generate_uuid():
    return str(uuid.uuid4())

class RawFeedback(Base):
    __tablename__ = "raw_feedback"

    internal_id = Column(String(36), primary_key=True, default=generate_uuid)
    source = Column(String(50), nullable=False)
    source_id = Column(String(255), nullable=False, unique=True)
    date = Column(DateTime, nullable=True)
    title = Column(String(255), nullable=True)
    text = Column(Text, nullable=False)
    rating = Column(Float, nullable=True)
    url = Column(String(512), nullable=True)
    category = Column(String(100), nullable=True)
    metadata_ = Column(JSON, nullable=True)

class NormalizedFeedback(Base):
    __tablename__ = "normalized_feedback"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    raw_id = Column(String(36), ForeignKey("raw_feedback.internal_id"), nullable=False)
    source = Column(String(50), nullable=False)
    source_id = Column(String(255), nullable=False)
    date = Column(DateTime, nullable=True)
    rating = Column(Float, nullable=True)
    original_text = Column(Text, nullable=False)
    normalized_text = Column(Text, nullable=False)
    language = Column(String(10), nullable=True)
    is_valid = Column(Boolean, default=True)
    rejection_reason = Column(String(255), nullable=True)

class ExtractedSignal(Base):
    __tablename__ = "extracted_signal"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    raw_id = Column(String(36), ForeignKey("raw_feedback.internal_id"), nullable=False, unique=True)
    signals = Column(JSON, nullable=False)
    processed_at = Column(DateTime, nullable=True)

