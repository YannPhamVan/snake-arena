// AI player logic for spectate mode

import { Position, Direction, GameState, GRID_SIZE, getNextHeadPosition, wrapPosition } from './gameLogic';

export function getAIDirection(state: GameState, mode: 'pass-through' | 'walls'): Direction {
  const head = state.snake[0];
  const food = state.food;
  
  // Calculate possible moves
  const possibleMoves: Direction[] = ['UP', 'DOWN', 'LEFT', 'RIGHT'];
  const currentDirection = state.direction;
  
  // Remove opposite direction
  const opposites: Record<Direction, Direction> = {
    UP: 'DOWN',
    DOWN: 'UP',
    LEFT: 'RIGHT',
    RIGHT: 'LEFT',
  };
  
  const validMoves = possibleMoves.filter(dir => dir !== opposites[currentDirection]);
  
  // Score each move
  const moveScores = validMoves.map(direction => {
    const nextHead = getNextHeadPosition(head, direction);
    const wrappedHead = mode === 'pass-through' ? wrapPosition(nextHead) : nextHead;
    
    let score = 0;
    
    // Avoid walls in walls mode
    if (mode === 'walls' && (
      wrappedHead.x < 0 || wrappedHead.x >= GRID_SIZE ||
      wrappedHead.y < 0 || wrappedHead.y >= GRID_SIZE
    )) {
      score -= 1000;
    }
    
    // Avoid self-collision
    if (state.snake.some(segment => segment.x === wrappedHead.x && segment.y === wrappedHead.y)) {
      score -= 1000;
    }
    
    // Move towards food
    const distanceToFood = Math.abs(wrappedHead.x - food.x) + Math.abs(wrappedHead.y - food.y);
    score -= distanceToFood;
    
    // Prefer continuing in the same direction (smooth movement)
    if (direction === currentDirection) {
      score += 2;
    }
    
    // Avoid corners in walls mode
    if (mode === 'walls') {
      const distanceToWall = Math.min(
        wrappedHead.x,
        wrappedHead.y,
        GRID_SIZE - 1 - wrappedHead.x,
        GRID_SIZE - 1 - wrappedHead.y
      );
      
      if (distanceToWall <= 1) {
        score -= 50;
      }
    }
    
    return { direction, score };
  });
  
  // Sort by score and pick the best move
  moveScores.sort((a, b) => b.score - a.score);
  
  // Add some randomness (10% chance to pick a suboptimal move)
  if (Math.random() < 0.1 && moveScores.length > 1) {
    return moveScores[1].direction;
  }
  
  return moveScores[0].direction;
}
