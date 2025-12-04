# Backend Dockerfile
FROM python:3.12-slim AS builder

# Install uv globally
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml ./
# Copy lock file if it exists
COPY uv.lock* ./

# Install dependencies
RUN uv sync --frozen --no-dev || uv sync --no-dev

# Runtime stage
FROM python:3.12-slim

# Install uv in runtime stage too
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY app ./app
COPY pyproject.toml ./

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Set PATH to use virtual environment
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app"

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
