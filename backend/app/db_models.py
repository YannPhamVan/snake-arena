from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Enum as SQLEnum, Index
from sqlalchemy.sql import func
from datetime import datetime
import uuid
from .database import Base
from .models import GameMode


def generate_uuid():
    """Generate a UUID string"""
    return str(uuid.uuid4())


class DBUser(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    high_score = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "highScore": self.high_score
        }


class DBLeaderboardEntry(Base):
    __tablename__ = "leaderboard_entries"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    username = Column(String, nullable=False)  # Denormalized for performance
    score = Column(Integer, nullable=False)
    mode = Column(SQLEnum(GameMode), nullable=False)
    timestamp = Column(DateTime, default=func.now(), nullable=False)
    
    # Indexes for common queries
    __table_args__ = (
        Index('idx_leaderboard_mode_score', 'mode', 'score'),
        Index('idx_leaderboard_timestamp', 'timestamp'),
    )
    
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "score": self.score,
            "mode": self.mode.value,
            "timestamp": self.timestamp.isoformat()
        }


class DBGameSession(Base):
    __tablename__ = "game_sessions"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    username = Column(String, nullable=False)  # Denormalized for performance
    score = Column(Integer, default=0, nullable=False)
    mode = Column(SQLEnum(GameMode), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "userId": self.user_id,
            "username": self.username,
            "score": self.score,
            "mode": self.mode.value,
            "isActive": self.is_active
        }
