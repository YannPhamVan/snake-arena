# Neon Snake 🐍

A retro-futuristic Snake game with a cyberpunk aesthetic, featuring two game modes, multiplayer preparation, and comprehensive test coverage.

## Features

### 🎮 Game Modes
- **Walls Mode**: Classic gameplay where hitting walls ends the game
- **Pass-Through Mode**: Snake wraps around edges for continuous play

### 👥 Multiplayer Ready
- User authentication (login/signup)
- Global leaderboard with mode-specific rankings
- Spectate mode to watch other players (with AI-simulated gameplay)
- Real-time session tracking

### 🎨 Design
- Retro-futuristic neon aesthetic
- Smooth animations and glow effects
- Responsive grid-based gameplay
- Dark cyberpunk theme with bright accents

### 🧪 Testing
Comprehensive test coverage for:
- Game logic (movement, collision detection, scoring)
- Mock backend service (auth, leaderboard, sessions)
- AI player behavior

## Running Tests

```bash
npm run test        # Run tests once
npm run test:ui     # Run tests with UI
npm run test:watch  # Run tests in watch mode
```

## Game Controls

- **Arrow Keys** or **WASD**: Move snake
- **Space**: Pause/Resume game

## Architecture

### Centralized Backend (Mocked)
All backend calls are centralized in `src/lib/mockBackend.ts`:
- Authentication: `login()`, `signup()`, `logout()`
- Leaderboard: `getLeaderboard()`, `submitScore()`
- Sessions: `createSession()`, `getActiveSessions()`, `updateSession()`

### Game Logic
Core game mechanics in `src/lib/gameLogic.ts`:
- Snake movement and collision detection
- Food generation
- Mode-specific behavior (walls vs pass-through)
- Dynamic difficulty (speed increases with score)

### AI Player
Intelligent AI for spectate mode in `src/lib/aiPlayer.ts`:
- Pathfinding towards food
- Collision avoidance
- Mode-aware behavior

## Project Structure

```
src/
├── components/
│   ├── GameBoard.tsx       # Canvas-based game renderer
│   ├── AuthDialog.tsx      # Login/signup modal
│   ├── Leaderboard.tsx     # Score rankings
│   └── SpectateView.tsx    # Live games viewer
├── lib/
│   ├── mockBackend.ts      # Centralized mock API
│   ├── gameLogic.ts        # Core game mechanics
│   ├── aiPlayer.ts         # AI for spectate mode
│   └── __tests__/          # Comprehensive tests
├── pages/
│   ├── Index.tsx           # Home/menu page
│   ├── Game.tsx            # Active gameplay
│   └── Spectate.tsx        # Watch mode
└── index.css               # Design system tokens
```

## Design System

All colors and styles are defined using semantic HSL tokens:
- `--primary`: Neon green (#00ff41)
- `--secondary`: Electric blue
- `--accent`: Magenta/pink
- `--background`: Deep dark
- Custom glow effects and animations

## How to Play

1. Sign up or log in to track your scores
2. Choose your mode (Walls or Pass-Through)
3. Control the snake with arrow keys
4. Eat food to grow and increase your score
5. Avoid collisions with yourself (and walls in Walls mode)
6. Compete for the top spot on the leaderboard!

## Future Enhancements (Backend Integration)

When connecting to a real backend:
- Replace `mockBackend` calls with actual API endpoints
- Implement WebSocket for real-time multiplayer
- Add user profiles and avatars
- Enable actual spectating of live games
- Store game replays

## Development

```bash
npm install
npm run dev
```

Visit http://localhost:8080 to play!

## Technologies

- React + TypeScript
- Vite
- Tailwind CSS
- Vitest + Testing Library
- Canvas API for rendering
- React Router for navigation
