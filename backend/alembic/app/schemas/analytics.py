from pydantic import BaseModel
from typing import Dict


class UsageAnalytics(BaseModel):
    """Usage analytics schema."""
    total_prompts: int
    prompts_by_tool: Dict[str, int]
    prompts_by_category: Dict[str, int]
    total_cost_estimate: float
    avg_tokens_per_prompt: float
    time_saved_hours: float


class ProductivityMetrics(BaseModel):
    """Productivity metrics schema."""
    total_commits: int
    lines_of_code_changed: int
    ai_assisted_commits: int
    ai_contribution_percentage: float
    test_coverage: float
    avg_build_time_minutes: float
