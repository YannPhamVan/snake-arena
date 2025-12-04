from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from ..db_models import DBUser, DBLeaderboardEntry, DBGameSession
from ..models import User, LeaderboardEntry, GameSession, GameMode
from ..auth import hash_password, verify_password


class DatabaseService:
    """Database service for handling all database operations"""
    
    # User operations
    @staticmethod
    def create_user(db: Session, username: str, email: str, password: str) -> User:
        """Create a new user with hashed password"""
        hashed_pw = hash_password(password)
        db_user = DBUser(
            username=username,
            email=email,
            hashed_password=hashed_pw,
            high_score=0
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return User(**db_user.to_dict())
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[DBUser]:
        """Get user by email"""
        return db.query(DBUser).filter(DBUser.email == email).first()
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[DBUser]:
        """Get user by username"""
        return db.query(DBUser).filter(DBUser.username == username).first()
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: str) -> Optional[DBUser]:
        """Get user by ID"""
        return db.query(DBUser).filter(DBUser.id == user_id).first()
    
    @staticmethod
    def verify_user_password(db: Session, email: str, password: str) -> Optional[DBUser]:
        """Verify user password and return user if valid"""
        user = DatabaseService.get_user_by_email(db, email)
        if user and verify_password(password, user.hashed_password):
            return user
        return None
    
    @staticmethod
    def update_user_high_score(db: Session, user_id: str, new_score: int) -> bool:
        """Update user's high score if new score is higher"""
        user = DatabaseService.get_user_by_id(db, user_id)
        if user and new_score > user.high_score:
            user.high_score = new_score
            db.commit()
            return True
        return False
    
    # Leaderboard operations
    @staticmethod
    def get_leaderboard(
        db: Session, 
        mode: Optional[GameMode] = None, 
        limit: int = 10
    ) -> List[LeaderboardEntry]:
        """Get leaderboard entries, optionally filtered by mode"""
        query = db.query(DBLeaderboardEntry)
        
        if mode:
            query = query.filter(DBLeaderboardEntry.mode == mode)
        
        entries = query.order_by(desc(DBLeaderboardEntry.score)).limit(limit).all()
        return [LeaderboardEntry(**entry.to_dict()) for entry in entries]
    
    @staticmethod
    def submit_score(
        db: Session, 
        user_id: str, 
        username: str, 
        score: int, 
        mode: GameMode
    ) -> LeaderboardEntry:
        """Submit a score to the leaderboard"""
        entry = DBLeaderboardEntry(
            user_id=user_id,
            username=username,
            score=score,
            mode=mode
        )
        db.add(entry)
        db.commit()
        db.refresh(entry)
        
        # Update user's high score if needed
        DatabaseService.update_user_high_score(db, user_id, score)
        
        return LeaderboardEntry(**entry.to_dict())
    
    # Session operations
    @staticmethod
    def create_session(db: Session, user_id: str, username: str, mode: GameMode) -> GameSession:
        """Create a new game session"""
        session = DBGameSession(
            user_id=user_id,
            username=username,
            score=0,
            mode=mode,
            is_active=True
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        return GameSession(**session.to_dict())
    
    @staticmethod
    def get_active_sessions(db: Session) -> List[GameSession]:
        """Get all active game sessions"""
        sessions = db.query(DBGameSession).filter(DBGameSession.is_active == True).all()
        return [GameSession(**session.to_dict()) for session in sessions]
    
    @staticmethod
    def get_session(db: Session, session_id: str) -> Optional[GameSession]:
        """Get a game session by ID"""
        session = db.query(DBGameSession).filter(DBGameSession.id == session_id).first()
        return GameSession(**session.to_dict()) if session else None
    
    @staticmethod
    def update_session_score(db: Session, session_id: str, score: int) -> bool:
        """Update session score"""
        session = db.query(DBGameSession).filter(DBGameSession.id == session_id).first()
        if session:
            session.score = score
            db.commit()
            return True
        return False
    
    @staticmethod
    def end_session(db: Session, session_id: str) -> bool:
        """End a game session"""
        session = db.query(DBGameSession).filter(DBGameSession.id == session_id).first()
        if session:
            session.is_active = False
            db.commit()
            return True
        return False


# Singleton instance
db_service = DatabaseService()
