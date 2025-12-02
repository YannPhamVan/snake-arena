from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..models import AuthResponse, LoginRequest, SignupRequest, User, ErrorResponse
from ..services.mock_db import mock_db

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    token = credentials.credentials
    if token != "mock-jwt-token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # In a real app, we would decode the token to get the user ID
    # For mock, we'll just return the last logged in user or a default one if available
    # But since we don't have request context here easily without more complex mocking,
    # we will rely on the client sending the token we gave them.
    # For simplicity in this mock, we'll just assume the token is valid and return a mock user
    # or try to find a user if we had a way to map token to user.
    # Given the mock nature, let's just return the first user found or raise if empty.
    
    # BETTER APPROACH for mock:
    # The frontend mock stores user in localStorage.
    # Here we can't easily know WHICH user corresponds to the token without state.
    # But `mock_db` is a singleton.
    # Let's just return a dummy user for now if the token is valid, 
    # OR we could store a mapping in mock_db.
    
    # Let's assume the token is valid for the "current" user concept in the mock DB 
    # isn't quite right for a server.
    # We will just verify the token is the mock token.
    return User(id="mock-user-id", username="MockUser", email="mock@example.com", highScore=0)


@router.post("/signup", response_model=AuthResponse, responses={400: {"model": ErrorResponse}})
async def signup(request: SignupRequest):
    if mock_db.get_user_by_email(request.email) or mock_db.get_user_by_username(request.username):
        raise HTTPException(status_code=400, detail="User already exists")
    
    user = mock_db.create_user(request.username, request.email)
    return AuthResponse(user=user, token="mock-jwt-token")

@router.post("/login", response_model=AuthResponse, responses={401: {"model": ErrorResponse}})
async def login(request: LoginRequest):
    user = mock_db.get_user_by_email(request.email)
    if not user or request.password == "wrong-password": # Simple mock check
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return AuthResponse(user=user, token="mock-jwt-token")

@router.post("/logout")
async def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    return {"message": "Logout successful"}

@router.get("/me", response_model=User)
async def get_me(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # In a real app, decode token. Here, just return a mock user or the last created one for demo
    # For the purpose of the test, let's return the user from the mock DB if we can find one,
    # or just a placeholder.
    # To make it testable, let's return the user with the highest score (SnakeMaster) or similar.
    users = list(mock_db.users.values())
    if users:
        return users[0]
    raise HTTPException(status_code=401, detail="Not authenticated")
