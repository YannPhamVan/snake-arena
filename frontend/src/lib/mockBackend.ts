import { api } from './api';
export * from './types';

// Re-export the api as mockBackend to maintain compatibility with existing code
export const mockBackend = api;
