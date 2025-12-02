from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ..models import GameSession, CreateSessionRequest, UpdateSessionRequest
from ..services.mock_db import mock_db
from .auth import get_current_user

router = APIRouter(prefix="/sessions", tags=["sessions"])

@router.get("/", response_model=List[GameSession])
async def get_active_sessions():
    return mock_db.get_active_sessions()

@router.post("/", response_model=GameSession, dependencies=[Depends(get_current_user)])
async def create_session(request: CreateSessionRequest):
    # Again, pick a mock user
    users = list(mock_db.users.values())
    if not users:
        raise HTTPException(status_code=400, detail="No users found")
    
    user = users[0]
    return mock_db.create_session(user, request.mode)

@router.get("/{session_id}", response_model=GameSession)
async def get_session(session_id: str):
    session = mock_db.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.put("/{session_id}", dependencies=[Depends(get_current_user)])
async def update_session(session_id: str, request: UpdateSessionRequest):
    if not mock_db.update_session_score(session_id, request.score):
        raise HTTPException(status_code=404, detail="Session not found")
    return {"message": "Session updated successfully"}

@router.delete("/{session_id}", dependencies=[Depends(get_current_user)])
async def end_session(session_id: str):
    if not mock_db.end_session(session_id):
        raise HTTPException(status_code=404, detail="Session not found")
    return {"message": "Session ended successfully"}
