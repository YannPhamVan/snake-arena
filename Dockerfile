# Unified Dockerfile
# Stage 1: Build Frontend
FROM node:20-alpine AS frontend-builder
WORKDIR /app
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ .
RUN npm run build

# Stage 2: Setup Backend and Runtime
FROM python:3.12-slim

# Install uv globally
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copy dependency files
COPY backend/pyproject.toml ./
COPY backend/uv.lock* ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy application code
COPY backend/app ./app
COPY start.sh .
RUN chmod +x start.sh

# Copy built frontend assets
COPY --from=frontend-builder /app/dist /app/static

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Set PATH
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app"

# Expose port
EXPOSE 8000

# Run the application
CMD ["./start.sh"]
