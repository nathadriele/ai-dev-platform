import { apiClient } from './api';
import { AgentExecution } from '@/types';

interface AgentExecutionCreate {
  project_id: string;
  agent_type: string;
  task_description: string;
  input_data?: Record<string, unknown>;
}

interface AgentType {
  id: string;
  name: string;
  description: string;
  capabilities: string[];
  requires_mcp_server: boolean;
}

export const agentService = {
  async execute(data: AgentExecutionCreate): Promise<{ data: AgentExecution }> {
    return apiClient.post<{ data: AgentExecution }>('/agents', data);
  },

  async get(id: string): Promise<{ data: AgentExecution }> {
    return apiClient.get<{ data: AgentExecution }>(`/agents/${id}`);
  },

  async listTypes(): Promise<{ data: AgentType[] }> {
    return apiClient.get<{ data: AgentType[] }>('/agents/types');
  },
};
