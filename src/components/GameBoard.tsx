import { useEffect, useRef } from 'react';
import { GameState, GRID_SIZE } from '@/lib/gameLogic';

interface GameBoardProps {
  gameState: GameState;
  cellSize?: number;
}

export const GameBoard = ({ gameState, cellSize = 20 }: GameBoardProps) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Clear canvas
    ctx.fillStyle = 'hsl(240, 5%, 10%)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Draw grid
    ctx.strokeStyle = 'hsl(240, 5%, 15%)';
    ctx.lineWidth = 1;
    for (let i = 0; i <= GRID_SIZE; i++) {
      ctx.beginPath();
      ctx.moveTo(i * cellSize, 0);
      ctx.lineTo(i * cellSize, GRID_SIZE * cellSize);
      ctx.stroke();

      ctx.beginPath();
      ctx.moveTo(0, i * cellSize);
      ctx.lineTo(GRID_SIZE * cellSize, i * cellSize);
      ctx.stroke();
    }

    // Draw snake
    gameState.snake.forEach((segment, index) => {
      const isHead = index === 0;
      
      // Snake body gradient
      const gradient = ctx.createRadialGradient(
        segment.x * cellSize + cellSize / 2,
        segment.y * cellSize + cellSize / 2,
        0,
        segment.x * cellSize + cellSize / 2,
        segment.y * cellSize + cellSize / 2,
        cellSize / 2
      );
      
      if (isHead) {
        gradient.addColorStop(0, 'hsl(142, 76%, 50%)');
        gradient.addColorStop(1, 'hsl(142, 76%, 36%)');
      } else {
        const alpha = 1 - (index / gameState.snake.length) * 0.3;
        gradient.addColorStop(0, `hsl(142, 76%, ${40 - index * 2}%, ${alpha})`);
        gradient.addColorStop(1, `hsl(142, 76%, ${30 - index * 2}%, ${alpha})`);
      }

      ctx.fillStyle = gradient;
      ctx.fillRect(
        segment.x * cellSize + 1,
        segment.y * cellSize + 1,
        cellSize - 2,
        cellSize - 2
      );

      // Add glow effect to head
      if (isHead) {
        ctx.shadowBlur = 15;
        ctx.shadowColor = 'hsl(142, 76%, 36%)';
        ctx.fillRect(
          segment.x * cellSize + 1,
          segment.y * cellSize + 1,
          cellSize - 2,
          cellSize - 2
        );
        ctx.shadowBlur = 0;
      }
    });

    // Draw food with pulsing effect
    const foodGradient = ctx.createRadialGradient(
      gameState.food.x * cellSize + cellSize / 2,
      gameState.food.y * cellSize + cellSize / 2,
      0,
      gameState.food.x * cellSize + cellSize / 2,
      gameState.food.y * cellSize + cellSize / 2,
      cellSize / 2
    );
    
    foodGradient.addColorStop(0, 'hsl(330, 100%, 60%)');
    foodGradient.addColorStop(1, 'hsl(330, 100%, 50%)');

    ctx.fillStyle = foodGradient;
    ctx.shadowBlur = 20;
    ctx.shadowColor = 'hsl(330, 100%, 50%)';
    
    ctx.beginPath();
    ctx.arc(
      gameState.food.x * cellSize + cellSize / 2,
      gameState.food.y * cellSize + cellSize / 2,
      cellSize / 2 - 2,
      0,
      Math.PI * 2
    );
    ctx.fill();
    ctx.shadowBlur = 0;
  }, [gameState, cellSize]);

  return (
    <div className="relative">
      <canvas
        ref={canvasRef}
        width={GRID_SIZE * cellSize}
        height={GRID_SIZE * cellSize}
        className="border-2 border-primary rounded neon-border"
      />
      {gameState.gameOver && (
        <div className="absolute inset-0 flex items-center justify-center bg-background/80 backdrop-blur-sm">
          <div className="text-center">
            <p className="text-4xl font-bold text-destructive neon-text mb-2">GAME OVER</p>
            <p className="text-2xl text-primary">Score: {gameState.score}</p>
          </div>
        </div>
      )}
      {gameState.paused && !gameState.gameOver && (
        <div className="absolute inset-0 flex items-center justify-center bg-background/60 backdrop-blur-sm">
          <p className="text-3xl font-bold text-secondary neon-text">PAUSED</p>
        </div>
      )}
    </div>
  );
};
