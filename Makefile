# Transcription App Makefile

.PHONY: help build up down logs clean local-setup local-backend local-frontend local-test local-test-backend local-test-frontend local-clean

# Default target
help:
	@echo "Available commands:"
	@echo "Docker commands:"
	@echo "  make build              - Build Docker images"
	@echo "  make up                 - Start all services"
	@echo "  make down               - Stop all services"
	@echo "  make logs               - View logs"
	@echo "  make clean              - Remove Docker containers and volumes"
	@echo ""
	@echo "Local development commands:"
	@echo "  make local-setup        - Setup local development environment"
	@echo "  make local-backend      - Run backend locally"
	@echo "  make local-frontend     - Run frontend locally"
	@echo "  make local-test         - Run all tests locally"
	@echo "  make local-test-backend - Run backend tests locally"
	@echo "  make local-test-frontend - Run frontend tests locally"
	@echo "  make local-clean        - Clean local development environment"

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
	mkdir -p backend/instance
	mkdir -p backend/uploads
	touch backend/instance/dev.db
	chmod 666 backend/instance/dev.db

# Run backend locally
local-backend:
	@echo "Starting backend server..."
	cd backend && \
	. venv/bin/activate && \
	FLASK_APP=app.main:create_app FLASK_ENV=development \
	python -c "import os; from app.main import create_app; from app.database import db; app = create_app('development'); app.app_context().push(); db.create_all(); print(f'Database initialized at: {app.config[\"SQLALCHEMY_DATABASE_URI\"]}')" && \
	flask --app app.main:create_app run --host=0.0.0.0 --port=8000

# Run frontend locally
local-frontend:
	@echo "Starting frontend server..."
	cd frontend && npm run dev

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

# Clean local development environment
local-clean:
	@echo "Cleaning local development environment..."
	rm -rf backend/venv
	rm -rf frontend/node_modules
	rm -f backend/instance/*.db
	rm -rf backend/uploads/*
	@echo "Local development environment cleaned successfully!" 