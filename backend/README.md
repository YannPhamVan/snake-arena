# Snake Arena Backend

FastAPI backend for the Snake Arena game.

## Setup

Dependencies are managed with `uv`. To install:

```bash
uv sync
```

## Running the Server

Start the development server with auto-reload:

```bash
uv run uvicorn app.main:app --reload
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive docs**: http://localhost:8000/docs
- **Alternative docs**: http://localhost:8000/redoc

## Test Credentials

All mock users use the same password: `password123`

Example users:
- **Email**: `snake@example.com` (SnakeMaster)
- **Email**: `grid@example.com` (GridWarrior)
- **Email**: `neon@example.com` (NeonViper)

## Running Tests

```bash
uv run pytest
```

For verbose output:

```bash
uv run pytest -v
```

## API Endpoints

See `openapi.yaml` in the project root for full API specification.

### Authentication
- `POST /auth/signup` - Register new user
- `POST /auth/login` - Login user
- `POST /auth/logout` - Logout user
- `GET /auth/me` - Get current user

### Leaderboard
- `GET /leaderboard/` - Get leaderboard entries
- `POST /leaderboard/` - Submit score

### Sessions
- `GET /sessions/` - Get active sessions
- `POST /sessions/` - Create new session
- `GET /sessions/{id}` - Get session by ID
- `PUT /sessions/{id}` - Update session score
- `DELETE /sessions/{id}` - End session
