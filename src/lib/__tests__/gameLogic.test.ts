import { describe, it, expect } from 'vitest';
import {
  createInitialGameState,
  generateFood,
  getNextHeadPosition,
  wrapPosition,
  isOutOfBounds,
  checkSelfCollision,
  moveSnake,
  changeDirection,
  getGameSpeed,
  GRID_SIZE,
} from '../gameLogic';

describe('gameLogic', () => {
  describe('createInitialGameState', () => {
    it('should create a valid initial game state', () => {
      const state = createInitialGameState();
      
      expect(state.snake).toHaveLength(3);
      expect(state.direction).toBe('RIGHT');
      expect(state.score).toBe(0);
      expect(state.gameOver).toBe(false);
      expect(state.paused).toBe(false);
      expect(state.food).toBeDefined();
    });

    it('should place snake in center of grid', () => {
      const state = createInitialGameState();
      const center = Math.floor(GRID_SIZE / 2);
      
      expect(state.snake[0].x).toBe(center);
      expect(state.snake[0].y).toBe(center);
    });
  });

  describe('generateFood', () => {
    it('should generate food within grid bounds', () => {
      const snake = [{ x: 10, y: 10 }];
      const food = generateFood(snake);
      
      expect(food.x).toBeGreaterThanOrEqual(0);
      expect(food.x).toBeLessThan(GRID_SIZE);
      expect(food.y).toBeGreaterThanOrEqual(0);
      expect(food.y).toBeLessThan(GRID_SIZE);
    });

    it('should not generate food on snake position', () => {
      const snake = [{ x: 5, y: 5 }];
      const food = generateFood(snake);
      
      expect(food.x !== 5 || food.y !== 5).toBe(true);
    });
  });

  describe('getNextHeadPosition', () => {
    it('should move up correctly', () => {
      const head = { x: 5, y: 5 };
      const next = getNextHeadPosition(head, 'UP');
      
      expect(next.x).toBe(5);
      expect(next.y).toBe(4);
    });

    it('should move down correctly', () => {
      const head = { x: 5, y: 5 };
      const next = getNextHeadPosition(head, 'DOWN');
      
      expect(next.x).toBe(5);
      expect(next.y).toBe(6);
    });

    it('should move left correctly', () => {
      const head = { x: 5, y: 5 };
      const next = getNextHeadPosition(head, 'LEFT');
      
      expect(next.x).toBe(4);
      expect(next.y).toBe(5);
    });

    it('should move right correctly', () => {
      const head = { x: 5, y: 5 };
      const next = getNextHeadPosition(head, 'RIGHT');
      
      expect(next.x).toBe(6);
      expect(next.y).toBe(5);
    });
  });

  describe('wrapPosition', () => {
    it('should wrap negative x position', () => {
      const pos = { x: -1, y: 5 };
      const wrapped = wrapPosition(pos);
      
      expect(wrapped.x).toBe(GRID_SIZE - 1);
      expect(wrapped.y).toBe(5);
    });

    it('should wrap position exceeding grid width', () => {
      const pos = { x: GRID_SIZE, y: 5 };
      const wrapped = wrapPosition(pos);
      
      expect(wrapped.x).toBe(0);
      expect(wrapped.y).toBe(5);
    });

    it('should wrap negative y position', () => {
      const pos = { x: 5, y: -1 };
      const wrapped = wrapPosition(pos);
      
      expect(wrapped.x).toBe(5);
      expect(wrapped.y).toBe(GRID_SIZE - 1);
    });
  });

  describe('isOutOfBounds', () => {
    it('should return true for negative x', () => {
      expect(isOutOfBounds({ x: -1, y: 5 })).toBe(true);
    });

    it('should return true for x beyond grid', () => {
      expect(isOutOfBounds({ x: GRID_SIZE, y: 5 })).toBe(true);
    });

    it('should return true for negative y', () => {
      expect(isOutOfBounds({ x: 5, y: -1 })).toBe(true);
    });

    it('should return false for valid position', () => {
      expect(isOutOfBounds({ x: 5, y: 5 })).toBe(false);
    });
  });

  describe('checkSelfCollision', () => {
    it('should detect collision with body', () => {
      const head = { x: 5, y: 5 };
      const body = [
        { x: 6, y: 5 },
        { x: 5, y: 5 }, // Same as head
        { x: 4, y: 5 },
      ];
      
      expect(checkSelfCollision(head, body)).toBe(true);
    });

    it('should return false when no collision', () => {
      const head = { x: 5, y: 5 };
      const body = [
        { x: 6, y: 5 },
        { x: 7, y: 5 },
        { x: 8, y: 5 },
      ];
      
      expect(checkSelfCollision(head, body)).toBe(false);
    });
  });

  describe('moveSnake', () => {
    it('should move snake forward in pass-through mode', () => {
      const state = createInitialGameState();
      const newState = moveSnake(state, 'pass-through');
      
      expect(newState.snake[0].x).toBe(state.snake[0].x + 1);
    });

    it('should wrap around in pass-through mode', () => {
      const state = createInitialGameState();
      state.snake = [{ x: GRID_SIZE - 1, y: 10 }];
      state.direction = 'RIGHT';
      
      const newState = moveSnake(state, 'pass-through');
      
      expect(newState.snake[0].x).toBe(0);
    });

    it('should end game on wall collision in walls mode', () => {
      const state = createInitialGameState();
      state.snake = [{ x: GRID_SIZE - 1, y: 10 }];
      state.direction = 'RIGHT';
      
      const newState = moveSnake(state, 'walls');
      
      expect(newState.gameOver).toBe(true);
    });

    it('should increase score when eating food', () => {
      const state = createInitialGameState();
      state.food = { x: state.snake[0].x + 1, y: state.snake[0].y };
      state.direction = 'RIGHT';
      
      const newState = moveSnake(state, 'pass-through');
      
      expect(newState.score).toBe(10);
      expect(newState.snake.length).toBe(state.snake.length + 1);
    });

    it('should not move when paused', () => {
      const state = createInitialGameState();
      state.paused = true;
      
      const newState = moveSnake(state, 'pass-through');
      
      expect(newState).toEqual(state);
    });

    it('should not move when game over', () => {
      const state = createInitialGameState();
      state.gameOver = true;
      
      const newState = moveSnake(state, 'walls');
      
      expect(newState).toEqual(state);
    });

    it('should end game on self-collision', () => {
      const state = createInitialGameState();
      state.snake = [
        { x: 5, y: 5 },
        { x: 6, y: 5 },
        { x: 6, y: 6 },
        { x: 5, y: 6 },
      ];
      state.direction = 'LEFT';
      
      const newState = moveSnake(state, 'pass-through');
      
      expect(newState.gameOver).toBe(true);
    });
  });

  describe('changeDirection', () => {
    it('should change to new direction', () => {
      const newDir = changeDirection('RIGHT', 'UP');
      expect(newDir).toBe('UP');
    });

    it('should not allow reversing direction', () => {
      const newDir = changeDirection('RIGHT', 'LEFT');
      expect(newDir).toBe('RIGHT');
    });

    it('should not allow UP when moving DOWN', () => {
      const newDir = changeDirection('DOWN', 'UP');
      expect(newDir).toBe('DOWN');
    });
  });

  describe('getGameSpeed', () => {
    it('should return initial speed at score 0', () => {
      expect(getGameSpeed(0)).toBe(150);
    });

    it('should decrease speed as score increases', () => {
      const speed0 = getGameSpeed(0);
      const speed100 = getGameSpeed(100);
      
      expect(speed100).toBeLessThan(speed0);
    });

    it('should not go below minimum speed', () => {
      const speed = getGameSpeed(10000);
      expect(speed).toBeGreaterThanOrEqual(50);
    });
  });
});
