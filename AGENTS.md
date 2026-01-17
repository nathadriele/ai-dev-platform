# AI Code Agents Documentation

This document describes the behavior, configuration, and usage of code agents in the AI-Assisted Developer Productivity Platform.

## Overview

Code agents are autonomous AI-powered tools that can perform specific development tasks within the platform. Each agent has a defined purpose, capabilities, and integration points with external tools via MCP (Model-Context Protocol).

## Available Agents

### 1. Code Scaffolder Agent

**Agent ID**: `code-scaffolder`
**Name**: Code Scaffolder
**Status**: Production Ready

#### Purpose
Generates project structure, boilerplate code, and initial implementation for new features or components.

#### Capabilities
- `scaffold`: Generate complete project structure
- `boilerplate`: Create boilerplate code for common patterns
- `structure`: Organize file and directory hierarchies

#### System Prompt
```
You are an expert software architect and code scaffolding specialist. Your task is to generate
well-structured, production-ready code following these principles:

1. **Clean Architecture**: Follow SOLID principles and separation of concerns
2. **Type Safety**: Use TypeScript/Python type hints comprehensively
3. **Best Practices**: Follow framework conventions and idiomatic patterns
4. **Documentation**: Include clear comments and docstrings
5. **Testing**: Write testable code with clear testing interfaces

When scaffolding:
- Start with the overall structure
- Define interfaces/types/models first
- Implement core logic
- Add error handling
- Include basic tests
- Document usage

Always explain your architectural choices and provide usage examples.
```

#### Input Schema
```python
{
  "project_id": str,
  "task_description": str,
  "input_data": {
    "feature_name": str,
    "tech_stack": List[str], 
    "patterns": List[str],
    "include_tests": bool,
  }
}
```

#### Output Schema
```python
{
  "status": "completed",
  "output_data": {
    "files_created": List[str],
    "structure": dict,
    "next_steps": List[str],
    "dependencies": List[str],
  }
}
```

#### Example Usage
```python
agent_service.execute(
    project_id="123e4567-e89b-12d3-a456-426614174000",
    agent_type="code-scaffolder",
    task_description="Create a FastAPI service for user authentication",
    input_data={
        "feature_name": "user-auth",
        "tech_stack": ["fastapi", "sqlalchemy", "pydantic"],
        "patterns": ["repository", "dependency-injection"],
        "include_tests": True,
    }
)
```

#### Workflow
1. Analyze task requirements
2. Determine appropriate architecture
3. Generate file structure
4. Create implementation files
5. Add configuration and dependencies
6. Generate basic tests
7. Document usage and next steps

#### Limitations
- Cannot execute code or create actual files
- Limited to generating code text
- Requires manual integration
- May need adjustments for specific project patterns

---

### 2. Code Reviewer Agent

**Agent ID**: `code-reviewer`
**Name**: Code Reviewer
**Status**: Production Ready
**MCP Required**: Yes (GitHub, Filesystem)

#### Purpose
Reviews code for bugs, security vulnerabilities, performance issues, and adherence to best practices.

#### Capabilities
- `review`: Perform comprehensive code review
- `analyze`: Analyze code quality metrics
- `security`: Focus on security vulnerabilities
- `performance`: Identify performance bottlenecks

#### System Prompt
```
You are a senior software engineer and security specialist performing code reviews. Your role
is to provide thorough, constructive feedback on code changes.

Review Checklist:

1. **Security** (Critical):
   - SQL injection vulnerabilities
   - XSS and CSRF risks
   - Authentication/authorization flaws
   - Sensitive data exposure
   - Dependency vulnerabilities

2. **Correctness**:
   - Logic errors
   - Edge cases
   - Error handling
   - Input validation

3. **Performance**:
   - Database query efficiency (N+1 problems)
   - Algorithm complexity
   - Memory usage
   - Caching opportunities

4. **Code Quality**:
   - Type safety
   - Code duplication (DRY)
   - Naming conventions
   - SOLID principles
   - Design patterns

5. **Testing**:
   - Test coverage
   - Test quality
   - Edge case testing

For each issue:
- Provide severity level (Critical/High/Medium/Low/Info)
- Include specific code references
- Suggest concrete fixes with examples
- Explain the "why" behind issues

Be constructive and educational. Your goal is to improve code quality and developer knowledge.
```

#### Input Schema
```python
{
  "project_id": str,
  "task_description": str,
  "input_data": {
    "commit_sha": str,  
    "file_paths": List[str], 
    "focus": List[str], 
    "severity_threshold": str,
  }
}
```

#### Output Schema
```python
{
  "status": "completed",
  "output_data": {
    "summary": str,  
    "issues": List[{
      "severity": str, 
      "category": str,  
      "file_path": str,
      "line_number": int,
      "description": str,
      "suggestion": str,
      "code_example": str, 
    }],
    "metrics": {
      "total_issues": int,
      "critical_issues": int,
      "high_issues": int,
      "medium_issues": int,
      "low_issues": int,
    },
    "positive_notes": List[str], 
  }
}
```

#### Example Usage
```python
agent_service.execute(
    project_id="123e4567-e89b-12d3-a456-426614174000",
    agent_type="code-reviewer",
    task_description="Review commit abc123 for security issues",
    input_data={
        "commit_sha": "abc123",
        "file_paths": [],
        "focus": ["security", "performance"],
        "severity_threshold": "medium",
    }
)
```

#### MCP Integration
- **GitHub MCP**: Fetch commit diff, file changes
- **Filesystem MCP**: Read file contents for analysis

#### Workflow
1. Fetch code via MCP (GitHub/Filesystem)
2. Parse and analyze code structure
3. Run security patterns and heuristics
4. Identify performance issues
5. Check for code quality violations
6. Generate structured report
7. Provide actionable recommendations

---

### 3. Test Generator Agent

**Agent ID**: `test-generator`
**Name**: Test Generator
**Status**: Production Ready
**MCP Required**: Yes (Filesystem)

#### Purpose
Generates comprehensive unit tests, integration tests, and test fixtures for existing code.

#### Capabilities
- `testing`: Generate various types of tests
- `unit-tests`: Focus on unit test generation
- `integration-tests`: Create integration test suites
- `fixtures`: Generate test fixtures and mocks

#### System Prompt
```
You are a testing specialist dedicated to creating comprehensive, maintainable test suites.
Your tests should be:

1. **Comprehensive**: Cover normal cases, edge cases, and error conditions
2. **Clear**: Test names and assertions should be self-documenting
3. **Independent**: Tests should not depend on each other
4. **Fast**: Unit tests should run quickly
5. **Maintainable**: Use fixtures and setup/teardown appropriately
6. **Realistic**: Mocks should reflect actual behavior

Testing Principles:
- Arrange-Act-Assert (AAA) pattern
- One assertion per test (mostly)
- Descriptive test names
- Test behaviors, not implementation
- Use Given-When-Then for complex scenarios
- Mock external dependencies
- Test boundary conditions

Generate tests using pytest for Python and Jest/React Testing Library for frontend.
Include setup/teardown, fixtures, and documentation on running tests.
```

#### Input Schema
```python
{
  "project_id": str,
  "task_description": str,
  "input_data": {
    "file_path": str, 
    "test_types": List[str], 
    "coverage_target": float, 
    "framework": str, 
  }
}
```

#### Output Schema
```python
{
  "status": "completed",
  "output_data": {
    "test_file_path": str,
    "test_code": str,
    "fixtures": List[str], 
    "setup_instructions": str,
    "coverage_estimate": float,
    "test_count": int,
  }
}
```

#### Example Usage
```python
agent_service.execute(
    project_id="123e4567-e89b-12d3-a456-426614174000",
    agent_type="test-generator",
    task_description="Generate unit tests for user service",
    input_data={
        "file_path": "backend/app/services/user.py",
        "test_types": ["unit"],
        "coverage_target": 90.0,
        "framework": "pytest",
    }
)
```

#### Test Generation Strategy

**Unit Tests**:
- Test all public methods
- Mock all external dependencies
- Test edge cases and error conditions
- Use parameterized tests for multiple inputs

**Integration Tests**:
- Test component interactions
- Use test database
- Test API endpoints
- Verify database operations

**Test Fixtures**:
- Reusable test data
- Database fixtures
- Mock configurations
- Test client setup

#### Workflow
1. Read target code via Filesystem MCP
2. Analyze functions and dependencies
3. Determine test scenarios
4. Generate test cases for each scenario
5. Create fixtures and mocks
6. Add setup/teardown
7. Provide execution instructions

---

### 4. Documentation Generator Agent

**Agent ID**: `doc-generator`
**Name**: Documentation Generator
**Status**: Production Ready
**MCP Required**: Yes (Filesystem, GitHub)

#### Purpose
Generates and updates technical documentation, API docs, README files, and code comments.

#### Capabilities
- `docs`: Generate various documentation types
- `documentation`: Create comprehensive docs
- `markdown`: Generate Markdown documentation

#### System Prompt
```
You are a technical documentation specialist. Your documentation should be:

1. **Clear**: Use simple, precise language
2. **Complete**: Cover all necessary information
3. **Accurate**: Technical details must be correct
4. **Well-structured**: Use proper headings, lists, and formatting
5. **Audience-aware**: Adjust depth for target audience
6. **Example-rich**: Include practical examples

Documentation Types:
- API Reference: Endpoints, parameters, responses
- User Guides: Step-by-step instructions
- Architecture Docs: System design and decisions
- Code Comments: Inline explanations
- README: Project overview and setup

Use Markdown format. Include:
- Clear headings hierarchy
- Code blocks with syntax highlighting
- Diagrams (in Mermaid or text format)
- Tables for structured data
- Links to related docs

Always explain "why", not just "what".
```

#### Input Schema
```python
{
  "project_id": str,
  "task_description": str,
  "input_data": {
    "doc_type": str, 
    "source_files": List[str], 
    "audience": str, 
    "include_examples": bool,
  }
}
```

#### Output Schema
```python
{
  "status": "completed",
  "output_data": {
    "documentation": str,
    "file_path": str,
    "related_docs": List[str],
    "diagrams": List[str], 
  }
}
```

#### Example Usage
```python
agent_service.execute(
    project_id="123e4567-e89b-12d3-a456-426614174000",
    agent_type="doc-generator",
    task_description="Generate API documentation for user endpoints",
    input_data={
        "doc_type": "api",
        "source_files": ["backend/app/api/v1/users.py"],
        "audience": "developers",
        "include_examples": True,
    }
)
```

#### MCP Integration
- **Filesystem MCP**: Read source code
- **GitHub MCP**: Get recent changes, commit history

#### Workflow
1. Read source files via MCP
2. Analyze code structure
3. Extract API signatures/data models
4. Generate documentation
5. Create examples
6. Add diagrams where helpful
7. Review for completeness

---

## Agent Execution Architecture

### Execution Lifecycle

```
┌──────────────────────────────────────────────────────────────┐
│ 1. Task Submission                                           │
│    User/API creates AgentExecution record                    │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│ 2. Agent Initialization                                       │
│    - Load agent configuration                                │
│    - Initialize MCP connections (if required)                │
│    - Set up AI model client                                  │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│ 3. Context Gathering (MCP)                                   │
│    - Fetch relevant files                                    │
│    - Get repository data                                     │
│    - Query database if needed                                │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│ 4. Prompt Construction                                       │
│    - Load system prompt                                      │
│    - Add context from MCP                                    │
│    - Include task description                                │
│    - Add input data                                          │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│ 5. AI Model Execution                                        │
│    - Call AI API                                             │
│    - Stream response (if applicable)                         │
│    - Handle rate limits                                      │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│ 6. Response Processing                                       │
│    - Validate output structure                               │
│    - Parse results                                           │
│    - Extract actionable items                                │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│ 7. Result Storage                                            │
│    - Update AgentExecution record                            │
│    - Store generated code/files                              │
│    - Create notifications                                    │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│ 8. Completion Notification                                   │
│    - Mark execution as completed                             │
│    - Send webhook/notification                              │
│    - Trigger follow-up actions                               │
└──────────────────────────────────────────────────────────────┘
```

### Error Handling

Agents handle various error scenarios:

1. **AI API Errors**
   - Rate limiting: Implement exponential backoff
   - Timeouts: Retry with adjusted parameters
   - Invalid responses: Validate and retry

2. **MCP Errors**
   - Connection failures: Log and fallback
   - Missing data: Proceed with available context
   - Timeout: Use cached data if available

3. **Validation Errors**
   - Invalid input: Return clear error message
   - Missing required fields: Request clarification
   - Type mismatches: Convert or reject

4. **Execution Errors**
   - Partial completion: Save what's available
   - Critical failures: Rollback and notify
   - Warnings: Log but continue

### Performance Considerations

1. **Caching**
   - Cache MCP responses
   - Reuse AI responses when possible
   - Store generated code for reference

2. **Batching**
   - Process multiple files together
   - Batch API calls
   - Parallelize independent tasks

3. **Resource Management**
   - Limit concurrent executions
   - Monitor token usage
   - Implement timeouts

## Best Practices

### Using Agents Effectively

1. **Clear Task Descriptions**
   - Be specific about requirements
   - Include context and constraints
   - Provide examples if helpful

2. **Review Generated Output**
   - Always review agent output
   - Test generated code
   - Validate documentation

3. **Iterative Refinement**
   - Start with smaller tasks
   - Refine based on results
   - Combine multiple agents

4. **Track Agent Performance**
   - Monitor execution time
   - Measure quality metrics
   - Collect feedback

### Limitations

1. **Cannot Execute Code**
   - Agents generate code text only
   - Manual integration required
   - Testing needed

2. **Context Limits**
   - Large codebases may exceed context
   - Requires focused tasks
   - May need multiple iterations

3. **No Persistent Memory**
   - Each execution is independent
   - No learning from past
   - Cannot remember preferences

4. **Dependency on AI Models**
   - API rate limits
   - Potential downtime
   - Model hallucinations

## Future Enhancements

### Planned Agents

1. **Performance Optimizer Agent**
   - Analyze performance bottlenecks
   - Suggest optimizations
   - Generate profiling code

2. **Migration Agent**
   - Generate database migrations
   - Handle breaking changes
   - Create rollback scripts

3. **Deployment Agent**
   - Generate deployment configurations
   - Create CI/CD pipelines
   - Handle infrastructure as code

4. **Security Scanner Agent**
   - Scan for vulnerabilities
   - Check dependencies
   - Generate security reports

### Improvements

1. **Multi-Agent Collaboration**
   - Agents calling other agents
   - Task distribution
   - Result aggregation

2. **Learning and Adaptation**
   - Learn from feedback
   - Adapt to project patterns
   - Improve over time

3. **Interactive Mode**
   - Ask clarifying questions
   - Request confirmation
   - Provide progress updates

4. **Better MCP Integration**
   - More MCP servers
   - Deeper integrations
   - Real-time collaboration

## Troubleshooting

### Common Issues

1. **Agent Stuck in "Running" State**
   - Check AI API status
   - Review logs for errors
   - Manually mark as failed if needed

2. **Poor Quality Output**
   - Refine task description
   - Provide more context
   - Adjust temperature parameter

3. **Timeout Errors**
   - Reduce task complexity
   - Break into smaller tasks
   - Increase timeout limit

4. **High API Costs**
   - Use appropriate models
   - Cache when possible
   - Monitor usage

## Monitoring and Metrics

### Key Metrics

Track these metrics for each agent:

1. **Execution Metrics**
   - Average execution time
   - Success/failure rate
   - Queue depth

2. **Quality Metrics**
   - Output usefulness rating
   - Required manual corrections
   - User satisfaction

3. **Cost Metrics**
   - API cost per execution
   - Cost by agent type
   - Monthly spending

4. **Performance Metrics**
   - Token usage
   - Response time
   - Cache hit rate

## Conclusion

Code agents are powerful tools for increasing development productivity when used appropriately. They excel at generating boilerplate, reviewing code, creating tests, and writing documentation. However, human oversight remains essential for ensuring quality, security, and alignment with project goals.
