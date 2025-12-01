import { useEffect, useState } from 'react';
import { mockBackend, LeaderboardEntry } from '@/lib/mockBackend';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Trophy, Medal, Award } from 'lucide-react';

export const Leaderboard = () => {
  const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadLeaderboard();
  }, []);

  const loadLeaderboard = async () => {
    setLoading(true);
    const data = await mockBackend.getLeaderboard(undefined, 10);
    setLeaderboard(data);
    setLoading(false);
  };

  const loadModeLeaderboard = async (mode: 'pass-through' | 'walls') => {
    setLoading(true);
    const data = await mockBackend.getLeaderboard(mode, 10);
    setLeaderboard(data);
    setLoading(false);
  };

  const getRankIcon = (index: number) => {
    switch (index) {
      case 0:
        return <Trophy className="w-6 h-6 text-accent" />;
      case 1:
        return <Medal className="w-6 h-6 text-secondary" />;
      case 2:
        return <Award className="w-6 h-6 text-primary" />;
      default:
        return <span className="text-muted-foreground font-bold w-6 text-center">{index + 1}</span>;
    }
  };

  return (
    <Card className="bg-card border-2 border-primary">
      <CardHeader>
        <CardTitle className="text-2xl font-bold text-primary neon-text">LEADERBOARD</CardTitle>
      </CardHeader>
      <CardContent>
        <Tabs defaultValue="all" onValueChange={(value) => {
          if (value === 'all') loadLeaderboard();
          else loadModeLeaderboard(value as 'pass-through' | 'walls');
        }}>
          <TabsList className="grid w-full grid-cols-3 mb-4 bg-muted">
            <TabsTrigger value="all" className="data-[state=active]:bg-primary data-[state=active]:text-primary-foreground">
              All
            </TabsTrigger>
            <TabsTrigger value="walls" className="data-[state=active]:bg-primary data-[state=active]:text-primary-foreground">
              Walls
            </TabsTrigger>
            <TabsTrigger value="pass-through" className="data-[state=active]:bg-primary data-[state=active]:text-primary-foreground">
              Pass-Through
            </TabsTrigger>
          </TabsList>
          <TabsContent value="all" className="space-y-2">
            {loading ? (
              <div className="text-center text-muted-foreground py-8">Loading...</div>
            ) : (
              leaderboard.map((entry, index) => (
                <div
                  key={entry.id}
                  className="flex items-center justify-between p-3 bg-muted rounded border border-border hover:border-primary transition-colors"
                >
                  <div className="flex items-center gap-3">
                    {getRankIcon(index)}
                    <div>
                      <p className="font-bold text-foreground">{entry.username}</p>
                      <p className="text-xs text-muted-foreground uppercase">{entry.mode}</p>
                    </div>
                  </div>
                  <p className="text-xl font-bold text-primary">{entry.score}</p>
                </div>
              ))
            )}
          </TabsContent>
          <TabsContent value="walls" className="space-y-2">
            {loading ? (
              <div className="text-center text-muted-foreground py-8">Loading...</div>
            ) : (
              leaderboard.map((entry, index) => (
                <div
                  key={entry.id}
                  className="flex items-center justify-between p-3 bg-muted rounded border border-border hover:border-primary transition-colors"
                >
                  <div className="flex items-center gap-3">
                    {getRankIcon(index)}
                    <p className="font-bold text-foreground">{entry.username}</p>
                  </div>
                  <p className="text-xl font-bold text-primary">{entry.score}</p>
                </div>
              ))
            )}
          </TabsContent>
          <TabsContent value="pass-through" className="space-y-2">
            {loading ? (
              <div className="text-center text-muted-foreground py-8">Loading...</div>
            ) : (
              leaderboard.map((entry, index) => (
                <div
                  key={entry.id}
                  className="flex items-center justify-between p-3 bg-muted rounded border border-border hover:border-primary transition-colors"
                >
                  <div className="flex items-center gap-3">
                    {getRankIcon(index)}
                    <p className="font-bold text-foreground">{entry.username}</p>
                  </div>
                  <p className="text-xl font-bold text-primary">{entry.score}</p>
                </div>
              ))
            )}
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  );
};
