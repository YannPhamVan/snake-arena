"""Database initialization script

This script initializes the database schema and optionally seeds it with sample data.

Usage:
    # Initialize database only
    uv run python -m app.init_db
    
    # Initialize and seed with sample data
    uv run python -m app.init_db --seed
"""

import argparse
from datetime import datetime, timedelta
import random
from .database import init_db, SessionLocal
from .db_models import DBUser, DBLeaderboardEntry, DBGameSession
from .models import GameMode
from .auth import hash_password


def seed_database():
    """Seed the database with sample data"""
    db = SessionLocal()
    
    try:
        # Create mock users with varied scores
        mock_users_data = [
            {"username": "SnakeMaster", "email": "snake@example.com", "high_score": 2500},
            {"username": "GridWarrior", "email": "grid@example.com", "high_score": 2200},
            {"username": "NeonViper", "email": "neon@example.com", "high_score": 1950},
            {"username": "CyberSerpent", "email": "cyber@example.com", "high_score": 1800},
            {"username": "PixelPython", "email": "pixel@example.com", "high_score": 1650},
            {"username": "CodeCobra", "email": "cobra@example.com", "high_score": 1500},
            {"username": "ByteBasilisk", "email": "basilisk@example.com", "high_score": 1400},
            {"username": "RetroReptile", "email": "retro@example.com", "high_score": 1250},
            {"username": "ArcadeAdder", "email": "adder@example.com", "high_score": 1100},
            {"username": "GlitchGarter", "email": "garter@example.com", "high_score": 950},
        ]
        
        users = []
        for data in mock_users_data:
            user = DBUser(
                username=data["username"],
                email=data["email"],
                hashed_password=hash_password("password123"),
                high_score=data["high_score"]
            )
            db.add(user)
            users.append(user)
        
        db.commit()
        
        # Refresh users to get their IDs
        for user in users:
            db.refresh(user)
        
        # Create leaderboard entries
        for user in users:
            # Recent high score for walls mode
            entry = DBLeaderboardEntry(
                user_id=user.id,
                username=user.username,
                score=user.high_score,
                mode=GameMode.WALLS,
                timestamp=datetime.now() - timedelta(hours=random.randint(1, 24))
            )
            db.add(entry)
            
            # Older entry for walls mode
            entry = DBLeaderboardEntry(
                user_id=user.id,
                username=user.username,
                score=int(user.high_score * 0.8),
                mode=GameMode.WALLS,
                timestamp=datetime.now() - timedelta(days=random.randint(1, 7))
            )
            db.add(entry)
            
            # Recent entry for pass-through mode
            entry = DBLeaderboardEntry(
                user_id=user.id,
                username=user.username,
                score=int(user.high_score * 1.3),
                mode=GameMode.PASS_THROUGH,
                timestamp=datetime.now() - timedelta(hours=random.randint(1, 48))
            )
            db.add(entry)
            
            # Older entry for pass-through mode
            entry = DBLeaderboardEntry(
                user_id=user.id,
                username=user.username,
                score=int(user.high_score * 1.1),
                mode=GameMode.PASS_THROUGH,
                timestamp=datetime.now() - timedelta(days=random.randint(2, 14))
            )
            db.add(entry)
        
        # Create some active game sessions
        num_sessions = random.randint(3, 5)
        for i in range(num_sessions):
            user = random.choice(users)
            mode = random.choice([GameMode.WALLS, GameMode.PASS_THROUGH])
            current_score = random.randint(100, 1000)
            
            session = DBGameSession(
                user_id=user.id,
                username=user.username,
                score=current_score,
                mode=mode,
                is_active=True
            )
            db.add(session)
        
        db.commit()
        print(f"✓ Database seeded with {len(users)} users, multiple leaderboard entries, and {num_sessions} active sessions")
        
    except Exception as e:
        print(f"✗ Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser(description="Initialize the Snake Arena database")
    parser.add_argument("--seed", action="store_true", help="Seed the database with sample data")
    args = parser.parse_args()
    
    print("Initializing database...")
    init_db()
    print("✓ Database tables created successfully")
    
    if args.seed:
        print("Seeding database with sample data...")
        seed_database()
    
    print("✓ Database initialization complete!")


if __name__ == "__main__":
    main()
