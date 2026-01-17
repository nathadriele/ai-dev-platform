# Deployment Guide

This document provides comprehensive instructions for deploying the AI-Assisted Developer Productivity Platform to various cloud platforms.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Variables](#environment-variables)
3. [Deployment Options](#deployment-options)
   - [Render](#render)
   - [Railway](#railway)
   - [DigitalOcean App Platform](#digitalocean-app-platform)
   - [AWS ECS](#aws-ecs)
4. [Database Setup](#database-setup)
5. [Monitoring and Logging](#monitoring-and-logging)
6. [Troubleshooting](#troubleshooting)

## Prerequisites

Before deploying, ensure you have:

- A cloud platform account (Render, Railway, DigitalOcean, or AWS)
- Docker installed locally
- Git repository with the application code
- Domain name (optional, for custom domains)

## Environment Variables

### Backend Environment Variables

```bash
APP_NAME="AI-Assisted Developer Productivity Platform"
APP_VERSION="1.0.0"
DEBUG=false
ENVIRONMENT="production"

DATABASE_URL="postgresql+asyncpg://user:password@host:5432/dbname"

SECRET_KEY="your-production-secret-key-min-32-characters-long"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

CORS_ORIGINS=["https://your-domain.com"]

OPENAI_API_KEY="sk-..."
ANTHROPIC_API_KEY="sk-ant-..."
GITHUB_TOKEN="ghp_..."

MCP_GITHUB_ENDPOINT="https://..."
MCP_FILESYSTEM_ENDPOINT="https://..."
MCP_DATABASE_ENDPOINT="https://..."

LOG_LEVEL="INFO"
LOG_FORMAT="json"

RATE_LIMIT_PER_MINUTE=100
```

### Frontend Environment Variables

```bash
VITE_API_BASE_URL=https://your-backend-api.com/api/v1
VITE_APP_NAME="AI-Assisted Developer Productivity Platform"
VITE_APP_VERSION="1.0.0"
```

## Deployment Options

### Render

Render offers a straightforward deployment process with a generous free tier.

#### Backend Deployment (Render)

1. **Create a new Web Service**
   - Go to [render.com](https://render.com)
   - Click "New" -> "Web Service"
   - Connect your GitHub repository

2. **Configure the service**
   - **Name**: ai-dev-backend
   - **Environment**: Python 3
   - **Build Command**: `cd backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: Free (or Standard for production)

3. **Add Environment Variables**
   - Add all backend environment variables from the list above
   - **Important**: Set `DATABASE_URL` after creating the database

4. **Create PostgreSQL Database**
   - Click "New" -> "PostgreSQL"
   - Name: ai-dev-db
   - Database: ai_dev_platform
   - User: auto-generated
   - Copy the internal database URL to `DATABASE_URL` environment variable

#### Frontend Deployment (Render)

1. **Create a new Static Site**
   - Click "New" -> "Static Site"
   - Connect your GitHub repository

2. **Configure the site**
   - **Name**: ai-dev-frontend
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Publish Directory**: `frontend/dist`
   - **Add Environment Variable**: `VITE_API_BASE_URL=https://ai-dev-backend.onrender.com/api/v1`

#### Automated Deployments

Render automatically deploys when you push to the connected branch (usually `main`).

### Railway

Railway provides excellent developer experience with automatic deployments.

1. **Create a new project**
   - Go to [railway.app](https://railway.app)
   - Click "New Project"
   - Deploy from GitHub repo

2. **Add services**
   - Click "Add Service" -> "Deploy from GitHub repo"
   - Add backend service first, then frontend

3. **Configure each service**

   **Backend:**
   - Root directory: `backend`
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Add environment variables

   **Frontend:**
   - Root directory: `frontend`
   - Build command: `npm install && npm run build`
   - Start command: `npm run preview` (or use Static Site deployment)

4. **Add PostgreSQL**
   - Click "Add Service" -> "Database" -> "Add PostgreSQL"
   - Railway automatically provides `DATABASE_URL`

5. **Connect services**
   - Railway automatically creates connections between services

### DigitalOcean App Platform

1. **Create a new app**
   - Go to DigitalOcean Control Panel
   - Apps -> Create App
   - Connect GitHub repository

2. **Configure components**

   **Backend Component:**
   - Name: backend
   - Build command: `cd backend && pip install -r requirements.txt`
   - Run command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - HTTP port: 8000

   **Frontend Component:**
   - Name: frontend
   - Build command: `cd frontend && npm install && npm run build`
   - Output directory: `/frontend/dist`
   - Route: `/`

3. **Add database**
   - Add "Dev Database" or "Production Database" (PostgreSQL)
   - Configure connection in backend environment variables

4. **Deploy**
   - Click "Create Resources"
   - App will be live at provided URL

### AWS ECS

For enterprise-grade deployments, use Amazon ECS.

1. **Push Docker images to ECR**
   ```bash
   aws ecr create-repository --repository-name ai-dev-backend
   aws ecr create-repository --repository-name ai-dev-frontend

   docker build -t ai-dev-backend ./backend
   docker tag ai-dev-backend:latest <ACCOUNT-ID>.dkr.ecr.<REGION>.amazonaws.com/ai-dev-backend:latest
   docker push <ACCOUNT-ID>.dkr.ecr.<REGION>.amazonaws.com/ai-dev-backend:latest
   ```

2. **Create ECS Cluster**
   - Go to ECS console
   - Create cluster: "ai-dev-cluster"
   - Use Fargate (serverless) or EC2 launch type

3. **Create Task Definitions**

   **Backend Task:**
   - Image: ECR backend image
   - CPU: 512
   - Memory: 1024
   - Port: 8000
   - Environment variables: Add all required variables

   **Frontend Task:**
   - Image: ECR frontend image
   - CPU: 256
   - Memory: 512
   - Port: 80

4. **Create Services**
   - Backend service with load balancer
   - Frontend service with load balancer

5. **Configure RDS PostgreSQL**
   - Create RDS PostgreSQL instance
   - Set `DATABASE_URL` to RDS connection string

6. **Set up ALB**
   - Application Load Balancer with SSL certificates
   - Route frontend requests to frontend service
   - Route API requests to backend service

## Database Setup

### Production Database (PostgreSQL)

1. **Create database**
   - Use cloud provider's managed PostgreSQL service
   - Or use Amazon RDS, Google Cloud SQL, Azure Database

2. **Run migrations**
   ```bash
   # SSH into backend container or use cloud shell
   cd backend
   alembic upgrade head
   ```

3. **Create initial data** (optional)
   - Create admin user
   - Seed with sample data if needed

## Monitoring and Logging

### Health Checks

Configure health check endpoints:

```bash
# Backend health
https://your-backend.com/api/v1/health

# Readiness check
https://your-backend.com/api/v1/health/ready
```

### Logging

- **Backend**: Structured JSON logging (configured in `app/main.py`)
- **Frontend**: Console logging (in production, consider using a logging service)

### Monitoring Services

- **Sentry**: Error tracking
- **Datadog**: Infrastructure monitoring
- **New Relic**: Application performance monitoring
- **LogRocket**: Frontend session replay

## Troubleshooting

### Common Issues

1. **Database connection errors**
   - Verify `DATABASE_URL` is correct
   - Check database allows connections from your app IP
   - Ensure database is running and accessible

2. **CORS errors**
   - Add frontend domain to `CORS_ORIGINS`
   - Check API requests use correct base URL

3. **Build failures**
   - Check build logs in deployment platform
   - Verify all dependencies are installable
   - Ensure Dockerfile is correct

4. **Container crashes**
   - Check application logs
   - Verify all environment variables are set
   - Ensure database is accessible during startup

### Performance Optimization

1. **Enable caching**
   - Redis for session storage
   - CDN for static assets

2. **Database optimization**
   - Connection pooling
   - Read replicas for scaling
   - Regular backups

3. **Scaling**
   - Horizontal scaling: Add more containers
   - Vertical scaling: Increase container resources

### Backup Strategy

- **Database backups**: Daily automated backups
- **Code backups**: Git repository
- **Configuration backups**: Export environment variables regularly

## Security Best Practices

1. **Use secrets management**
   - Never commit secrets to git
   - Use cloud provider's secret management
   - Rotate secrets regularly

2. **Enable SSL/TLS**
   - All traffic should be HTTPS
   - Use valid certificates from Let's Encrypt or your CA

3. **Rate limiting**
   - Implement rate limiting on API endpoints
   - Use API gateway features if available

4. **Regular updates**
   - Keep dependencies updated
   - Monitor for security vulnerabilities

## Cost Estimation

### Render (Monthly)
- Free tier: $0 (limited resources)
- Standard: $7-25/month per service
- PostgreSQL: $7-50/month depending on size

### Railway (Monthly)
- Free trial: $5 credit
- Pay-as-you-go: Usage-based pricing
- Estimated: $10-50/month for small production app

### DigitalOcean (Monthly)
- Basic App Platform: $5-40/month
- Database: $15-240/month
- Total: $20-280/month

### AWS (Monthly)
- ECS Fargate: $30-100/month
- RDS PostgreSQL: $15-200/month
- Load Balancer: $18/month
- Total: $63-318/month

## Rollback Procedure

If deployment fails:

1. **Quick rollback**
   - Redeploy previous commit
   - Use platform's rollback feature

2. **Database rollback**
   - Restore from backup if schema changed
   - Run `alembic downgrade` to revert migrations

3. **Verify health checks**
   - Ensure `/health` and `/health/ready` return 200

## Continuous Deployment

The CI/CD pipeline (`.github/workflows/ci-cd.yml`) automatically:

1. Runs tests on every commit
2. Builds Docker images on main branch
3. Deploys to production (configure webhook)
4. Creates GitHub releases

Configure deployment webhook in your cloud platform to trigger on successful builds.
