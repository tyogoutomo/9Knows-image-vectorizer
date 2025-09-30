# 9Knows Image Vectorizer

A FastAPI-based service for converting images into vector embeddings using ResNet50 model, with PostgreSQL storage support.

## Features

- Image vectorization using pre-trained ResNet50 model
- RESTful API with FastAPI
- PostgreSQL database integration
- Docker containerization
- Health checks and monitoring
- Production-ready configuration

## Docker Setup

### Quick Start with Docker Compose (Recommended)

1. **Development setup:**
   ```bash
   # Build and run with database
   docker-compose up --build
   
   # Run in background
   docker-compose up -d --build
   ```

3. **Environment variables:**
   Copy `.env.example` to `.env` and modify as needed:
   ```bash
   cp .env.example .env
   ```

### Manual Docker Commands

**Build the container:**
```bash
docker build -t fastapi-vectorizer .
```

**Run the container (standalone):**
```bash
docker run -p 8000:8000 \
  -e DB_HOST=host.docker.internal \
  -e DB_NAME=n8n \
  -e DB_USER=postgres \
  -e DB_PASSWORD=n8n \
  -e DB_PORT=5432 \
  fastapi-vectorizer
```

**Run with database:**
```bash
# Start PostgreSQL first
docker run -d --name postgres \
  -e POSTGRES_DB=n8n \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=n8n \
  -p 5432:5432 \
  postgres:15-alpine

# Then start the app
docker run -p 8000:8000 \
  --link postgres:postgres \
  -e DB_HOST=postgres \
  fastapi-vectorizer
```

## API Usage

**Test the vectorizer endpoint:**
```bash
curl -X POST "http://localhost:8000/api/vectorize" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test.jpg"
```

**Health check:**
```bash
curl http://localhost:8000/
```
