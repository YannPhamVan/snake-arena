from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from ..models import GameSession, CreateSessionRequest, UpdateSessionRequest, User
from ..services.database import db_service
from ..database import get_db
from .auth import get_current_user

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.get("/", response_model=List[GameSession])
async def get_active_sessions(db: Session = Depends(get_db)):
    """Get all active game sessions"""
    return db_service.get_active_sessions(db)


@router.post("/", response_model=GameSession)
async def create_session(
    request: CreateSessionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new game session (requires authentication)"""
    return db_service.create_session(db, current_user.id, current_user.username, request.mode)


@router.get("/{session_id}", response_model=GameSession)
async def get_session(session_id: str, db: Session = Depends(get_db)):
    """Get a game session by ID"""
    session = db_service.get_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.put("/{session_id}")
async def update_session(
    session_id: str,
    request: UpdateSessionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update session score (requires authentication)"""
    if not db_service.update_session_score(db, session_id, request.score):
        raise HTTPException(status_code=404, detail="Session not found")
    return {"message": "Session updated successfully"}


@router.delete("/{session_id}")
async def end_session(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """End a game session (requires authentication)"""
    if not db_service.end_session(db, session_id):
        raise HTTPException(status_code=404, detail="Session not found")
    return {"message": "Session ended successfully"}

