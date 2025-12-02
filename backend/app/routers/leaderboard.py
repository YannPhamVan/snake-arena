from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from ..models import LeaderboardEntry, SubmitScoreRequest, GameMode
from ..services.mock_db import mock_db
from .auth import get_current_user

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])

@router.get("/", response_model=List[LeaderboardEntry])
async def get_leaderboard(
    mode: Optional[GameMode] = None,
    limit: int = Query(default=10, ge=1, le=100)
):
    return mock_db.get_leaderboard(mode, limit)

@router.post("/", dependencies=[Depends(get_current_user)])
async def submit_score(request: SubmitScoreRequest):
    # In a real app, we'd get the user from the token.
    # Here we'll just use a mock user or find one.
    # For the mock, let's just pick the first user to simulate "current user"
    users = list(mock_db.users.values())
    if not users:
        raise HTTPException(status_code=400, detail="No users found")
    
    user = users[0]
    mock_db.submit_score(user, request.score, request.mode)
    return {"message": "Score submitted successfully"}
