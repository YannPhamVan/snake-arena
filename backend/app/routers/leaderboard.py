from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import LeaderboardEntry, SubmitScoreRequest, GameMode, User
from ..services.database import db_service
from ..database import get_db
from .auth import get_current_user

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])


@router.get("/", response_model=List[LeaderboardEntry])
async def get_leaderboard(
    mode: Optional[GameMode] = None,
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get leaderboard entries, optionally filtered by game mode"""
    return db_service.get_leaderboard(db, mode, limit)


@router.post("/")
async def submit_score(
    request: SubmitScoreRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit a score to the leaderboard (requires authentication)"""
    db_service.submit_score(db, current_user.id, current_user.username, request.score, request.mode)
    return {"message": "Score submitted successfully"}

