# Docker Setup Guide

## Quick Start

Start the entire application stack with one command:

```bash
docker-compose up -d
```

Access the application:
- **Frontend**: http://localhost:8080
- **Backend API**: http://localhost:8080/api
- **Backend Direct**: http://localhost:8000 (if needed)

## Prerequisites

- Docker Engine 20.10+
- Docker Compose V2+

## Services

### Frontend (nginx)
- **Port**: 80
- **Image**: Built from `./frontend/Docker file`
- **Technology**: React + Vite, served by nginx
- **Features**:
  - Static file serving with caching
  - Gzip compression  
  - API proxy to backend at `/api/*`
  - SPA fallback routing

### Backend (FastAPI)
- **Port**: 8000 (internal to Docker network)
- **Image**: Built from `./backend/Dockerfile`
- **Technology**: Python 3.12 + FastAPI + SQLAlchemy
- **Features**:
  - Automatic database initialization with seed data
  - Health checks
  - PostgreSQL connection

### Database (PostgreSQL)
- **Port**: 5432 (internal)
- **Image**: postgres:16-alpine
- **Features**:
  - Persistent data volume
  - Health checks
  - Automatic initialization

## Commands

### Build and Start

```bash
# Build all images
docker-compose build

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f backend
```

### Stop and Cleanup

```bash
# Stop services
docker-compose stop

# Stop and remove containers
docker-compose down

# Remove containers and volumes (WARNING: deletes all data)
docker-compose down -v
```

### Database Operations

```bash
# Connect to PostgreSQL
docker-compose exec db psql -U snakearena -d snakearena

# Re-seed database
docker-compose exec backend uv run python -m app.init_db --seed

# View database logs
docker-compose logs db
```

### Rebuild Services

```bash
# Rebuild specific service
docker-compose build backend

# Rebuild and restart
docker-compose up -d --build backend
```

## Environment Variables

Create a `.env.docker` file (optional) to customize:

```bash
# Copy example
cp .env.docker.example .env.docker

# Edit as needed
nano .env.docker
```

### Available Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | (default) | JWT secret key for backend |
| `POSTGRES_DB` | snakearena | Database name |
| `POSTGRES_USER` | snakearena | Database user |
| `POSTGRES_PASSWORD` | snakearena | Database password |

## Health Checks

All services include health checks:

```bash
# Check service health
docker-compose ps
```

Healthy services show "healthy" in the STATUS column.

## Troubleshooting

### Services Not Starting

```bash
# Check logs
docker-compose logs

# Restart services
docker-compose restart
```

### Database Connection Issues

```bash
# Check database is healthy
docker-compose ps db

# View database logs
docker-compose logs db

# Restart database
docker-compose restart db
```

### Frontend Not Loading

```bash
# Check nginx logs
docker-compose logs frontend

# Rebuild frontend
docker-compose build frontend
docker-compose up -d frontend
```

### Clear Everything and Start Fresh

```bash
# Stop and remove all containers, networks, and volumes
docker-compose down -v

# Rebuild and start
docker-compose build
docker-compose up -d
```

## Development

### Hot Reload (Optional)

For development with hot reload, use volume mounts:

```yaml
# Create docker-compose.override.yml
services:
  backend:
    volumes:
      - ./backend/app:/app/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Accessing Services Directly

- Backend: `http://localhost:8000` (add port mapping to docker-compose.yml)
- Database: `localhost:5432` (add port mapping to docker-compose.yml)

## Production Deployment

### Security Checklist

- [ ] Change default PostgreSQL password
- [ ] Generate strong SECRET_KEY
- [ ] Use environment variables for secrets
- [ ] Enable HTTPS (add reverse proxy)
- [ ] Configure firewall rules
- [ ] Set up automated backups

### Recommended Changes

1. **Use secrets management**:
   ```bash
   docker secret create db_password -
   ```

2. **Enable HTTPS** (add Caddy or Traefik)

3. **Configure backups**:
   ```bash
   docker-compose exec db pg_dump -U snakearena snakearena > backup.sql
   ```

4. **Monitor logs**:
   ```bash
   docker-compose logs -f --tail=100
   ```

## Architecture

```
┌─────────────────┐
│   Port 80       │
│   Frontend      │──┐
│   (nginx)       │  │
└─────────────────┘  │
                     │
              ┌──────▼──────┐      ┌─────────────┐
              │  Backend    │─────▶│  PostgreSQL │
              │  (FastAPI)  │      │  Database   │
              │  Port 8000  │      │  Port 5432  │
              └─────────────┘      └─────────────┘
                     │                     │
                     └─────────────────────┘
                        snake-arena-network
```

## File Structure

```
snake-arena/
├── docker-compose.yml       # Main compose configuration
├── .env.docker.example      # Environment template
├── frontend/
│   ├── Dockerfile          # Frontend image
│   ├── nginx.conf          # nginx configuration
│   └── .dockerignore       # Build exclusions
└── backend/
    ├── Dockerfile          # Backend image
    └── .dockerignore       # Build exclusions
```

## Additional Resources

- [Docker Documentation](https://docs.docker.com)
- [Docker Compose Documentation](https://docs.docker.com/compose)
- [nginx Documentation](https://nginx.org/en/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs)

## Unified Container Deployment

For simplified deployment, you can use the single-container approach which bundles the Frontend and Backend together.

### Build and Run

```bash
# Build the unified image
docker build -t snake-arena-unified -f Dockerfile .

# Run locally (requires external DB or link to db container)
docker run -p 8080:8000 --env-file .env.docker snake-arena-unified
```

### Testing via Docker Compose

We have added a `unified` service to `docker-compose.yml` for testing:

```bash
docker-compose up -d unified
# Access at http://localhost:8081
```

The unified container serves:
- Frontend at root `/`
- API at `/api`
