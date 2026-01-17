# Quick Start Guide - AI-Assisted Developer Productivity Platform

## Prerequisites

- Docker and docker-compose OR
- Python 3.11+ and Node.js 20+

## Option 1: Docker (Recommended)

```bash
# 1. Clone repository
git clone https://github.com/nathadriele/ai-dev-platform.git
cd ai-dev-platform

# 2. Configure environment
cp .env.example .env
nano .env  # Edit with your settings

# 3. Start all services
docker-compose up -d

# 4. Access the application
# Frontend: http://localhost:80
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
# n8n: http://localhost:5678

# 5. Create user account
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "myuser",
    "password": "MyPass123!",
    "full_name": "My Name"
  }'
```

## Option 2: Local Development

### Backend Setup

```bash
cd backend

# Virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure
cp .env.example .env
nano .env  # Set DATABASE_URL and SECRET_KEY

# Migrations
alembic upgrade head

# Seed data (optional)
python scripts/seed.py

# Run server
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure
cp .env.example .env

# Run dev server
npm run dev
```

## Testing

```bash
# Backend tests
cd backend
pytest tests/ -v --cov=app

# Frontend tests
cd frontend
npm test
```

## MCP Servers (Optional)

```bash
# Terminal 1: Filesystem MCP Server
python mcp-workflows/filesystem/mcp_server.py

# Terminal 2: GitHub MCP Server
python mcp-workflows/github/mcp_server.py
```

## Common Issues

### Database connection error
- Verify `DATABASE_URL` in .env
- For SQLite: Ensure file path is writable
- For PostgreSQL: Verify server is running

### Port already in use
- Change ports in docker-compose.yml or .env files

### Import errors
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`

## Next Steps

1. Explore the API documentation at `/docs`
2. Create your first project
3. Log AI activities
4. Try the code agents
5. Set up GitHub webhooks
6. Configure n8n workflows

## Support

For detailed documentation:
- Architecture: `ARCHITECTURE.md`
- AI Tools: `docs/AI_DOCUMENTATION.md`
- Deployment: `docs/DEPLOYMENT.md`
- Agents: `AGENTS.md`
- Implementations: `IMPLEMENTATIONS_REPORT.md`
