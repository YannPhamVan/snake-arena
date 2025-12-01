// Centralized mock backend service
// All backend calls should go through this service

export interface User {
  id: string;
  username: string;
  email: string;
  highScore: number;
}

export interface LeaderboardEntry {
  id: string;
  username: string;
  score: number;
  mode: 'pass-through' | 'walls';
  timestamp: Date;
}

export interface GameSession {
  id: string;
  userId: string;
  username: string;
  score: number;
  mode: 'pass-through' | 'walls';
  isActive: boolean;
}

class MockBackendService {
  private users: Map<string, User> = new Map();
  private leaderboard: LeaderboardEntry[] = [];
  private activeSessions: Map<string, GameSession> = new Map();
  private currentUser: User | null = null;

  constructor() {
    this.initializeMockData();
  }

  private initializeMockData() {
    // Create mock users and leaderboard entries
    const mockUsers = [
      { username: 'SnakeMaster', email: 'snake@example.com', highScore: 2500 },
      { username: 'GridWarrior', email: 'grid@example.com', highScore: 2200 },
      { username: 'NeonViper', email: 'neon@example.com', highScore: 1950 },
      { username: 'CyberSerpent', email: 'cyber@example.com', highScore: 1800 },
      { username: 'PixelPython', email: 'pixel@example.com', highScore: 1650 },
    ];

    mockUsers.forEach((userData, index) => {
      const user: User = {
        id: `user-${index}`,
        ...userData,
      };
      this.users.set(user.id, user);

      // Add leaderboard entries for walls mode
      this.leaderboard.push({
        id: `entry-${index}-walls`,
        username: user.username,
        score: userData.highScore,
        mode: 'walls',
        timestamp: new Date(Date.now() - Math.random() * 7 * 24 * 60 * 60 * 1000),
      });

      // Add leaderboard entries for pass-through mode
      this.leaderboard.push({
        id: `entry-${index}-passthrough`,
        username: user.username,
        score: Math.floor(userData.highScore * 1.2),
        mode: 'pass-through',
        timestamp: new Date(Date.now() - Math.random() * 7 * 24 * 60 * 60 * 1000),
      });
    });

    // Sort leaderboard by score
    this.leaderboard.sort((a, b) => b.score - a.score);

    // Create some active sessions
    this.createMockActiveSessions();
  }

  private createMockActiveSessions() {
    const activeUsers = Array.from(this.users.values()).slice(0, 3);
    activeUsers.forEach((user, index) => {
      const session: GameSession = {
        id: `session-${user.id}`,
        userId: user.id,
        username: user.username,
        score: Math.floor(Math.random() * 1000),
        mode: index % 2 === 0 ? 'walls' : 'pass-through',
        isActive: true,
      };
      this.activeSessions.set(session.id, session);
    });
  }

  // Authentication methods
  async login(email: string, password: string): Promise<{ user: User; token: string } | { error: string }> {
    await this.simulateNetworkDelay();
    
    const user = Array.from(this.users.values()).find(u => u.email === email);
    
    if (!user || password.length < 6) {
      return { error: 'Invalid credentials' };
    }

    this.currentUser = user;
    localStorage.setItem('mockToken', 'mock-jwt-token');
    localStorage.setItem('mockUser', JSON.stringify(user));
    
    return { user, token: 'mock-jwt-token' };
  }

  async signup(username: string, email: string, password: string): Promise<{ user: User; token: string } | { error: string }> {
    await this.simulateNetworkDelay();
    
    const existingUser = Array.from(this.users.values()).find(
      u => u.email === email || u.username === username
    );

    if (existingUser) {
      return { error: 'User already exists' };
    }

    if (password.length < 6) {
      return { error: 'Password must be at least 6 characters' };
    }

    const newUser: User = {
      id: `user-${Date.now()}`,
      username,
      email,
      highScore: 0,
    };

    this.users.set(newUser.id, newUser);
    this.currentUser = newUser;
    localStorage.setItem('mockToken', 'mock-jwt-token');
    localStorage.setItem('mockUser', JSON.stringify(newUser));

    return { user: newUser, token: 'mock-jwt-token' };
  }

  async logout(): Promise<void> {
    await this.simulateNetworkDelay();
    this.currentUser = null;
    localStorage.removeItem('mockToken');
    localStorage.removeItem('mockUser');
  }

  getCurrentUser(): User | null {
    if (this.currentUser) return this.currentUser;
    
    const storedUser = localStorage.getItem('mockUser');
    if (storedUser) {
      this.currentUser = JSON.parse(storedUser);
      return this.currentUser;
    }
    
    return null;
  }

  // Leaderboard methods
  async getLeaderboard(mode?: 'pass-through' | 'walls', limit: number = 10): Promise<LeaderboardEntry[]> {
    await this.simulateNetworkDelay();
    
    let filtered = mode 
      ? this.leaderboard.filter(entry => entry.mode === mode)
      : this.leaderboard;

    return filtered.slice(0, limit);
  }

  async submitScore(score: number, mode: 'pass-through' | 'walls'): Promise<void> {
    await this.simulateNetworkDelay();
    
    const user = this.getCurrentUser();
    if (!user) throw new Error('Not authenticated');

    const entry: LeaderboardEntry = {
      id: `entry-${Date.now()}`,
      username: user.username,
      score,
      mode,
      timestamp: new Date(),
    };

    this.leaderboard.push(entry);
    this.leaderboard.sort((a, b) => b.score - a.score);

    // Update user's high score
    if (score > user.highScore) {
      user.highScore = score;
      this.users.set(user.id, user);
      localStorage.setItem('mockUser', JSON.stringify(user));
    }
  }

  // Active sessions methods
  async getActiveSessions(): Promise<GameSession[]> {
    await this.simulateNetworkDelay();
    return Array.from(this.activeSessions.values()).filter(s => s.isActive);
  }

  async getSession(sessionId: string): Promise<GameSession | null> {
    await this.simulateNetworkDelay();
    return this.activeSessions.get(sessionId) || null;
  }

  async createSession(mode: 'pass-through' | 'walls'): Promise<GameSession> {
    await this.simulateNetworkDelay();
    
    const user = this.getCurrentUser();
    if (!user) throw new Error('Not authenticated');

    const session: GameSession = {
      id: `session-${Date.now()}`,
      userId: user.id,
      username: user.username,
      score: 0,
      mode,
      isActive: true,
    };

    this.activeSessions.set(session.id, session);
    return session;
  }

  async updateSession(sessionId: string, score: number): Promise<void> {
    await this.simulateNetworkDelay();
    
    const session = this.activeSessions.get(sessionId);
    if (session) {
      session.score = score;
      this.activeSessions.set(sessionId, session);
    }
  }

  async endSession(sessionId: string): Promise<void> {
    await this.simulateNetworkDelay();
    
    const session = this.activeSessions.get(sessionId);
    if (session) {
      session.isActive = false;
      this.activeSessions.set(sessionId, session);
    }
  }

  private async simulateNetworkDelay(): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, 300 + Math.random() * 200));
  }
}

export const mockBackend = new MockBackendService();
