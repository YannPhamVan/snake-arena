import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { AuthDialog } from '@/components/AuthDialog';
import { Leaderboard } from '@/components/Leaderboard';
import { SpectateView } from '@/components/SpectateView';
import { mockBackend, User } from '@/lib/mockBackend';
import { useNavigate } from 'react-router-dom';
import { LogOut, Play, Trophy, Eye } from 'lucide-react';

const Index = () => {
  const [user, setUser] = useState<User | null>(null);
  const [authDialogOpen, setAuthDialogOpen] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const currentUser = mockBackend.getCurrentUser();
    setUser(currentUser);
  }, []);

  const handleLogout = async () => {
    await mockBackend.logout();
    setUser(null);
  };

  const handleAuthSuccess = () => {
    const currentUser = mockBackend.getCurrentUser();
    setUser(currentUser);
  };

  const handlePlayGame = (mode: 'pass-through' | 'walls') => {
    if (!user) {
      setAuthDialogOpen(true);
      return;
    }
    navigate(`/game/${mode}`);
  };

  return (
    <div className="min-h-screen bg-background p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <header className="mb-8 flex items-center justify-between">
          <div>
            <h1 className="text-5xl md:text-6xl font-bold text-primary neon-text mb-2">
              NEON SNAKE
            </h1>
            <p className="text-muted-foreground text-sm">Classic arcade gaming reimagined</p>
          </div>
          {user ? (
            <div className="flex items-center gap-4">
              <div className="text-right">
                <p className="text-foreground font-bold">{user.username}</p>
                <p className="text-sm text-muted-foreground">High Score: {user.highScore}</p>
              </div>
              <Button
                onClick={handleLogout}
                variant="outline"
                className="border-destructive text-destructive hover:bg-destructive hover:text-destructive-foreground"
              >
                <LogOut className="w-4 h-4 mr-2" />
                Logout
              </Button>
            </div>
          ) : (
            <Button
              onClick={() => setAuthDialogOpen(true)}
              className="bg-primary text-primary-foreground hover:bg-primary/90 neon-border"
            >
              Login / Sign Up
            </Button>
          )}
        </header>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Game Modes */}
          <div className="lg:col-span-2 space-y-6">
            <div className="bg-card border-2 border-primary rounded-lg p-6">
              <h2 className="text-3xl font-bold text-primary neon-text mb-6 flex items-center gap-2">
                <Play className="w-8 h-8" />
                SELECT MODE
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <button
                  onClick={() => handlePlayGame('walls')}
                  className="group bg-muted hover:bg-muted/80 border-2 border-border hover:border-primary rounded-lg p-6 transition-all text-left"
                >
                  <h3 className="text-2xl font-bold text-primary group-hover:neon-text mb-2">
                    WALLS MODE
                  </h3>
                  <p className="text-muted-foreground mb-4">
                    Classic gameplay. Hit the wall and it's game over!
                  </p>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-destructive font-bold">HARD</span>
                    <Play className="w-5 h-5 text-primary group-hover:text-primary/80" />
                  </div>
                </button>

                <button
                  onClick={() => handlePlayGame('pass-through')}
                  className="group bg-muted hover:bg-muted/80 border-2 border-border hover:border-secondary rounded-lg p-6 transition-all text-left"
                >
                  <h3 className="text-2xl font-bold text-secondary group-hover:neon-text mb-2">
                    PASS-THROUGH MODE
                  </h3>
                  <p className="text-muted-foreground mb-4">
                    Snake wraps around edges. Infinite possibilities!
                  </p>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-primary font-bold">MEDIUM</span>
                    <Play className="w-5 h-5 text-secondary group-hover:text-secondary/80" />
                  </div>
                </button>
              </div>
            </div>

            {/* Spectate Section */}
            <SpectateView />
          </div>

          {/* Leaderboard */}
          <div className="lg:col-span-1">
            <Leaderboard />
          </div>
        </div>

        {/* Footer */}
        <footer className="mt-12 text-center text-muted-foreground text-sm">
          <p>Use arrow keys to control the snake</p>
          <p className="mt-1">Press SPACE to pause</p>
        </footer>
      </div>

      <AuthDialog
        open={authDialogOpen}
        onOpenChange={setAuthDialogOpen}
        onSuccess={handleAuthSuccess}
      />
    </div>
  );
};

export default Index;
