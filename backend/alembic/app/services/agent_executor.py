"""
Real Agent Executor - Executes AI agents with actual AI API calls
"""
import os
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.ai_client import AIClient
from app.services.github_service import GitHubService
from app.models.agent import AgentExecution, AgentStatus
from app.models.ai_activity import AIActivity, AITool, ActivityCategory
import uuid
import json


class AgentExecutor:
    """Execute AI agents with real AI model calls."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.ai_client = AIClient()

    async def execute_code_scaffolder(
        self,
        execution: AgentExecution,
        project_name: str,
        tech_stack: List[str],
        feature_description: str
    ) -> Dict[str, Any]:
        """Execute Code Scaffolder agent."""
        prompt = f"""Generate project structure and boilerplate code for:

Project Name: {project_name}
Tech Stack: {', '.join(tech_stack)}
Feature: {feature_description}

Please provide:
1. Recommended directory structure
2. Boilerplate code for main files
3. Configuration files needed
4. Installation instructions

Format as JSON with keys: structure, files, config, instructions."""

        response = await self.ai_client.call_model(
            prompt=prompt,
            provider="anthropic",
            model="claude-3-sonnet-20240229",
            max_tokens=3000
        )

        return {
            "agent_type": "code-scaffolder",
            "result": response,
            "structured_output": self._parse_code_scaffolder_output(response)
        }

    async def execute_code_reviewer(
        self,
        execution: AgentExecution,
        code_content: str,
        file_path: str
    ) -> Dict[str, Any]:
        """Execute Code Reviewer agent."""
        prompt = f"""Review this code for bugs, security issues, and best practices:

File: {file_path}

Code:
```python
{code_content}
```

Please analyze:
1. Security vulnerabilities
2. Bugs or logic errors
3. Performance issues
4. Code quality and best practices
5. Suggestions for improvement

Provide specific line references and code examples."""

        response = await self.ai_client.call_model(
            prompt=prompt,
            provider="anthropic",
            model="claude-3-sonnet-20240229",
            max_tokens=2000
        )

        return {
            "agent_type": "code-reviewer",
            "result": response,
            "structured_output": self._parse_review_output(response)
        }

    async def execute_test_generator(
        self,
        execution: AgentExecution,
        code_content: str,
        file_path: str
    ) -> Dict[str, Any]:
        """Execute Test Generator agent."""
        prompt = f"""Generate comprehensive tests for this code:

File: {file_path}

Code:
```python
{code_content}
```

Generate:
1. Unit tests for all functions
2. Edge case tests
3. Integration test example
4. Fixtures if needed
5. Instructions for running tests

Use pytest framework. Include proper assertions and comments."""

        response = await self.ai_client.call_model(
            prompt=prompt,
            provider="anthropic",
            model="claude-3-sonnet-20240229",
            max_tokens=3000
        )

        return {
            "agent_type": "test-generator",
            "result": response,
            "structured_output": self._parse_test_output(response)
        }

    async def execute_doc_generator(
        self,
        execution: AgentExecution,
        code_content: str,
        file_path: str,
        context: str = ""
    ) -> Dict[str, Any]:
        """Execute Documentation Generator agent."""
        prompt = f"""Generate technical documentation for this code:

File: {file_path}

Context: {context}

Code:
```python
{code_content}
```

Provide:
1. Overview of what the code does
2. Parameters and return types
3. Usage examples
4. Dependencies
5. Notes on implementation

Format in Markdown."""

        response = await self.ai_client.call_model(
            prompt=prompt,
            provider="anthropic",
            model="claude-3-sonnet-20240229",
            max_tokens=2000
        )

        return {
            "agent_type": "doc-generator",
            "result": response,
            "structured_output": {
                "documentation": response,
                "format": "markdown"
            }
        }

    async def execute_with_github_context(
        self,
        execution: AgentExecution,
        repo_url: str
    ) -> Dict[str, Any]:
        """Execute agent with GitHub context."""
        # Parse repo URL
        github_service = GitHubService()
        owner, repo = await github_service.parse_repository_url(repo_url)

        # Get recent commits
        commits = await github_service.get_repo_commits(owner, repo, per_page=5)

        # Analyze with AI
        prompt = f"""Analyze these recent commits from {owner}/{repo}:

{json.dumps(commits, indent=2)}

Provide:
1. Summary of changes
2. Potential issues or improvements
3. Suggestions for next steps
4. Code quality assessment"""

        response = await self.ai_client.call_model(
            prompt=prompt,
            provider="anthropic",
            max_tokens=2000
        )

        return {
            "agent_type": "github-analyzer",
            "result": response,
            "github_context": {
                "repo": f"{owner}/{repo}",
                "commits_analyzed": len(commits)
            }
        }

    async def run_agent(
        self,
        agent_type: str,
        project_id: str,
        task_description: str,
        input_data: Dict[str, Any]
    ) -> AgentExecution:
        """Main method to execute any agent."""
        # Create execution record
        execution = AgentExecution(
            id=uuid.uuid4(),
            project_id=project_id,
            agent_type=agent_type,
            task_description=task_description,
            status=AgentStatus.RUNNING,
            input_data=input_data,
        )
        self.db.add(execution)
        await self.db.commit()

        try:
            # Route to appropriate agent
            if agent_type == "code-scaffolder":
                result = await self.execute_code_scaffolder(
                    execution,
                    **input_data
                )
            elif agent_type == "code-reviewer":
                result = await self.execute_code_reviewer(
                    execution,
                    **input_data
                )
            elif agent_type == "test-generator":
                result = await self.execute_test_generator(
                    execution,
                    **input_data
                )
            elif agent_type == "doc-generator":
                result = await self.execute_doc_generator(
                    execution,
                    **input_data
                )
            elif agent_type == "github-analyzer":
                result = await self.execute_with_github_context(
                    execution,
                    **input_data
                )
            else:
                raise ValueError(f"Unknown agent type: {agent_type}")

            # Update execution as completed
            execution.status = AgentStatus.COMPLETED
            execution.output_data = result
            execution.completed_at = datetime.utcnow()

            # Log AI activity
            await self._log_agent_activity(execution, result)

            await self.db.commit()
            await self.db.refresh(execution)

            return execution

        except Exception as e:
            # Mark as failed
            execution.status = AgentStatus.FAILED
            execution.error_message = str(e)
            execution.completed_at = datetime.utcnow()
            await self.db.commit()
            raise

    async def _log_agent_activity(
        self,
        execution: AgentExecution,
        result: Dict[str, Any]
    ):
        """Log agent execution as AI activity."""
        activity = AIActivity(
            id=uuid.uuid4(),
            project_id=execution.project_id,
            tool_used=AITool.CLAUDE,
            prompt=execution.task_description,
            response=result.get("result", ""),
            code_changes=result.get("structured_output", {}).get("files_modified", []),
            timestamp=datetime.utcnow(),
            user_id=execution.project_id,  # TODO: Get actual user
            category=ActivityCategory.FEATURE,
        )
        self.db.add(activity)
        await self.db.commit()

    def _parse_code_scaffolder_output(self, output: str) -> Dict:
        """Parse code scaffolder output."""
        # Try to extract JSON from output
        try:
            import json
            start = output.find('{')
            end = output.rfind('}') + 1
            if start != -1 and end > start:
                return json.loads(output[start:end])
        except:
            pass
        return {"raw_output": output}

    def _parse_review_output(self, output: str) -> Dict:
        """Parse code review output."""
        return {
            "review": output,
            "issues_found": output.lower().count("issue"),
            "suggestions": output.lower().count("suggest")
        }

    def _parse_test_output(self, output: str) -> Dict:
        """Parse test generator output."""
        import re
        test_count = len(re.findall(r'def test_', output))
        return {
            "test_code": output,
            "test_count": test_count
        }
