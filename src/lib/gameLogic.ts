// Core game logic for Snake

export type Direction = 'UP' | 'DOWN' | 'LEFT' | 'RIGHT';
export type GameMode = 'pass-through' | 'walls';

export interface Position {
  x: number;
  y: number;
}

export interface GameState {
  snake: Position[];
  food: Position;
  direction: Direction;
  score: number;
  gameOver: boolean;
  paused: boolean;
}

export const GRID_SIZE = 20;
export const INITIAL_SPEED = 150; // ms per move

export function createInitialGameState(): GameState {
  const center = Math.floor(GRID_SIZE / 2);
  return {
    snake: [
      { x: center, y: center },
      { x: center - 1, y: center },
      { x: center - 2, y: center },
    ],
    food: generateFood([{ x: center, y: center }]),
    direction: 'RIGHT',
    score: 0,
    gameOver: false,
    paused: false,
  };
}

export function generateFood(snake: Position[]): Position {
  let food: Position;
  do {
    food = {
      x: Math.floor(Math.random() * GRID_SIZE),
      y: Math.floor(Math.random() * GRID_SIZE),
    };
  } while (snake.some(segment => segment.x === food.x && segment.y === food.y));
  return food;
}

export function getNextHeadPosition(head: Position, direction: Direction): Position {
  const next = { ...head };
  
  switch (direction) {
    case 'UP':
      next.y -= 1;
      break;
    case 'DOWN':
      next.y += 1;
      break;
    case 'LEFT':
      next.x -= 1;
      break;
    case 'RIGHT':
      next.x += 1;
      break;
  }
  
  return next;
}

export function wrapPosition(position: Position): Position {
  return {
    x: (position.x + GRID_SIZE) % GRID_SIZE,
    y: (position.y + GRID_SIZE) % GRID_SIZE,
  };
}

export function isOutOfBounds(position: Position): boolean {
  return (
    position.x < 0 ||
    position.x >= GRID_SIZE ||
    position.y < 0 ||
    position.y >= GRID_SIZE
  );
}

export function checkSelfCollision(head: Position, body: Position[]): boolean {
  return body.some(segment => segment.x === head.x && segment.y === head.y);
}

export function moveSnake(state: GameState, mode: GameMode): GameState {
  if (state.gameOver || state.paused) return state;

  const head = state.snake[0];
  let nextHead = getNextHeadPosition(head, state.direction);

  // Handle wall collision based on mode
  if (mode === 'pass-through') {
    nextHead = wrapPosition(nextHead);
  } else if (isOutOfBounds(nextHead)) {
    return { ...state, gameOver: true };
  }

  // Check self-collision
  if (checkSelfCollision(nextHead, state.snake)) {
    return { ...state, gameOver: true };
  }

  const newSnake = [nextHead, ...state.snake];
  let newFood = state.food;
  let newScore = state.score;

  // Check if food is eaten
  if (nextHead.x === state.food.x && nextHead.y === state.food.y) {
    newFood = generateFood(newSnake);
    newScore += 10;
  } else {
    newSnake.pop(); // Remove tail if no food eaten
  }

  return {
    ...state,
    snake: newSnake,
    food: newFood,
    score: newScore,
  };
}

export function changeDirection(currentDirection: Direction, newDirection: Direction): Direction {
  // Prevent reversing direction
  const opposites: Record<Direction, Direction> = {
    UP: 'DOWN',
    DOWN: 'UP',
    LEFT: 'RIGHT',
    RIGHT: 'LEFT',
  };

  if (opposites[currentDirection] === newDirection) {
    return currentDirection;
  }

  return newDirection;
}

export function getGameSpeed(score: number): number {
  // Speed increases as score increases
  const speedIncrease = Math.floor(score / 50);
  return Math.max(50, INITIAL_SPEED - speedIncrease * 10);
}
