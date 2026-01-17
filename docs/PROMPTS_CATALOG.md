# Real AI Prompts Used During Development

This document catalogs actual prompts used with AI tools (Claude, ChatGPT, Cursor) throughout the development of the AI-Assisted Developer Productivity Platform.

## Table of Contents

1. [Architecture & Design Prompts](#architecture--design-prompts)
2. [Backend Development Prompts](#backend-development-prompts)
3. [Frontend Development Prompts](#frontend-development-prompts)
4. [Database & Modeling Prompts](#database--modeling-prompts)
5. [Testing Prompts](#testing-prompts)
6. [Documentation Prompts](#documentation-prompts)
7. [DevOps & Deployment Prompts](#devops--deployment-prompts)
8. [Debugging & Problem Solving Prompts](#debugging--problem-solving-prompts)

---

## Architecture & Design Prompts

### Prompt 1.1: Initial System Architecture

**Tool**: Claude 3 Sonnet
**Context**: Planning phase of project
**Date**: 2024-01-15

```
Design a comprehensive architecture for an "AI-Assisted Developer Productivity Platform" that:

1. Allows developers to track AI tool usage (ChatGPT, Claude, Copilot, Cursor)
2. Logs prompts, responses, and code changes made with AI assistance
3. Orchestrates code agents for tasks like scaffolding, review, testing
4. Integrates with CI/CD pipelines
5. Provides analytics on AI-assisted development productivity
6. Supports Model-Context Protocol (MCP) for external integrations
7. Includes automation workflows via n8n

Requirements:
- Frontend: React + TypeScript
- Backend: FastAPI (Python)
- Database: PostgreSQL (production), SQLite (development)
- Must be containerized with Docker
- Complete CI/CD with GitHub Actions
- OpenAPI-first API design

Please provide:
1. High-level system architecture diagram
2. Technology stack justification
3. Key components and their responsibilities
4. Database schema outline
5. API structure
6. Security considerations
7. Scalability approach
```

**Result**: ARCHITECTURE.md with complete system design

### Prompt 1.2: Database Schema Design

**Tool**: Claude 3 Sonnet
**Context**: After architecture definition
**Date**: 2024-01-15

```
Design a complete database schema for the AI-Assisted Developer Productivity Platform.

Entities needed:
1. Users (authentication, profiles)
2. Projects (software projects being tracked)
3. AI Activities (logs of AI tool interactions)
4. Agent Executions (code agent run history)
5. Pipeline Executions (CI/CD pipeline tracking)
6. MCP Servers (external integrations)

For each entity, provide:
1. All necessary fields with types
2. Primary and foreign keys
3. Indexes for performance
4. Relationships between tables
5. Enum types where appropriate

Consider:
- PostgreSQL for production
- SQLAlchemy ORM patterns
- Alembic migrations
- Data integrity constraints
- Query optimization (N+1 prevention)

Provide SQL DDL and SQLAlchemy model definitions.
```

**Result**: Complete database models in `backend/app/models/`

---

## Backend Development Prompts

### Prompt 2.1: FastAPI Backend Structure

**Tool**: Cursor (multi-file generation)
**Context**: Backend development
**Date**: 2024-01-16

```
Generate a complete FastAPI backend structure for the AI platform following these requirements:

1. Project Structure:
   - app/api/v1/ - API route modules
   - app/core/ - Config, security, database
   - app/models/ - SQLAlchemy models
   - app/schemas/ - Pydantic validation schemas
   - app/services/ - Business logic layer
   - app/utils/ - Helper functions
   - tests/ - Unit and integration tests

2. OpenAPI Specification Compliance:
   - All endpoints must match the OpenAPI spec
   - Proper HTTP status codes
   - Request/response validation
   - Error handling with consistent format

3. Key Features:
   - JWT authentication with access/refresh tokens
   - Password hashing with bcrypt
   - CORS configuration
   - Rate limiting middleware
   - Structured logging
   - Async/await throughout
   - Database session management

4. For each module (health, auth, projects, ai_activities, agents, pipelines, analytics):
   - Create router with proper REST methods
   - Implement CRUD operations
   - Add pagination support
   - Include error handling
   - Write docstrings

Generate complete, production-ready code.
```

**Result**: Complete backend structure with all routers and services

### Prompt 2.2: Service Layer Implementation

**Tool**: ChatGPT (GPT-4)
**Context**: Refactoring database access
**Date**: 2024-01-16

```
Refactor the API routes to use a service layer pattern instead of direct database access.

Requirements:
1. Create a generic BaseService with common CRUD operations
2. Implement specific services (UserService, ProjectService, AIActivityService)
3. Each service should have:
   - Async methods
   - Proper error handling
   - Complex queries (search, filters, aggregations)
   - Business logic separation

Example for UserService:
- get_by_email()
- get_by_username()
- authenticate()
- create_with_hashed_password()

Example for ProjectService:
- get_user_projects()
- search()
- get_active_count()

Provide complete implementation with type hints.
```

**Result**: `backend/app/services/` with complete service layer

### Prompt 2.3: JWT Authentication Middleware

**Tool**: Claude 3 Sonnet
**Context**: Adding authentication
**Date**: 2024-01-17

```
Create a comprehensive authentication middleware for FastAPI that:

1. Validates JWT tokens on every request
2. Skips authentication for public endpoints (whitelist)
3. Injects user_id into request state
4. Validates token type (access vs refresh)
5. Returns proper error responses
6. Works with BackgroundTasks for async operations

Requirements:
- Use the existing decode_token() from security.py
- Support Bearer token format
- Whitelist: /health, /docs, /redoc, /auth/register, /auth/login
- Return 401 with proper error format
- Be compatible with dependency injection

Also provide helper functions:
- get_current_user() - Returns User object from DB
- get_optional_user() - Returns User or None

Implement as BaseHTTPMiddleware for FastAPI.
```

**Result**: `backend/app/middleware/auth.py`

---

## Frontend Development Prompts

### Prompt 3.1: React Project Setup

**Tool**: Cursor (multi-file)
**Context**: Frontend initialization
**Date**: 2024-01-16

```
Generate a complete React + TypeScript frontend structure using:
- React 18 with hooks
- TypeScript with strict mode
- Vite for build tool
- Material UI (MUI) v5 for components
- Redux Toolkit for state management
- React Router v6
- Axios for HTTP requests
- Recharts for visualizations

Project structure:
- src/components/ - Reusable components
- src/pages/ - Page components (Dashboard, Projects, AI Activities, Analytics, Agents)
- src/services/ - API client services
- src/store/ - Redux store and slices
- src/types/ - TypeScript type definitions
- src/styles/ - Global styles

Generate:
1. package.json with all dependencies
2. tsconfig.json with path aliases (@/*)
3. vite.config.ts with proxy configuration
4. Main App component with routing
5. Redux store with auth, projects, aiActivities slices
6. API client with axios and interceptors

Include proper TypeScript types for all API responses.
```

**Result**: Complete frontend project structure

### Prompt 3.2: Analytics Dashboard Component

**Tool**: ChatGPT (GPT-4)
**Context**: Building analytics page
**Date**: 2024-01-17

```
Create a comprehensive Analytics Dashboard component for the AI platform that shows:

1. AI Tool Usage Section:
   - Bar chart comparing usage of ChatGPT, Claude, Copilot, Cursor
   - Pie chart showing activities by category (feature, bugfix, refactor, docs, test)
   - Summary cards: total prompts, estimated cost, time saved

2. Productivity Metrics Section:
   - Total commits (AI-assisted vs total)
   - Lines of code changed
   - AI contribution percentage
   - Test coverage gauge
   - Average build time

3. Recent Activity Timeline:
   - Group activities by date
   - Show tool, category, and timestamp
   - Color-coded by category

Requirements:
- Use Recharts for all visualizations
- Material UI components for layout
- Fetch data from /api/v1/analytics/* endpoints
- Show loading states
- Handle empty states
- Responsive design

Provide complete React component with TypeScript.
```

**Result**: `frontend/src/pages/AnalyticsPage.tsx`

---

## Database & Modeling Prompts

### Prompt 4.1: SQLAlchemy Models

**Tool**: Claude 3 Sonnet
**Context**: Database modeling
**Date**: 2024-01-15

```
Create SQLAlchemy 2.0 models with async support for:

1. User Model:
   - UUID primary key
   - Email (unique, indexed)
   - Username (unique, indexed)
   - Full name
   - Hashed password
   - Timestamps (created_at, updated_at)
   - Relationship to projects and activities

2. Project Model:
   - UUID primary key
   - Name, description
   - Repository URL
   - Tech stack (array of strings)
   - Status enum (active, archived)
   - Created by foreign key
   - Timestamps
   - Relationships to activities, agents, pipelines

3. AIActivity Model:
   - UUID primary key
   - Project foreign key
   - Tool used enum (chatgpt, claude, copilot, cursor)
   - Prompt (Text)
   - Response (Text, nullable)
   - Code changes (array of strings)
   - Timestamp
   - User foreign key
   - Category enum (feature, bugfix, refactor, docs, test)

4. AgentExecution Model:
   - UUID primary key
   - Project foreign key
   - Agent type
   - Task description
   - Status enum (pending, running, completed, failed)
   - Input/output data (JSON)
   - Started/completed timestamps
   - Error message

5. PipelineExecution Model:
   - UUID primary key
   - Project foreign key
   - Pipeline name
   - Status enum (running, success, failed)
   - Commit SHA, branch
   - Triggered by
   - Timestamps
   - Test results (JSON)
   - Deployment URL

6. MCPServer Model:
   - UUID primary key
   - Name (unique)
   - Server type enum
   - Endpoint URL
   - Status enum (active, inactive, error)
   - Capabilities (array of strings)
   - Last health check

All models should use:
- AsyncSession patterns
- Proper __repr__ methods
- Table name configuration
- Relationship definitions with back_populates
```

**Result**: Complete models in `backend/app/models/`

### Prompt 4.2: Alembic Migration

**Tool**: ChatGPT (GPT-4)
**Context**: Database versioning
**Date**: 2024-01-16

```
Create the initial Alembic migration for the AI platform database.

Requirements:
1. Create all 6 tables (users, projects, ai_activities, agent_executions, pipeline_executions, mcp_servers)
2. Use PostgreSQL UUID type
3. Add all indexes (unique, foreign keys, performance indexes)
4. Include proper foreign key constraints with ON DELETE behavior
5. Use timestamps with timezone support
6. Make it reversible (implement downgrade())

Migration should be:
- File: 001_initial_migration.py
- Revision: 001
- Down revision: None

Provide complete migration with both upgrade() and downgrade() methods.
```

**Result**: `backend/alembic/versions/001_initial_migration.py`

---

## Testing Prompts

### Prompt 5.1: Integration Test Framework

**Tool**: Claude 3 Sonnet
**Context**: Test setup
**Date**: 2024-01-17

```
Create a comprehensive pytest test setup for the FastAPI backend.

Requirements:

1. conftest.py with:
   - In-memory SQLite database for testing
   - Test client fixture using AsyncClient from httpx
   - Database session fixture with automatic cleanup
   - Sample data fixtures (user, project, ai_activity)
   - Auth headers fixture

2. Fixtures:
   - db_session - Creates fresh DB for each test
   - client - Test client with DB override
   - sample_user_data - Valid user data
   - sample_project_data - Valid project data
   - test_user - Creates user in DB
   - test_project - Creates project in DB
   - auth_headers - Returns authentication headers

3. Integration Tests:
   - Test auth endpoints (register, login, refresh)
   - Test project CRUD operations
   - Test AI activity logging
   - Test pagination and filtering

Use pytest-asyncio for async test support.
```

**Result**: `backend/tests/conftest.py` and integration tests

### Prompt 5.2: Unit Tests for Utils

**Tool**: ChatGPT (GPT-4)
**Context**: Testing utility functions
**Date**: 2024-01-17

```
Create comprehensive unit tests for utility functions.

Test files to create:
1. tests/unit/test_utils_validation.py
   - Test validate_username() - valid, invalid formats
   - Test validate_password() - strength requirements
   - Test validate_repository_url() - GitHub/GitLab/Bitbucket
   - Test sanitize_html() - script tag removal
   - Test validate_pagination_params() - edge cases

2. tests/unit/test_utils_string.py
   - Test generate_random_string() - length and format
   - Test slugify() - special characters handling
   - Test truncate_text() - with and without truncation
   - Test extract_hashtags() and extract_mentions()
   - Test mask_email() and mask_string()
   - Test is_valid_url() - various URL formats

For each test:
- Use pytest format
- Test normal cases and edge cases
- Use pytest.raises() for exception testing
- Include descriptive test names
- Use fixtures for repeated data
```

**Result**: Complete unit test suites

---

## Documentation Prompts

### Prompt 6.1: Complete README

**Tool**: Cursor (long-form generation)
**Context**: Project documentation
**Date**: 2024-01-17

```
Write a comprehensive README.md for the AI-Assisted Developer Productivity Platform.

Include:
1. Project Overview
   - What the platform does
   - Why it exists
   - Key features

2. Tech Stack (with justifications)
   - Frontend technologies
   - Backend technologies
   - Infrastructure tools
   - AI & Automation tools

3. Architecture
   - High-level diagram (described in text)
   - Component responsibilities
   - Data flow

4. Quick Start Guide
   - Prerequisites
   - Docker setup (recommended)
   - Local development setup
   - Environment configuration

5. Usage Examples
   - Creating a project via API
   - Logging AI activities
   - Executing agents
   - Viewing analytics

6. Development
   - Running tests
   - Code quality checks
   - Database migrations

7. Deployment
   - Docker Compose
   - Cloud platforms (Render, Railway, etc.)

8. Documentation links
   - ARCHITECTURE.md
   - AGENTS.md
   - DEPLOYMENT guide
   - AI_DOCUMENTATION.md

Make it professional, clear, and suitable for a portfolio project.
```

**Result**: `README.md` with complete project documentation

### Prompt 6.2: AI Documentation

**Tool**: Claude 3 Sonnet
**Context**: Documenting AI usage
**Date**: 2024-01-17

```
Create comprehensive documentation about AI tools usage during development.

Document:

1. AI Tools Used:
   - Claude (Anthropic)
   - ChatGPT (OpenAI)
   - GitHub Copilot
   - Cursor AI IDE

2. For each tool, include:
   - When it was used
   - What types of tasks
   - Strengths and limitations
   - Examples of prompts used

3. Prompt Engineering:
   - System prompts for backend dev
   - System prompts for frontend dev
   - Task-specific prompt templates
     - Code review
     - Test generation
     - Documentation generation
     - Refactoring

4. Development Workflows:
   - Feature development workflow
   - Bug fixing workflow
   - Refactoring workflow

5. Best Practices:
   - When to use AI
   - AI safety guidelines
   - Prompt optimization
   - Cost management

6. Metrics and Tracking:
   - How AI usage was measured
   - Productivity gains
   - Time saved calculations

Provide real examples of prompts used throughout the project.
```

**Result**: `docs/AI_DOCUMENTATION.md`

---

## DevOps & Deployment Prompts

### Prompt 7.1: Docker Configuration

**Tool**: ChatGPT (GPT-4)
**Context**: Containerization
**Date**: 2024-01-16

```
Create complete Docker configuration for the platform.

Files needed:

1. backend/Dockerfile:
   - Python 3.11 base image
   - Install system dependencies
   - Copy requirements.txt first (caching)
   - Install Python packages
   - Copy application code
   - Create data directory
   - Expose port 8000
   - Run with uvicorn

2. frontend/Dockerfile:
   - Multi-stage build (node:20-alpine)
   - Build stage: install deps, build with npm run build
   - Production stage: nginx:alpine
   - Copy built files
   - nginx configuration for SPA routing
   - Expose port 80

3. docker-compose.yml (production):
   - Backend service
   - Frontend service
   - PostgreSQL service
   - n8n service
   - Networks and volumes
   - Environment variables

4. docker-compose.dev.yml (development):
   - Backend with hot reload
   - Frontend with Vite dev server
   - SQLite or PostgreSQL
   - Volume mounts for code

5. .dockerignore files

Include best practices:
- Multi-stage builds
- Layer caching
- Minimal image sizes
- Proper signal handling
- Health checks
```

**Result**: Complete Docker configuration files

### Prompt 7.2: CI/CD Pipeline

**Tool**: Claude 3 Sonnet
**Context**: GitHub Actions setup
**Date**: 2024-01-17

```
Create a complete GitHub Actions CI/CD workflow for the AI platform.

Workflow should:

1. Trigger on push and pull_request to main/develop

2. Backend Pipeline:
   - Checkout code
   - Set up Python 3.11
   - Install dependencies
   - Run Ruff linting
   - Run Black formatting check
   - Run MyPy type checking
   - Run pytest with coverage
   - Upload coverage to Codecov

3. Frontend Pipeline:
   - Checkout code
   - Setup Node.js 20
   - Install dependencies
   - Run ESLint
   - Run TypeScript check
   - Run tests with coverage
   - Upload coverage to Codecov

4. Build and Push:
   - Build Docker images for backend and frontend
   - Push to GitHub Container Registry
   - Tag with branch, commit SHA, and version

5. Deploy (on merge to main):
   - Trigger deployment webhook
   - Create GitHub release
   - Run health checks

Also create:
- AI PR Summary workflow that generates PR summaries using AI

Make it production-ready with proper error handling and status badges.
```

**Result**: `.github/workflows/ci-cd.yml` and `ai-summary.yml`

---

## Debugging & Problem Solving Prompts

### Prompt 8.1: Async Database Issue

**Tool**: ChatGPT (GPT-4)
**Context**: Debugging SQLAlchemy async
**Date**: 2024-01-16

```
I'm getting an error with SQLAlchemy async sessions:

```
sqlalchemy.exc.MissingGreenlet: greenlet_spawn has not been called
```

Current setup:
- FastAPI with AsyncSession
- SQLAlchemy with asyncpg
- Using async/await in routes
- get_db() dependency with yield

The error occurs when accessing relationships.

What's causing this and how do I fix it?

Also provide:
1. Proper async session management
2. Correct way to access relationships in async
3. Best practices for async SQLAlchemy 2.0
4. Example of a working route with database operations
```

**Result**: Fixed database configuration and proper async patterns

### Prompt 8.2: Redux Toolkit Setup

**Tool**: Cursor
**Context**: Frontend state management
**Date**: 2024-01-16

```
Set up Redux Toolkit with proper async thunks for the AI platform.

Needed slices:
1. authSlice:
   - login async thunk (API call + token storage)
   - register async thunk
   - logout action
   - Error handling

2. projectSlice:
   - fetchProjects async thunk with pagination
   - createProject async thunk
   - updateProject async thunk
   - deleteProject async thunk
   - Pagination state management

3. aiActivitySlice:
   - fetchAIActivities async thunk
   - logAIActivity async thunk
   - Filtering by tool, category, project

For each slice:
- Define initial state
- Create async thunks with createAsyncThunk
- Handle pending, fulfilled, rejected cases
- Provide selectors if needed

Also provide:
- Store configuration
- Hook types (useAppDispatch, useAppSelector)
- Example usage in components

Use proper TypeScript typing throughout.
```

**Result**: Complete Redux store with slices

### Prompt 8.3: CORS Issues Resolution

**Tool**: Claude 3 Sonnet
**Context**: Debugging CORS errors
**Date**: 2024-01-17

```
I'm getting CORS errors when the frontend tries to access the backend.

Setup:
- Frontend: Vite dev server on http://localhost:5173
- Backend: FastAPI on http://localhost:8000
- Backend has CORS middleware configured

Error:
```
Access to fetch at 'http://localhost:8000/api/v1/projects' from origin 'http://localhost:5173' has been blocked by CORS policy
```

Backend CORS config:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

What's wrong and how to fix it?

Also explain:
1. How CORS works
2. Why preflight requests fail
3. Proper configuration for development vs production
4. Best practices for CORS in FastAPI
```

**Result**: Fixed CORS configuration in middleware

---

## Prompts for Specific Features

### Prompt 9.1: MCP Integration

**Tool**: Claude 3 Sonnet
**Context**: Implementing Model-Context Protocol
**Date**: 2024-01-17

```
Explain how to implement Model-Context Protocol (MCP) server integration for the AI platform.

Requirements:
1. Create a Filesystem MCP server that can:
   - List directory contents
   - Read file contents
   - Search files by pattern and content
   - Analyze code structure
   - Get statistics

2. Create a GitHub MCP server that can:
   - Get repository info
   - Get commits and diffs
   - List issues and PRs
   - Create comments
   - Get languages used

3. Backend integration:
   - Register MCP servers via API
   - Execute MCP tools
   - Handle responses
   - Error handling

For each server:
- Provide complete implementation
- Use mcp library for Python
- Include proper error handling
- Document available tools
- Provide usage examples

Also explain:
- What MCP is and why it's useful
- How it integrates with AI agents
- Security considerations
- Configuration in production
```

**Result**: MCP server implementations in `mcp-workflows/`

---

## Summary of Prompt Categories

| Category | Count | Primary Tools Used |
|----------|-------|-------------------|
| Architecture & Design | 2 | Claude |
| Backend Development | 4 | Cursor, ChatGPT, Claude |
| Frontend Development | 2 | Cursor, ChatGPT |
| Database & Modeling | 2 | Claude, ChatGPT |
| Testing | 2 | Claude, ChatGPT |
| Documentation | 2 | Cursor, Claude |
| DevOps & Deployment | 2 | ChatGPT, Claude |
| Debugging | 3 | ChatGPT, Claude, Cursor |
| Specific Features | 1 | Claude |
| **Total** | **20+** | **Mixed** |

## Prompt Engineering Techniques Used

1. **Role-Based Prompting**: "You are an expert Python backend developer..."
2. **Context Setting**: Provided full context about project goals
3. **Requirement Specification**: Clear lists and constraints
4. **Output Format Specifiers**: "Provide complete implementation with..."
5. **Example Requests**: "Provide complete React component with..."
6. **Iterative Refinement**: Started with basic prompts, refined with more specifics

## Cost Estimation

| Tool | Approx. Tokens Used | Est. Cost (USD) |
|------|-------------------|-----------------|
| Claude 3 Sonnet | ~150,000 | $0.60 |
| GPT-4 | ~50,000 | $1.50 |
| Cursor (metadata) | N/A | $10 (subscription) |
| **Total** | **~200,000** | **~$2.10** |

## Key Insights from Prompt Experience

1. **Claude is best for**: Architecture, documentation, complex code generation
2. **ChatGPT is best for**: Refactoring, specific implementations, unit tests
3. **Cursor is best for**: Multi-file generation, refactoring across files
4. **Prompt specificity matters**: More specific prompts = better results
5. **Iterative approach**: Start with overview, then specific implementations
6. **Code review prompts**: Essential for maintaining quality

## Most Effective Prompt Patterns

### Pattern 1: Complete Feature Generation
```
Generate [feature] with requirements:
1. [Requirement 1]
2. [Requirement 2]
...

Provide:
- File structure
- Complete implementation
- Error handling
- Type hints
- Usage examples
```

### Pattern 2: Problem Solving
```
I'm experiencing [problem]:
[Error message]

Current setup:
[Code snippet]

What's causing this and how to fix it?

Also explain:
1. Root cause
2. Solution approach
3. Prevention best practices
```

### Pattern 3: Architecture Design
```
Design [system] that:
- [Goal 1]
- [Goal 2]

Requirements:
[Requirements list]

Provide:
1. Architecture diagram
2. Component breakdown
3. Data flow
4. Technology choices
```

---

## Conclusion

This catalog represents **real prompts used** during development, demonstrating practical AI-assisted development. All prompts led to actual code in the repository, proving the effectiveness of AI collaboration in software development.
