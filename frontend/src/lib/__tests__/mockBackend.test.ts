import { describe, it, expect, beforeEach } from 'vitest';
import { mockBackend } from '../mockBackend';

describe('mockBackend', () => {
  beforeEach(() => {
    // Clear localStorage and backend state before each test
    localStorage.clear();
    mockBackend.reset();
  });

  describe('Authentication', () => {
    describe('signup', () => {
      it('should create a new user', async () => {
        const result = await mockBackend.signup('testuser', 'test@example.com', 'password123');

        expect('user' in result).toBe(true);
        if ('user' in result) {
          expect(result.user.username).toBe('testuser');
          expect(result.user.email).toBe('test@example.com');
          expect(result.user.highScore).toBe(0);
        }
      });

      it('should reject short passwords', async () => {
        const result = await mockBackend.signup('testuser', 'test@example.com', '123');

        expect('error' in result).toBe(true);
        if ('error' in result) {
          expect(result.error).toContain('at least 6 characters');
        }
      });

      it('should reject duplicate username', async () => {
        await mockBackend.signup('testuser', 'test1@example.com', 'password123');
        const result = await mockBackend.signup('testuser', 'test2@example.com', 'password123');

        expect('error' in result).toBe(true);
        if ('error' in result) {
          expect(result.error).toContain('already exists');
        }
      });

      it('should reject duplicate email', async () => {
        await mockBackend.signup('user1', 'test@example.com', 'password123');
        const result = await mockBackend.signup('user2', 'test@example.com', 'password123');

        expect('error' in result).toBe(true);
      });

      it('should store user in localStorage', async () => {
        await mockBackend.signup('testuser', 'test@example.com', 'password123');

        const storedUser = localStorage.getItem('mockUser');
        expect(storedUser).toBeTruthy();

        if (storedUser) {
          const user = JSON.parse(storedUser);
          expect(user.username).toBe('testuser');
        }
      });
    });

    describe('login', () => {
      beforeEach(async () => {
        await mockBackend.signup('testuser', 'test@example.com', 'password123');
        await mockBackend.logout();
      });

      it('should login existing user', async () => {
        const result = await mockBackend.login('test@example.com', 'password123');

        expect('user' in result).toBe(true);
        if ('user' in result) {
          expect(result.user.username).toBe('testuser');
        }
      });

      it('should reject invalid email', async () => {
        const result = await mockBackend.login('wrong@example.com', 'password123');

        expect('error' in result).toBe(true);
      });

      it('should reject short password', async () => {
        const result = await mockBackend.login('test@example.com', '123');

        expect('error' in result).toBe(true);
      });
    });

    describe('logout', () => {
      it('should clear user session', async () => {
        await mockBackend.signup('testuser', 'test@example.com', 'password123');
        await mockBackend.logout();

        const user = mockBackend.getCurrentUser();
        expect(user).toBeNull();
        expect(localStorage.getItem('mockToken')).toBeNull();
        expect(localStorage.getItem('mockUser')).toBeNull();
      });
    });

    describe('getCurrentUser', () => {
      it('should return null when not logged in', () => {
        const user = mockBackend.getCurrentUser();
        expect(user).toBeNull();
      });

      it('should return user when logged in', async () => {
        await mockBackend.signup('testuser', 'test@example.com', 'password123');

        const user = mockBackend.getCurrentUser();
        expect(user).toBeTruthy();
        expect(user?.username).toBe('testuser');
      });

      it('should restore user from localStorage', async () => {
        await mockBackend.signup('testuser', 'test@example.com', 'password123');

        // Simulate page refresh by creating new instance check
        const user = mockBackend.getCurrentUser();
        expect(user).toBeTruthy();
      });
    });
  });

  describe('Leaderboard', () => {
    beforeEach(async () => {
      await mockBackend.signup('testuser', 'test@example.com', 'password123');
    });

    describe('getLeaderboard', () => {
      it('should return leaderboard entries', async () => {
        const leaderboard = await mockBackend.getLeaderboard();

        expect(Array.isArray(leaderboard)).toBe(true);
        expect(leaderboard.length).toBeGreaterThan(0);
      });

      it('should filter by mode', async () => {
        const wallsLeaderboard = await mockBackend.getLeaderboard('walls');

        expect(wallsLeaderboard.every(entry => entry.mode === 'walls')).toBe(true);
      });

      it('should respect limit parameter', async () => {
        const leaderboard = await mockBackend.getLeaderboard(undefined, 5);

        expect(leaderboard.length).toBeLessThanOrEqual(5);
      });

      it('should return entries sorted by score', async () => {
        const leaderboard = await mockBackend.getLeaderboard();

        for (let i = 0; i < leaderboard.length - 1; i++) {
          expect(leaderboard[i].score).toBeGreaterThanOrEqual(leaderboard[i + 1].score);
        }
      });
    });

    describe('submitScore', () => {
      it('should add score to leaderboard', async () => {
        await mockBackend.submitScore(1000, 'walls');

        const leaderboard = await mockBackend.getLeaderboard('walls');
        const userEntry = leaderboard.find(entry => entry.username === 'testuser');

        expect(userEntry).toBeTruthy();
      });

      it('should update high score', async () => {
        const user = mockBackend.getCurrentUser();
        const initialHighScore = user?.highScore || 0;

        await mockBackend.submitScore(5000, 'walls');

        const updatedUser = mockBackend.getCurrentUser();
        expect(updatedUser?.highScore).toBeGreaterThan(initialHighScore);
      });

      it('should not decrease high score', async () => {
        await mockBackend.submitScore(5000, 'walls');
        const highScore = mockBackend.getCurrentUser()?.highScore;

        await mockBackend.submitScore(1000, 'walls');

        expect(mockBackend.getCurrentUser()?.highScore).toBe(highScore);
      });

      it('should require authentication', async () => {
        await mockBackend.logout();

        await expect(mockBackend.submitScore(1000, 'walls')).rejects.toThrow();
      });
    });
  });

  describe('Game Sessions', () => {
    beforeEach(async () => {
      await mockBackend.signup('testuser', 'test@example.com', 'password123');
    });

    describe('createSession', () => {
      it('should create a new game session', async () => {
        const session = await mockBackend.createSession('walls');

        expect(session.userId).toBeTruthy();
        expect(session.username).toBe('testuser');
        expect(session.mode).toBe('walls');
        expect(session.isActive).toBe(true);
        expect(session.score).toBe(0);
      });

      it('should require authentication', async () => {
        await mockBackend.logout();

        await expect(mockBackend.createSession('walls')).rejects.toThrow();
      });
    });

    describe('getActiveSessions', () => {
      it('should return active sessions', async () => {
        await mockBackend.createSession('walls');
        const sessions = await mockBackend.getActiveSessions();

        expect(Array.isArray(sessions)).toBe(true);
        expect(sessions.length).toBeGreaterThan(0);
        expect(sessions.every(s => s.isActive)).toBe(true);
      });
    });

    describe('updateSession', () => {
      it('should update session score', async () => {
        const session = await mockBackend.createSession('walls');
        await mockBackend.updateSession(session.id, 500);

        const updated = await mockBackend.getSession(session.id);
        expect(updated?.score).toBe(500);
      });
    });

    describe('endSession', () => {
      it('should mark session as inactive', async () => {
        const session = await mockBackend.createSession('walls');
        await mockBackend.endSession(session.id);

        const ended = await mockBackend.getSession(session.id);
        expect(ended?.isActive).toBe(false);
      });
    });
  });
});
