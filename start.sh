#!/bin/sh
set -e

# Initialize/Seed database
echo "Initializing database..."
uv run python -m app.init_db --seed

# Start the server
# Use PORT environment variable if available, otherwise default to 8000
PORT=${PORT:-8000}
echo "Starting server on port $PORT..."
exec uvicorn app.main:app --host 0.0.0.0 --port "$PORT"
