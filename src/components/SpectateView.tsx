import { useEffect, useState } from 'react';
import { mockBackend, GameSession } from '@/lib/mockBackend';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Eye } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export const SpectateView = () => {
  const [sessions, setSessions] = useState<GameSession[]>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    loadActiveSessions();
    
    // Refresh sessions every 5 seconds
    const interval = setInterval(loadActiveSessions, 5000);
    return () => clearInterval(interval);
  }, []);

  const loadActiveSessions = async () => {
    const data = await mockBackend.getActiveSessions();
    setSessions(data);
    setLoading(false);
  };

  const handleSpectate = (sessionId: string) => {
    navigate(`/spectate/${sessionId}`);
  };

  return (
    <Card className="bg-card border-2 border-secondary">
      <CardHeader>
        <CardTitle className="text-2xl font-bold text-secondary neon-text flex items-center gap-2">
          <Eye className="w-6 h-6" />
          LIVE GAMES
        </CardTitle>
      </CardHeader>
      <CardContent>
        {loading ? (
          <div className="text-center text-muted-foreground py-8">Loading...</div>
        ) : sessions.length === 0 ? (
          <div className="text-center text-muted-foreground py-8">
            No active games at the moment
          </div>
        ) : (
          <div className="space-y-3">
            {sessions.map((session) => (
              <div
                key={session.id}
                className="flex items-center justify-between p-4 bg-muted rounded border border-border hover:border-secondary transition-colors"
              >
                <div>
                  <p className="font-bold text-foreground text-lg">{session.username}</p>
                  <div className="flex gap-4 text-sm text-muted-foreground mt-1">
                    <span className="uppercase">{session.mode}</span>
                    <span className="text-primary font-bold">Score: {session.score}</span>
                  </div>
                </div>
                <Button
                  onClick={() => handleSpectate(session.id)}
                  className="bg-secondary text-secondary-foreground hover:bg-secondary/90 neon-border"
                >
                  <Eye className="w-4 h-4 mr-2" />
                  Watch
                </Button>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
};
