# Transcription App Makefile

.PHONY: help build up down logs shell docker-test docker-test-backend docker-test-frontend clean local-setup local-backend local-frontend local-test local-test-backend local-test-frontend

# Default target
help:
	@echo "Available commands:"
	@echo "Docker commands:"
	@echo "  make build              - Build Docker images"
	@echo "  make up                 - Start all services"
	@echo "  make down               - Stop all services"
	@echo "  make logs               - View logs"
	@echo "  make shell              - Open shell in backend container"
	@echo "  make docker-test        - Run all tests in Docker"
	@echo "  make docker-test-backend - Run backend tests in Docker"
	@echo "  make docker-test-frontend - Run frontend tests in Docker"
	@echo "  make clean              - Remove Docker containers and volumes"
	@echo ""
	@echo "Local development commands:"
	@echo "  make local-setup        - Setup local development environment"
	@echo "  make local-backend      - Run backend locally"
	@echo "  make local-frontend     - Run frontend locally"
	@echo "  make local-test         - Run all tests locally"
	@echo "  make local-test-backend - Run backend tests locally"
	@echo "  make local-test-frontend - Run frontend tests locally"

# Docker commands
# ---------------

# Build Docker images
build:
	docker-compose build

# Start all services
up:
	docker-compose up -d

# Stop all services
down:
	docker-compose down

# View logs
logs:
	docker-compose logs -f

# Open shell in backend container
shell:
	docker-compose exec backend bash

# Run all tests in Docker
docker-test: docker-test-backend docker-test-frontend

# Run backend tests in Docker
docker-test-backend:
	@echo "Running backend tests in Docker..."
	docker-compose exec backend ./run_tests.sh

# Run frontend tests in Docker
docker-test-frontend:
	@echo "Running frontend tests in Docker..."
	docker-compose exec frontend npm run test

# Remove Docker containers and volumes
clean:
	docker-compose down -v
	docker system prune -f

# Local development commands
# -------------------------

# Setup local development environment
local-setup:
	@echo "Setting up local development environment..."
	cd backend && python -m venv venv && \
	. venv/bin/activate && \
	pip install -r requirements.txt
	cd frontend && npm install

# Run backend locally
local-backend:
	@echo "Starting backend server..."
	cd backend && . venv/bin/activate && \
	FLASK_APP=app.main:create_app FLASK_ENV=development flask run --host=0.0.0.0 --port=8000

# Run frontend locally
local-frontend:
	@echo "Starting frontend server..."
	cd frontend && npm start

# Run all tests locally
local-test: local-test-backend local-test-frontend

# Run backend tests locally
local-test-backend:
	@echo "Running backend tests locally..."
	cd backend && . venv/bin/activate && \
	python -m pytest

# Run frontend tests locally
local-test-frontend:
	@echo "Running frontend tests locally..."
	cd frontend && npm run test 