.PHONY: install run test test-integration test-all clean init-db seed-db

install:
	uv sync

init-db:
	uv run python -m app.init_db

seed-db:
	uv run python -m app.init_db --seed

run:
	uv run uvicorn app.main:app --reload --port 8000

test:
	uv run pytest tests/ -v

test-integration:
	uv run pytest tests_integration/ -v

test-all:
	uv run pytest tests/ tests_integration/ -v

clean:
	rm -rf .venv
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -f *.db
