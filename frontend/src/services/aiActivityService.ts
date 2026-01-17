import { apiClient } from './api';
import { AIActivity, PaginatedResponse } from '@/types';

interface AIActivityCreate {
  project_id: string;
  tool_used: 'chatgpt' | 'claude' | 'copilot' | 'cursor';
  prompt: string;
  response?: string;
  code_changes?: string[];
  category: 'feature' | 'bugfix' | 'refactor' | 'docs' | 'test';
}

interface AIActivityListParams {
  page?: number;
  per_page?: number;
  project_id?: string;
  tool_used?: 'chatgpt' | 'claude' | 'copilot' | 'cursor';
  category?: 'feature' | 'bugfix' | 'refactor' | 'docs' | 'test';
}

export const aiActivityService = {
  async list(params?: AIActivityListParams): Promise<PaginatedResponse<AIActivity>> {
    return apiClient.get<PaginatedResponse<AIActivity>>('/ai-activities', params);
  },

  async get(id: string): Promise<{ data: AIActivity }> {
    return apiClient.get<{ data: AIActivity }>(`/ai-activities/${id}`);
  },

  async create(data: AIActivityCreate): Promise<{ data: AIActivity }> {
    return apiClient.post<{ data: AIActivity }>('/ai-activities', data);
  },
};
