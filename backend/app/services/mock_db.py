import uuid
from datetime import datetime
from typing import List, Optional, Dict
from ..models import User, LeaderboardEntry, GameSession, GameMode

class MockDatabase:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MockDatabase, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.users: Dict[str, User] = {}
        self.leaderboard: List[LeaderboardEntry] = []
        self.active_sessions: Dict[str, GameSession] = {}
        self._initialize_mock_data()

    def _initialize_mock_data(self):
        # Create mock users
        mock_users_data = [
            {"username": "SnakeMaster", "email": "snake@example.com", "highScore": 2500},
            {"username": "GridWarrior", "email": "grid@example.com", "highScore": 2200},
            {"username": "NeonViper", "email": "neon@example.com", "highScore": 1950},
            {"username": "CyberSerpent", "email": "cyber@example.com", "highScore": 1800},
            {"username": "PixelPython", "email": "pixel@example.com", "highScore": 1650},
        ]

        for i, data in enumerate(mock_users_data):
            user_id = f"user-{i}"
            user = User(id=user_id, **data)
            self.users[user_id] = user

            # Add leaderboard entries
            self.leaderboard.append(LeaderboardEntry(
                id=f"entry-{i}-walls",
                username=user.username,
                score=user.highScore,
                mode=GameMode.WALLS,
                timestamp=datetime.now()
            ))
            self.leaderboard.append(LeaderboardEntry(
                id=f"entry-{i}-passthrough",
                username=user.username,
                score=int(user.highScore * 1.2),
                mode=GameMode.PASS_THROUGH,
                timestamp=datetime.now()
            ))

        self.leaderboard.sort(key=lambda x: x.score, reverse=True)

    def reset(self):
        self._initialize()

    # User methods
    def get_user_by_email(self, email: str) -> Optional[User]:
        for user in self.users.values():
            if user.email == email:
                return user
        return None

    def get_user_by_username(self, username: str) -> Optional[User]:
        for user in self.users.values():
            if user.username == username:
                return user
        return None

    def create_user(self, username: str, email: str) -> User:
        user_id = f"user-{uuid.uuid4()}"
        user = User(id=user_id, username=username, email=email, highScore=0)
        self.users[user_id] = user
        return user

    # Leaderboard methods
    def get_leaderboard(self, mode: Optional[GameMode] = None, limit: int = 10) -> List[LeaderboardEntry]:
        entries = self.leaderboard
        if mode:
            entries = [e for e in entries if e.mode == mode]
        return entries[:limit]

    def submit_score(self, user: User, score: int, mode: GameMode):
        entry = LeaderboardEntry(
            id=f"entry-{uuid.uuid4()}",
            username=user.username,
            score=score,
            mode=mode,
            timestamp=datetime.now()
        )
        self.leaderboard.append(entry)
        self.leaderboard.sort(key=lambda x: x.score, reverse=True)

        if score > user.highScore:
            user.highScore = score
            self.users[user.id] = user

    # Session methods
    def create_session(self, user: User, mode: GameMode) -> GameSession:
        session_id = f"session-{uuid.uuid4()}"
        session = GameSession(
            id=session_id,
            userId=user.id,
            username=user.username,
            score=0,
            mode=mode,
            isActive=True
        )
        self.active_sessions[session_id] = session
        return session

    def get_active_sessions(self) -> List[GameSession]:
        return [s for s in self.active_sessions.values() if s.isActive]

    def get_session(self, session_id: str) -> Optional[GameSession]:
        return self.active_sessions.get(session_id)

    def update_session_score(self, session_id: str, score: int) -> bool:
        session = self.active_sessions.get(session_id)
        if session:
            session.score = score
            return True
        return False

    def end_session(self, session_id: str) -> bool:
        session = self.active_sessions.get(session_id)
        if session:
            session.isActive = False
            return True
        return False

mock_db = MockDatabase()
