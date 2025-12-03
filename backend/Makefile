.PHONY: install run test clean

install:
	uv sync

run:
	uv run uvicorn app.main:app --reload --port 8000

test:
	uv run pytest

clean:
	rm -rf .venv
	find . -type d -name "__pycache__" -exec rm -rf {} +
