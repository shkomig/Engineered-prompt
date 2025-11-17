"""Database module for storing and indexing prompts."""
from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import json

Base = declarative_base()


class PromptRecord(Base):
    """Database model for storing prompt generation history."""

    __tablename__ = "prompts"

    id = Column(Integer, primary_key=True, index=True)
    input_text = Column(Text, nullable=False)  # Original Hebrew text
    detected_intent = Column(String(100), nullable=False)
    detected_style = Column(String(50))
    generated_prompt = Column(Text, nullable=False)
    user_feedback = Column(String(20))  # good, bad, neutral
    rating = Column(Float)  # 1-5
    metadata_json = Column(Text)  # JSON string for additional data
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        """Convert record to dictionary."""
        return {
            "id": self.id,
            "input_text": self.input_text,
            "detected_intent": self.detected_intent,
            "detected_style": self.detected_style,
            "generated_prompt": self.generated_prompt,
            "user_feedback": self.user_feedback,
            "rating": self.rating,
            "metadata": json.loads(self.metadata_json) if self.metadata_json else {},
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class PromptDatabase:
    """Database handler for prompt storage and retrieval."""

    def __init__(self, database_url: str = "sqlite:///./prompts.db"):
        """Initialize database connection."""
        self.engine = create_engine(database_url, connect_args={"check_same_thread": False})
        Base.metadata.create_all(bind=self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_session(self) -> Session:
        """Get database session."""
        return self.SessionLocal()

    def save_prompt(
        self,
        input_text: str,
        detected_intent: str,
        generated_prompt: str,
        detected_style: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> int:
        """Save a generated prompt to the database."""
        session = self.get_session()
        try:
            record = PromptRecord(
                input_text=input_text,
                detected_intent=detected_intent,
                detected_style=detected_style,
                generated_prompt=generated_prompt,
                metadata_json=json.dumps(metadata) if metadata else None
            )
            session.add(record)
            session.commit()
            session.refresh(record)
            return record.id
        finally:
            session.close()

    def update_feedback(self, prompt_id: int, feedback: str, rating: Optional[float] = None) -> bool:
        """Update feedback for a prompt."""
        session = self.get_session()
        try:
            record = session.query(PromptRecord).filter(PromptRecord.id == prompt_id).first()
            if record:
                record.user_feedback = feedback
                if rating is not None:
                    record.rating = rating
                session.commit()
                return True
            return False
        finally:
            session.close()

    def get_prompt_history(self, limit: int = 50, intent_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve prompt history."""
        session = self.get_session()
        try:
            query = session.query(PromptRecord)
            if intent_filter:
                query = query.filter(PromptRecord.detected_intent == intent_filter)
            records = query.order_by(PromptRecord.created_at.desc()).limit(limit).all()
            return [record.to_dict() for record in records]
        finally:
            session.close()

    def get_prompt_by_id(self, prompt_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific prompt by ID."""
        session = self.get_session()
        try:
            record = session.query(PromptRecord).filter(PromptRecord.id == prompt_id).first()
            return record.to_dict() if record else None
        finally:
            session.close()

    def get_best_prompts(self, intent: str, min_rating: float = 4.0, limit: int = 10) -> List[Dict[str, Any]]:
        """Get best-rated prompts for a specific intent (for hindsight learning)."""
        session = self.get_session()
        try:
            records = (
                session.query(PromptRecord)
                .filter(
                    PromptRecord.detected_intent == intent,
                    PromptRecord.rating >= min_rating
                )
                .order_by(PromptRecord.rating.desc())
                .limit(limit)
                .all()
            )
            return [record.to_dict() for record in records]
        finally:
            session.close()

    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics."""
        session = self.get_session()
        try:
            total_prompts = session.query(PromptRecord).count()
            avg_rating = session.query(PromptRecord).filter(
                PromptRecord.rating.isnot(None)
            ).with_entities(PromptRecord.rating).all()

            intents = session.query(
                PromptRecord.detected_intent
            ).distinct().all()

            return {
                "total_prompts": total_prompts,
                "average_rating": sum(r[0] for r in avg_rating) / len(avg_rating) if avg_rating else 0,
                "total_intents": len(intents),
                "intents": [i[0] for i in intents]
            }
        finally:
            session.close()
