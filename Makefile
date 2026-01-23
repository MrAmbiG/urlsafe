.PHONY: install run docker-up docker-down test build clean

# Install dependencies
install:
	uv sync

# Print activation command
venv:
	@echo "source .venv/bin/activate"

# Run locally
run:
	uv run uvicorn app.main:app --reload

# Run with Docker Compose
du:
	docker compose down && docker compose up --remove-orphans

# Run with Docker Compose (build)
dudb:
	docker compose down && docker compose up -d --build --remove-orphans

# Run with docker compose down
dd:
	docker compose down

# Run integration tests
test:
	uv run python tests/integration_test.py

# Build Docker image
build:
	docker build -t urlsafe .

# Clean cleanup
clean:
	rm -rf .venv
	find . -type d -name "__pycache__" -exec rm -rf {} +
