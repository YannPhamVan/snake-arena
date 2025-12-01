import { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { GameBoard } from '@/components/GameBoard';
import { Button } from '@/components/ui/button';
import { ArrowLeft, RotateCcw } from 'lucide-react';
import { toast } from 'sonner';
import { mockBackend } from '@/lib/mockBackend';
import {
  GameState,
  GameMode,
  Direction,
  createInitialGameState,
  moveSnake,
  changeDirection,
  getGameSpeed,
} from '@/lib/gameLogic';

const Game = () => {
  const { mode } = useParams<{ mode: GameMode }>();
  const navigate = useNavigate();
  const [gameState, setGameState] = useState<GameState>(createInitialGameState());
  const [sessionId, setSessionId] = useState<string | null>(null);

  useEffect(() => {
    const user = mockBackend.getCurrentUser();
    if (!user) {
      toast.error('Please login to play');
      navigate('/');
      return;
    }

    // Create game session
    mockBackend.createSession(mode as GameMode).then((session) => {
      setSessionId(session.id);
    });
  }, [mode, navigate]);

  useEffect(() => {
    if (gameState.gameOver || gameState.paused) return;

    const speed = getGameSpeed(gameState.score);
    const intervalId = setInterval(() => {
      setGameState((prev) => {
        const newState = moveSnake(prev, mode as GameMode);
        
        // Update session score
        if (sessionId && newState.score !== prev.score) {
          mockBackend.updateSession(sessionId, newState.score);
        }
        
        return newState;
      });
    }, speed);

    return () => clearInterval(intervalId);
  }, [gameState.gameOver, gameState.paused, gameState.score, mode, sessionId]);

  const handleKeyPress = useCallback((e: KeyboardEvent) => {
    if (gameState.gameOver) return;

    if (e.code === 'Space') {
      e.preventDefault();
      setGameState((prev) => ({ ...prev, paused: !prev.paused }));
      return;
    }

    if (gameState.paused) return;

    const keyMap: Record<string, Direction> = {
      ArrowUp: 'UP',
      ArrowDown: 'DOWN',
      ArrowLeft: 'LEFT',
      ArrowRight: 'RIGHT',
      KeyW: 'UP',
      KeyS: 'DOWN',
      KeyA: 'LEFT',
      KeyD: 'RIGHT',
    };

    const newDirection = keyMap[e.code];
    if (newDirection) {
      e.preventDefault();
      setGameState((prev) => ({
        ...prev,
        direction: changeDirection(prev.direction, newDirection),
      }));
    }
  }, [gameState.gameOver, gameState.paused]);

  useEffect(() => {
    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [handleKeyPress]);

  useEffect(() => {
    if (gameState.gameOver && sessionId) {
      // Submit score and end session
      mockBackend.endSession(sessionId);
      mockBackend.submitScore(gameState.score, mode as GameMode);
      toast.success(`Game Over! Final Score: ${gameState.score}`);
    }
  }, [gameState.gameOver, gameState.score, mode, sessionId]);

  const handleRestart = () => {
    setGameState(createInitialGameState());
    if (sessionId) {
      mockBackend.endSession(sessionId);
    }
    mockBackend.createSession(mode as GameMode).then((session) => {
      setSessionId(session.id);
    });
  };

  const handleBack = () => {
    if (sessionId) {
      mockBackend.endSession(sessionId);
    }
    navigate('/');
  };

  return (
    <div className="min-h-screen bg-background p-4 md:p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-6 flex items-center justify-between">
          <Button
            onClick={handleBack}
            variant="outline"
            className="border-primary text-primary hover:bg-primary hover:text-primary-foreground"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back
          </Button>
          <div className="text-center">
            <h2 className="text-2xl font-bold text-primary neon-text uppercase">
              {mode === 'walls' ? 'Walls Mode' : 'Pass-Through Mode'}
            </h2>
            <p className="text-muted-foreground text-sm mt-1">
              {mode === 'walls' ? 'Avoid the walls!' : 'Wrap around edges'}
            </p>
          </div>
          <Button
            onClick={handleRestart}
            variant="outline"
            className="border-secondary text-secondary hover:bg-secondary hover:text-secondary-foreground"
          >
            <RotateCcw className="w-4 h-4 mr-2" />
            Restart
          </Button>
        </div>

        {/* Score Display */}
        <div className="mb-6 text-center">
          <div className="inline-block bg-card border-2 border-primary rounded-lg px-8 py-4">
            <p className="text-sm text-muted-foreground mb-1">SCORE</p>
            <p className="text-4xl font-bold text-primary neon-text">{gameState.score}</p>
          </div>
        </div>

        {/* Game Board */}
        <div className="flex justify-center">
          <GameBoard gameState={gameState} />
        </div>

        {/* Controls Info */}
        <div className="mt-6 text-center text-muted-foreground text-sm">
          <p>Arrow Keys or WASD to move</p>
          <p className="mt-1">SPACE to pause</p>
        </div>
      </div>
    </div>
  );
};

export default Game;
