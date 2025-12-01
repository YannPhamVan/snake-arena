import { describe, it, expect } from 'vitest';
import { getAIDirection } from '../aiPlayer';
import { createInitialGameState, Direction } from '../gameLogic';

describe('aiPlayer', () => {
  describe('getAIDirection', () => {
    it('should return a valid direction', () => {
      const state = createInitialGameState();
      const direction = getAIDirection(state, 'walls');
      
      const validDirections: Direction[] = ['UP', 'DOWN', 'LEFT', 'RIGHT'];
      expect(validDirections).toContain(direction);
    });

    it('should not reverse direction', () => {
      const state = createInitialGameState();
      state.direction = 'RIGHT';
      
      const direction = getAIDirection(state, 'walls');
      
      expect(direction).not.toBe('LEFT');
    });

    it('should move towards food when safe', () => {
      const state = createInitialGameState();
      state.snake = [{ x: 5, y: 5 }];
      state.food = { x: 5, y: 3 }; // Food above
      state.direction = 'RIGHT';
      
      const direction = getAIDirection(state, 'walls');
      
      // Should prefer moving towards food (UP)
      expect(direction).toBe('UP');
    });

    it('should avoid walls in walls mode', () => {
      const state = createInitialGameState();
      state.snake = [{ x: 0, y: 5 }]; // At left edge
      state.food = { x: 10, y: 5 };
      state.direction = 'UP';
      
      const direction = getAIDirection(state, 'walls');
      
      // Should not go LEFT (into wall)
      expect(direction).not.toBe('LEFT');
    });

    it('should avoid self-collision', () => {
      const state = createInitialGameState();
      state.snake = [
        { x: 5, y: 5 }, // Head
        { x: 5, y: 6 }, // Body below
        { x: 4, y: 6 }, // Body left-below
        { x: 4, y: 5 }, // Body left
      ];
      state.food = { x: 10, y: 5 };
      state.direction = 'DOWN';
      
      const direction = getAIDirection(state, 'walls');
      
      // Should avoid LEFT (self-collision)
      expect(direction).not.toBe('LEFT');
    });

    it('should work in pass-through mode', () => {
      const state = createInitialGameState();
      state.snake = [{ x: 0, y: 5 }];
      state.food = { x: 19, y: 5 }; // Food on opposite side
      state.direction = 'UP';
      
      const direction = getAIDirection(state, 'pass-through');
      
      // In pass-through mode, can go LEFT to wrap around
      expect(['LEFT', 'UP', 'DOWN']).toContain(direction);
    });
  });
});
