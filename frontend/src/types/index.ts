export interface User {
  id: string;
  email: string;
  username: string;
  full_name?: string;
  created_at: string;
  updated_at?: string;
}

export interface Project {
  id: string;
  name: string;
  description?: string;
  repository_url: string;
  tech_stack: string[];
  status: 'active' | 'archived';
  created_by: string;
  created_at: string;
  updated_at?: string;
}

export interface AIActivity {
  id: string;
  project_id: string;
  tool_used: 'chatgpt' | 'claude' | 'copilot' | 'cursor';
  prompt: string;
  response?: string;
  code_changes: string[];
  timestamp: string;
  user_id: string;
  category: 'feature' | 'bugfix' | 'refactor' | 'docs' | 'test';
}

export interface AgentExecution {
  id: string;
  project_id: string;
  agent_type: string;
  task_description: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  input_data?: Record<string, unknown>;
  output_data?: Record<string, unknown>;
  started_at: string;
  completed_at?: string;
  error_message?: string;
}

export interface PipelineExecution {
  id: string;
  project_id: string;
  pipeline_name: string;
  status: 'running' | 'success' | 'failed';
  commit_sha: string;
  branch: string;
  triggered_by: string;
  started_at: string;
  completed_at?: string;
  test_results?: Record<string, unknown>;
  deployment_url?: string;
}

export interface MCPServer {
  id: string;
  name: string;
  server_type: 'github' | 'filesystem' | 'database' | 'http_api';
  endpoint: string;
  status: 'active' | 'inactive' | 'error';
  capabilities: string[];
  last_health_check: string;
}

export interface UsageAnalytics {
  total_prompts: number;
  prompts_by_tool: Record<string, number>;
  prompts_by_category: Record<string, number>;
  total_cost_estimate: number;
  avg_tokens_per_prompt: number;
  time_saved_hours: number;
}

export interface ProductivityMetrics {
  total_commits: number;
  lines_of_code_changed: number;
  ai_assisted_commits: number;
  ai_contribution_percentage: number;
  test_coverage: number;
  avg_build_time_minutes: number;
}

export interface PaginatedResponse<T> {
  data: T[];
  meta: {
    page: number;
    per_page: number;
    total: number;
    total_pages: number;
  };
}

export interface ErrorResponse {
  error: {
    message: string;
    code?: string;
    details?: Record<string, unknown>;
  };
}
