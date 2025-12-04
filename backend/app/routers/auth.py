from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from ..models import AuthResponse, LoginRequest, SignupRequest, User, ErrorResponse
from ..services.database import db_service
from ..database import get_db
from ..auth import create_access_token, decode_access_token

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to get the current authenticated user from JWT token.
    Raises HTTPException if token is invalid or user not found.
    """
    token = credentials.credentials
    
    # Decode the JWT token
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Extract user ID from token
    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user from database
    db_user = db_service.get_user_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return User(**db_user.to_dict())


@router.post("/signup", response_model=AuthResponse, responses={400: {"model": ErrorResponse}})
async def signup(request: SignupRequest, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if user already exists
    if db_service.get_user_by_email(db, request.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    if db_service.get_user_by_username(db, request.username):
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Create user with hashed password
    user = db_service.create_user(db, request.username, request.email, request.password)
    
    # Generate JWT token
    access_token = create_access_token(data={"sub": user.id})
    
    return AuthResponse(user=user, token=access_token)


@router.post("/login", response_model=AuthResponse, responses={401: {"model": ErrorResponse}})
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Login a user"""
    # Verify credentials
    db_user = db_service.verify_user_password(db, request.email, request.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Generate JWT token
    access_token = create_access_token(data={"sub": db_user.id})
    
    return AuthResponse(user=User(**db_user.to_dict()), token=access_token)


@router.post("/logout")
async def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Logout the current user (client-side - just invalidate token)"""
    return {"message": "Logout successful"}


@router.get("/me", response_model=User)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current authenticated user profile"""
    return current_user
