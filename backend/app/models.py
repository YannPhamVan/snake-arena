from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class GameMode(str, Enum):
    PASS_THROUGH = "pass-through"
    WALLS = "walls"

class User(BaseModel):
    id: str
    username: str
    email: EmailStr
    highScore: int

class LeaderboardEntry(BaseModel):
    id: str
    username: str
    score: int
    mode: GameMode
    timestamp: datetime

class GameSession(BaseModel):
    id: str
    userId: str
    username: str
    score: int
    mode: GameMode
    isActive: bool

class AuthResponse(BaseModel):
    user: User
    token: str

class ErrorResponse(BaseModel):
    error: str

class SignupRequest(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(min_length=6)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class SubmitScoreRequest(BaseModel):
    score: int
    mode: GameMode

class CreateSessionRequest(BaseModel):
    mode: GameMode

class UpdateSessionRequest(BaseModel):
    score: int
