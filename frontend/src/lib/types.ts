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
