import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { GameBoard } from '@/components/GameBoard';
import { Button } from '@/components/ui/button';
import { ArrowLeft, Eye } from 'lucide-react';
import { mockBackend, GameSession } from '@/lib/mockBackend';
import {
  GameState,
  createInitialGameState,
  moveSnake,
  getGameSpeed,
} from '@/lib/gameLogic';
import { getAIDirection } from '@/lib/aiPlayer';

const Spectate = () => {
  const { sessionId } = useParams<{ sessionId: string }>();
  const navigate = useNavigate();
  const [gameState, setGameState] = useState<GameState>(createInitialGameState());
  const [session, setSession] = useState<GameSession | null>(null);

  useEffect(() => {
    if (!sessionId) {
      navigate('/');
      return;
    }

    mockBackend.getSession(sessionId).then((data) => {
      if (data) {
        setSession(data);
      } else {
        navigate('/');
      }
    });
  }, [sessionId, navigate]);

  useEffect(() => {
    if (!session || gameState.gameOver) return;

    const speed = getGameSpeed(gameState.score);
    const intervalId = setInterval(() => {
      setGameState((prev) => {
        // Get AI direction before moving
        const aiDirection = getAIDirection(prev, session.mode);
        const stateWithAIDirection = { ...prev, direction: aiDirection };
        
        return moveSnake(stateWithAIDirection, session.mode);
      });
    }, speed);

    return () => clearInterval(intervalId);
  }, [gameState.gameOver, gameState.score, session]);

  const handleBack = () => {
    navigate('/');
  };

  if (!session) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <p className="text-muted-foreground">Loading...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background p-4 md:p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-6 flex items-center justify-between">
          <Button
            onClick={handleBack}
            variant="outline"
            className="border-secondary text-secondary hover:bg-secondary hover:text-secondary-foreground"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back
          </Button>
          <div className="text-center">
            <h2 className="text-2xl font-bold text-secondary neon-text flex items-center justify-center gap-2">
              <Eye className="w-6 h-6" />
              SPECTATING
            </h2>
            <p className="text-muted-foreground text-sm mt-1">{session.username}</p>
          </div>
          <div className="w-24" /> {/* Spacer for alignment */}
        </div>

        {/* Player Info */}
        <div className="mb-6 flex justify-center gap-4">
          <div className="bg-card border-2 border-secondary rounded-lg px-6 py-3">
            <p className="text-xs text-muted-foreground mb-1">PLAYER</p>
            <p className="text-lg font-bold text-foreground">{session.username}</p>
          </div>
          <div className="bg-card border-2 border-secondary rounded-lg px-6 py-3">
            <p className="text-xs text-muted-foreground mb-1">MODE</p>
            <p className="text-lg font-bold text-foreground uppercase">{session.mode}</p>
          </div>
          <div className="bg-card border-2 border-primary rounded-lg px-6 py-3">
            <p className="text-xs text-muted-foreground mb-1">SCORE</p>
            <p className="text-lg font-bold text-primary">{gameState.score}</p>
          </div>
        </div>

        {/* Game Board */}
        <div className="flex justify-center">
          <GameBoard gameState={gameState} />
        </div>

        {/* Spectate Info */}
        <div className="mt-6 text-center">
          <div className="inline-flex items-center gap-2 bg-muted/50 px-4 py-2 rounded-lg">
            <div className="w-2 h-2 bg-destructive rounded-full animate-pulse-glow" />
            <p className="text-sm text-muted-foreground">Watching live gameplay</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Spectate;
