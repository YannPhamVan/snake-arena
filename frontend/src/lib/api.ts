import { User, LeaderboardEntry, GameSession } from './types';

const API_BASE = '/api';

class ApiError extends Error {
    constructor(public status: number, message: string) {
        super(message);
        this.name = 'ApiError';
    }
}

async function request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const token = localStorage.getItem('mockToken'); // Using same key for compatibility
    const headers: HeadersInit = {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
        ...options.headers,
    };

    const response = await fetch(`${API_BASE}${endpoint}`, {
        ...options,
        headers,
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ error: 'Unknown error' }));
        throw new ApiError(response.status, errorData.error || response.statusText);
    }

    // Handle 204 No Content
    if (response.status === 204) {
        return {} as T;
    }

    return response.json();
}

export const api = {
    // Auth
    async login(email: string, password: string): Promise<{ user: User; token: string }> {
        const data = await request<{ user: User; token: string }>('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password }),
        });
        localStorage.setItem('mockToken', data.token);
        localStorage.setItem('mockUser', JSON.stringify(data.user));
        return data;
    },

    async signup(username: string, email: string, password: string): Promise<{ user: User; token: string }> {
        const data = await request<{ user: User; token: string }>('/auth/signup', {
            method: 'POST',
            body: JSON.stringify({ username, email, password }),
        });
        localStorage.setItem('mockToken', data.token);
        localStorage.setItem('mockUser', JSON.stringify(data.user));
        return data;
    },

    async logout(): Promise<void> {
        try {
            await request('/auth/logout', { method: 'POST' });
        } catch (error) {
            console.error('Logout failed:', error);
        } finally {
            localStorage.removeItem('mockToken');
            localStorage.removeItem('mockUser');
        }
    },

    async getCurrentUser(): Promise<User | null> {
        try {
            return await request<User>('/auth/me');
        } catch (error) {
            return null;
        }
    },

    // Leaderboard
    async getLeaderboard(mode?: 'pass-through' | 'walls', limit: number = 10): Promise<LeaderboardEntry[]> {
        const params = new URLSearchParams();
        if (mode) params.append('mode', mode);
        params.append('limit', limit.toString());
        return request<LeaderboardEntry[]>(`/leaderboard/?${params.toString()}`);
    },

    async submitScore(score: number, mode: 'pass-through' | 'walls'): Promise<void> {
        await request('/leaderboard/', {
            method: 'POST',
            body: JSON.stringify({ score, mode }),
        });
    },

    // Sessions
    async getActiveSessions(): Promise<GameSession[]> {
        return request<GameSession[]>('/sessions/');
    },

    async getSession(id: string): Promise<GameSession | null> {
        try {
            return await request<GameSession>(`/sessions/${id}`);
        } catch (error) {
            if (error instanceof ApiError && error.status === 404) return null;
            throw error;
        }
    },

    async createSession(mode: 'pass-through' | 'walls'): Promise<GameSession> {
        return request<GameSession>('/sessions/', {
            method: 'POST',
            body: JSON.stringify({ mode }),
        });
    },

    async updateSession(id: string, score: number): Promise<void> {
        await request(`/sessions/${id}`, {
            method: 'PUT',
            body: JSON.stringify({ score }),
        });
    },

    async endSession(id: string): Promise<void> {
        await request(`/sessions/${id}`, {
            method: 'DELETE',
        });
    },
};
