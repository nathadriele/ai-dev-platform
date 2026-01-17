# Architecture Documentation

## System Overview

The AI-Assisted Developer Productivity Platform is a full-stack web application designed to demonstrate and track the use of AI tools and code agents in software development workflows.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend Layer                       │
│                      (React + TypeScript)                    │
│              - User Interface                                │
│              - State Management (Redux Toolkit)              │
│              - API Client (axios/RTK Query)                  │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP/REST
┌──────────────────────▼──────────────────────────────────────┐
│                        API Gateway                           │
│                        (FastAPI)                             │
│              - OpenAPI-contract first                        │
│              - Authentication & Authorization                │
│              - Request Validation                            │
│              - Rate Limiting                                 │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                      Business Logic Layer                    │
│                      (FastAPI Services)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Project Mgmt │  │  AI Tracking │  │ Agent Orch.  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                     Data Access Layer                        │
│                    (SQLAlchemy ORM)                          │
│              - Database Models                               │
│              - Repositories                                  │
│              - Migrations                                    │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                      Database Layer                          │
│           SQLite (development)  |  PostgreSQL (prod)         │
└─────────────────────────────────────────────────────────────┘
```

## Technology Stack

### Frontend
- **React 18**: UI library with hooks and concurrent features
- **TypeScript 5**: Type-safe development
- **Vite**: Build tool and dev server
- **Redux Toolkit**: State management
- **React Router v6**: Client-side routing
- **Material UI (MUI)**: Component library for consistent UI
- **Axios**: HTTP client
- **React Query (RTK Query)**: Server state management

### Backend
- **FastAPI 0.104+**: Modern async Python web framework
- **Pydantic v2**: Data validation and serialization
- **SQLAlchemy 2.0**: ORM with async support
- **Alembic**: Database migrations
- **PostgreSQL**: Production database
- **SQLite**: Development database
- **PyJWT**: JWT authentication
- **python-multipart**: File upload support
- **uvicorn**: ASGI server

### DevOps & Infrastructure
- **Docker**: Containerization
- **docker-compose**: Multi-container orchestration
- **GitHub Actions**: CI/CD pipeline
- **nginx**: Reverse proxy (production)
- **Render/Railway/Vercel**: Cloud deployment platform

### AI & Automation
- **OpenAI API / Anthropic API**: LLM integration
- **Model-Context Protocol (MCP)**: Tool integration layer
- **n8n**: Low-code automation platform
- **GitHub Copilot/Cursor**: AI-assisted development

## Core Components

### 1. Project Management Module
Manages software projects tracked in the platform:
- Project CRUD operations
- Team member management
- Project metadata and configuration
- Integration status tracking

### 2. AI Activity Tracking Module
Tracks all AI interactions during development:
- Prompts sent to AI tools
- Responses received
- Code changes suggested by AI
- Decision documentation
- Cost and usage metrics

### 3. Agent Orchestration Module
Manages code agents and their execution:
- Agent lifecycle management
- Task queue and execution
- Result logging and verification
- Performance tracking

### 4. CI/CD Integration Module
Connects to CI/CD pipelines:
- Pipeline status monitoring
- Test result aggregation
- Deployment history
- Quality gate enforcement

### 5. Automation Module (n8n)
Provides workflow automation:
- Auto-generation of technical posts
- Resume adaptation for job postings
- Report generation
- Notification workflows

## Data Model

### Core Entities

#### Project
```typescript
{
  id: string
  name: string
  description: string
  repository_url: string
  tech_stack: string[]
  created_at: timestamp
  updated_at: timestamp
  status: 'active' | 'archived'
}
```

#### AIActivity
```typescript
{
  id: string
  project_id: string
  tool_used: 'chatgpt' | 'claude' | 'copilot' | 'cursor'
  prompt: string
  response: string
  code_changes: string[]
  timestamp: timestamp
  user_id: string
  category: 'feature' | 'bugfix' | 'refactor' | 'docs' | 'test'
}
```

#### AgentExecution
```typescript
{
  id: string
  project_id: string
  agent_type: string
  task_description: string
  status: 'pending' | 'running' | 'completed' | 'failed'
  input_data: object
  output_data: object
  started_at: timestamp
  completed_at: timestamp
  error_message?: string
}
```

#### PipelineExecution
```typescript
{
  id: string
  project_id: string
  pipeline_name: string
  status: 'running' | 'success' | 'failed'
  commit_sha: string
  branch: string
  triggered_by: string
  started_at: timestamp
  completed_at: timestamp
  test_results: object
  deployment_url?: string
}
```

## Security Architecture

### Authentication
- JWT-based authentication
- Refresh token rotation
- Token expiration: 15 minutes (access), 7 days (refresh)
- Secure token storage (httpOnly cookies)

### Authorization
- Role-based access control (RBAC)
- Project-level permissions
- API key authentication for external integrations

### Data Protection
- Input validation via Pydantic schemas
- SQL injection prevention (ORM)
- XSS protection (React auto-escaping)
- CSRF protection (SameSite cookies)
- CORS configuration
- Rate limiting (100 req/min per user)

## API Design Principles

### OpenAPI-First Approach
1. Define OpenAPI specification first
2. Generate types for frontend (TypeScript)
3. Implement backend handlers from contract
4. Validate conformance automatically

### RESTful Conventions
- Noun-based resource naming
- HTTP verb semantics (GET, POST, PUT, PATCH, DELETE)
- Plural nouns for collections
- Consistent response format
- Proper status codes

### Response Format
```json
{
  "data": { /* response data */ },
  "meta": {
    "page": 1,
    "per_page": 20,
    "total": 100
  },
  "errors": []
}
```

## MCP Integration

### GitHub MCP Server
- Repository read operations
- Issue and PR tracking
- Commit history extraction
- File system operations within repo

### Filesystem MCP Server
- Local project file access
- Code analysis workflows
- Automated documentation generation

### Database MCP Server
- Direct database queries for reporting
- Analytics and metrics extraction
- Bulk data operations

### MCP Workflow Example
```
User requests code analysis
  ↓
Frontend calls API: POST /api/v1/agents/analyze
  ↓
Backend orchestrates MCP server calls:
  1. Filesystem MCP: Read project structure
  2. Database MCP: Query AI activity history
  3. GitHub MCP: Fetch recent commits
  ↓
Aggregate results and return insights
```

## CI/CD Pipeline

### GitHub Actions Workflow

```
┌──────────────────┐
│  Trigger: Push/PR │
└────────┬─────────┘
         │
┌────────▼─────────┐
│  Lint & Format   │
│  (ESLint, Black) │
└────────┬─────────┘
         │
┌────────▼─────────┐
│  Unit Tests      │
│  (Jest, pytest)  │
└────────┬─────────┘
         │
┌────────▼─────────┐
│  Integration     │
│  Tests           │
└────────┬─────────┘
         │
┌────────▼─────────┐
│  Build Images    │
│  (Docker)        │
└────────┬─────────┘
         │
┌────────▼─────────┐
│  Deploy          │
│  (Staging/Prod)  │
└──────────────────┘
```

### Quality Gates
- Code coverage threshold: 80%
- No critical security vulnerabilities
- All tests must pass
- Docker images must build successfully

## Deployment Architecture

### Development
```yaml
services:
  frontend: Vite dev server
  backend: uvicorn with hot reload
  database: SQLite in volume
```

### Production
```yaml
services:
  frontend: nginx serving static files
  backend: uvicorn (multiple workers)
  database: PostgreSQL with persistence
  nginx: reverse proxy + SSL termination
```

### Cloud Platform Options
- **Render**: Simple deployment, free tier available
- **Railway**: Modern DX, auto-deploy from GitHub
- **DigitalOcean App Platform**: Predictable pricing
- **AWS ECS**: Enterprise-grade (if needed)

## Monitoring & Observability

### Application Metrics
- Request rate and latency
- Error rate by endpoint
- Database query performance
- AI agent execution time
- CI/CD pipeline duration

### Logging
- Structured JSON logging
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Correlation IDs for request tracing
- Sensitive data redaction

### Health Checks
- `/health`: Basic health check
- `/health/ready`: Readiness probe (dependencies)
- `/health/live`: Liveness probe (application state)

## Scalability Considerations

### Current Design (MVP)
- Single-instance deployment
- Horizontal scaling via container replicas
- Connection pooling for database
- Stateless API design

### Future Enhancements
- Redis caching layer
- Message queue for async agents
- Database read replicas
- CDN for static assets
- GraphQL API option

## Development Workflow

### AI-Assisted Development Flow
1. User creates feature request in platform
2. AI agent analyzes requirements
3. Agent generates initial code scaffold
4. Developer reviews and refines
5. Platform tracks all AI interactions
6. Automated tests generated with AI assistance
7. PR reviewed with AI-generated summary
8. Pipeline executes with quality gates
9. Deployment tracked in platform

### Vibe Coding Integration
- Real-time AI suggestions during development
- Prompt library for common tasks
- Template prompts for different scenarios
- Version-controlled prompts alongside code
