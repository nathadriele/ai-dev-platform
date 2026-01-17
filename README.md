# AI-Assisted Developer Productivity Platform

![alt text](/ai-dev-platform/imgs/image.png)

A full-stack platform for tracking, managing, and demonstrating the effective use of AI tools and code agents in software development workflows.

## Overview

This platform provides a centralized hub for:
- **Project Management**: Track software development projects
- **AI Activity Logging**: Document all AI tool interactions (prompts, responses, decisions)
- **Code Agent Orchestration**: Execute and monitor AI-powered code agents
- **CI/CD Integration**: Monitor pipelines and deployment history
- **Analytics & Reporting**: Gain insights into AI-assisted development productivity
- **MCP Integration**: Leverage Model-Context Protocol for enhanced tool capabilities

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                      Frontend (React + TypeScript)            │
│                   Material UI + Redux Toolkit                 │
└────────────────────────┬─────────────────────────────────────┘
                         │ HTTP/REST API
┌────────────────────────▼─────────────────────────────────────┐
│                    Backend (FastAPI)                          │
│              OpenAPI-first, Async Python                      │
└────────────────────────┬─────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────┐
│              Database (SQLite / PostgreSQL)                   │
│                 SQLAlchemy ORM                                │
└──────────────────────────────────────────────────────────────┘
```

## Tech Stack

### Frontend
- **React 18** with TypeScript
- **Material UI (MUI)** for components
- **Redux Toolkit** for state management
- **React Router v6** for routing
- **Vite** for build tooling
- **Axios** for HTTP requests
- **Recharts** for data visualization

### Backend
- **FastAPI** for REST API
- **SQLAlchemy 2.0** with async support
- **Pydantic v2** for data validation
- **PostgreSQL** (production) / **SQLite** (development)
- **Alembic** for database migrations
- **PyJWT** for authentication
- **Uvicorn** as ASGI server

### DevOps & Infrastructure
- **Docker** for containerization
- **docker-compose** for multi-container orchestration
- **GitHub Actions** for CI/CD
- **nginx** as reverse proxy (production)

### AI & Automation
- **OpenAI API** (GPT-4)
- **Anthropic API** (Claude)
- **Model-Context Protocol (MCP)**
- **n8n** for workflow automation

## Features

### 1. Project Management
- Create and manage software projects
- Track repository URLs and tech stacks
- Monitor project status and activity
- Archive completed projects

### 2. AI Activity Tracking
- Log interactions with AI tools (ChatGPT, Claude, Copilot, Cursor)
- Record prompts, responses, and code changes
- Categorize activities (feature, bugfix, refactor, docs, test)
- Track cost and time savings

### 3. Code Agent Orchestration
- Execute specialized code agents:
  - **Code Scaffolder**: Generate boilerplate and project structure
  - **Code Reviewer**: Review for bugs, security, and best practices
  - **Test Generator**: Create comprehensive test suites
  - **Documentation Generator**: Generate technical documentation
- Monitor agent execution status
- View agent outputs and results

### 4. CI/CD Pipeline Monitoring
- Track pipeline executions
- Monitor build and test results
- View deployment history
- Analyze success/failure rates

### 5. Analytics Dashboard
- AI tool usage statistics
- Productivity metrics
- Cost analysis
- Activity visualizations

### 6. MCP Integration
- Connect to GitHub MCP for repository operations
- Use Filesystem MCP for project analysis
- Database MCP for analytics
- HTTP API MCP for external integrations

## Quick Start

### Prerequisites

- **Docker** and **docker-compose** (for containerized setup)
- **Python 3.11+** (for local development)
- **Node.js 20+** and **npm** (for frontend development)
- **PostgreSQL 15+** (for production, optional for development)

### Option 1: Docker (Recommended)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/ai-dev-platform.git
   cd ai-dev-platform
   ```

2. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start all services**:
   ```bash
   docker-compose up -d
   ```

4. **Access the application**:
   - Frontend: http://localhost:80
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - n8n (automation): http://localhost:5678

### Option 2: Local Development

#### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run database migrations** (if using PostgreSQL):
   ```bash
   alembic upgrade head
   ```

6. **Start the development server**:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

#### Frontend Setup

1. **Navigate to frontend directory** (in a new terminal):
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install## Overview

This platform provides a centralized hub for:
- **Project Management**: Track software development projects
- **AI Activity Logging**: Document all AI tool interactions (prompts, responses, decisions)
- **Code Agent Orchestration**: Execute and monitor AI-powered code agents
- **CI/CD Integration**: Monitor pipelines and deployment history
- **Analytics & Reporting**: Gain insights into AI-assisted development productivity
- **MCP Integration**: Leverage Model-Context Protocol for enhanced tool capabilities

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                      Frontend (React + TypeScript)            │
│                   Material UI + Redux Toolkit                 │
└────────────────────────┬─────────────────────────────────────┘
                         │ HTTP/REST API
┌────────────────────────▼─────────────────────────────────────┐
│                    Backend (FastAPI)                          │
│              OpenAPI-first, Async Python                      │
└────────────────────────┬─────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────┐
│              Database (SQLite / PostgreSQL)                   │
│                 SQLAlchemy ORM                                │
└──────────────────────────────────────────────────────────────┘
```

## Tech Stack

### Frontend
- **React 18** with TypeScript
- **Material UI (MUI)** for components
- **Redux Toolkit** for state management
- **React Router v6** for routing
- **Vite** for build tooling
- **Axios** for HTTP requests
- **Recharts** for data visualization

### Backend
- **FastAPI** for REST API
- **SQLAlchemy 2.0** with async support
- **Pydantic v2** for data validation
- **PostgreSQL** (production) / **SQLite** (development)
- **Alembic** for database migrations
- **PyJWT** for authentication
- **Uvicorn** as ASGI server

### DevOps & Infrastructure
- **Docker** for containerization
- **docker-compose** for multi-container orchestration
- **GitHub Actions** for CI/CD
- **nginx** as reverse proxy (production)

### AI & Automation
- **OpenAI API** (GPT-4)
- **Anthropic API** (Claude)
- **Model-Context Protocol (MCP)**
- **n8n** for workflow automation

## Features

### 1. Project Management
- Create and manage software projects
- Track repository URLs and tech stacks
- Monitor project status and activity
- Archive completed projects

### 2. AI Activity Tracking
- Log interactions with AI tools (ChatGPT, Claude, Copilot, Cursor)
- Record prompts, responses, and code changes
- Categorize activities (feature, bugfix, refactor, docs, test)
- Track cost and time savings

### 3. Code Agent Orchestration
- Execute specialized code agents:
  - **Code Scaffolder**: Generate boilerplate and project structure
  - **Code Reviewer**: Review for bugs, security, and best practices
  - **Test Generator**: Create comprehensive test suites
  - **Documentation Generator**: Generate technical documentation
- Monitor agent execution status
- View agent outputs and results

### 4. CI/CD Pipeline Monitoring
- Track pipeline executions
- Monitor build and test results
- View deployment history
- Analyze success/failure rates

### 5. Analytics Dashboard
- AI tool usage statistics
- Productivity metrics
- Cost analysis
- Activity visualizations

### 6. MCP Integration
- Connect to GitHub MCP for repository operations
- Use Filesystem MCP for project analysis
- Database MCP for analytics
- HTTP API MCP for external integrations

## Quick Start

### Prerequisites

- **Docker** and **docker-compose** (for containerized setup)
- **Python 3.11+** (for local development)
- **Node.js 20+** and **npm** (for frontend development)
- **PostgreSQL 15+** (for production, optional for development)

### Option 1: Docker (Recommended)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/ai-dev-platform.git
   cd ai-dev-platform
   ```

2. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start all services**:
   ```bash
   docker-compose up -d
   ```

4. **Access the application**:
   - Frontend: http://localhost:80
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - n8n (automation): http://localhost:5678

### Option 2: Local Development

#### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run database migrations** (if using PostgreSQL):
   ```bash
   alembic upgrade head
   ```

6. **Start the development server**:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

#### Frontend Setup

1. **Navigate to frontend directory** (in a new terminal):
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Configure environment**:
   ```bash
   cp .env.example .env
   # The default values should work for local development
   ```

4. **Start the development server**:
   ```bash
   npm run dev
   ```

5. **Access the application**:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000

## Initial Setup

After starting the application:

1. **Create a user account**:
   - Navigate to http://localhost:5173 (or http://localhost:80 for Docker)
   - Click "Sign Up"
   - Enter your details
   - Or use the API directly:
     ```bash
     curl -X POST http://localhost:8000/api/v1/auth/register \
       -H "Content-Type: application/json" \
       -d '{
         "email": "user@example.com",
         "password": "securepassword",
         "username": "devuser"
       }'
     ```

2. **Create your first project**:
   - Login to the application
   - Go to "Projects"
   - Click "New Project"
   - Fill in project details

3. **Log AI activities**:
   - Start tracking your AI tool usage
   - Go to "AI Activities"
   - Log your interactions manually or via API

## Usage Examples

### Creating a Project via API

```bash
curl -X POST http://localhost:8000/api/v1/projects \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My AI-Assisted App",
    "description": "An application built with AI assistance",
    "repository_url": "https://github.com/user/my-app",
    "tech_stack": ["React", "FastAPI", "PostgreSQL"]
  }'
```

### Logging AI Activity

```bash
curl -X POST http://localhost:8000/api/v1/ai-activities \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "PROJECT_UUID",
    "tool_used": "claude",
    "prompt": "Generate a REST API for user management",
    "response": "Here is a complete FastAPI implementation...",
    "category": "feature"
  }'
```

### Executing a Code Agent

```bash
curl -X POST http://localhost:8000/api/v1/agents \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "PROJECT_UUID",
    "agent_type": "code-reviewer",
    "task_description": "Review the latest commit for security issues"
  }'
```

## Project Structure

```
ai-dev-platform/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Core functionality (config, security, db)
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   └── main.py         # Application entry point
│   ├── tests/              # Backend tests
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Backend container
│
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API client services
│   │   ├── store/          # Redux store
│   │   ├── types/          # TypeScript types
│   │   └── main.tsx        # Application entry point
│   ├── package.json        # Node dependencies
│   └── Dockerfile          # Frontend container
│
├── docs/                   # Documentation
│   ├── openapi.yaml        # API specification
│   ├── DEPLOYMENT.md       # Deployment guide
│   └── AI_DOCUMENTATION.md # AI tools and workflows
│
├── n8n-workflows/          # n8n automation workflows
│   └── automations/        # Workflow JSON files
│
├── .github/                # GitHub configurations
│   └── workflows/          # CI/CD workflows
│
├── docker-compose.yml      # Production containers
├── docker-compose.dev.yml  # Development containers
├── ARCHITECTURE.md         # System architecture
├── AGENTS.md              # Code agent documentation
└── README.md              # This file
```

## Documentation

- **[ARCHITECTURE.md](ARCHITECTURE.md)**: Detailed system architecture and design decisions
- **[AGENTS.md](AGENTS.md)**: Code agent documentation and usage
- **[docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)**: Complete deployment guide for various cloud platforms
- **[docs/AI_DOCUMENTATION.md](docs/AI_DOCUMENTATION.md)**: AI tools, prompts, and workflows
- **[docs/openapi.yaml](docs/openapi.yaml)**: Complete OpenAPI specification
- **[n8n-workflows/automations/README.md](n8n-workflows/automations/README.md)**: n8n workflow documentation

## Development

### Running Tests

**Backend tests**:
```bash
cd backend
pytest tests/ -v --cov=app --cov-report=html
```

**Frontend tests**:
```bash
cd frontend
npm test -- --coverage
```

### Code Quality

**Backend linting**:
```bash
cd backend
ruff check .
black --check .
mypy app/
```

**Frontend linting**:
```bash
cd frontend
npm run lint
npm run type-check
```

### Database Migrations

**Create migration**:
```bash
cd backend
alembic revision --autogenerate -m "Description of changes"
```

**Apply migrations**:
```bash
alembic upgrade head
```

**Rollback migration**:
```bash
alembic downgrade -1
```

## Deployment

### Quick Deploy to Render

1. Push code to GitHub
2. Go to [render.com](https://render.com)
3. Create new Web Services:
   - Backend: Connect to repo, set build and start commands
   - Frontend: Connect to repo, set build and output directory
4. Create PostgreSQL database
5. Add environment variables
6. Deploy!

For detailed deployment instructions for Render, Railway, DigitalOcean, or AWS, see [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md).

## CI/CD

The project includes a GitHub Actions workflow that:
- Runs linting and tests on every push and PR
- Builds Docker images
- Deploys to production on merge to main
- Generates AI-powered PR summaries

See [`.github/workflows/ci-cd.yml`](.github/workflows/ci-cd.yml) for details.

## AI Tools Used in Development

This platform was built with significant AI assistance. For details on:
- Which AI tools were used
- Effective prompts for various tasks
- Development workflows
- Best practices and limitations

See [docs/AI_DOCUMENTATION.md](docs/AI_DOCUMENTATION.md).

## n8n Automation

The platform includes n8n workflows for:
- **LinkedIn Post Generator**: Auto-generate technical posts
- **Resume Customizer**: Tailor resumes to job descriptions
- **Weekly Reports**: Summarize development activities
- **PR Summaries**: Generate pull request reviews

See [n8n-workflows/automations/README.md](n8n-workflows/automations/README.md) for setup instructions.

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes (document AI assistance in commit messages)
4. Add tests if applicable
5. Ensure all tests pass
6. Submit a pull request

## Roadmap

### Phase 1: Foundation (Current)
- Core platform functionality
- Basic AI activity tracking
- Project management
- CI/CD integration

### Phase 2: Enhanced Features
- Advanced analytics and dashboards
- Multi-language support
- Real-time collaboration
- Mobile app (React Native)

### Phase 3: AI Integration
- Direct AI API integration (no manual logging)
- AI-powered code suggestions
- Automated test generation
- Intelligent project recommendations

### Phase 4: Enterprise Features
- Team collaboration tools
- Advanced permissions
- SSO integration
- Audit logging
- Custom branding

## License

MIT License - see LICENSE file for details

## Acknowledgments

Built with the help of:
- **Claude (Anthropic)**: Architecture design, code generation, documentation
- **ChatGPT (OpenAI)**: Code snippets, debugging, test generation
- **GitHub Copilot**: Real-time code completion
- **Cursor**: Multi-file refactoring and scaffolding

Special thanks to the open-source community for the amazing tools and libraries that make this platform possible.

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check the documentation
- Review AI documentation for best practices

## Demonstrating AI-Assisted Development

This project itself serves as a demonstration of AI-assisted development. Key examples:

1. **OpenAPI-First Design**: API contract defined before implementation
2. **AI Code Generation**: Components and routes generated with AI assistance
3. **Automated Testing**: Test cases created with AI help
4. **Documentation**: Comprehensive docs generated via AI
5. **CI/CD Automation**: AI-generated PR summaries and analysis

For a detailed breakdown of how AI was used in building this platform, see [docs/AI_DOCUMENTATION.md](docs/AI_DOCUMENTATION.md).

---

**Built with passion and AI assistance to demonstrate the future of software development.**