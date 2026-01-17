import { apiClient } from './api';
import { Project, PaginatedResponse } from '@/types';

interface ProjectCreate {
  name: string;
  description?: string;
  repository_url: string;
  tech_stack: string[];
}

interface ProjectUpdate {
  name?: string;
  description?: string;
  repository_url?: string;
  tech_stack?: string[];
  status?: 'active' | 'archived';
}

interface ProjectListParams {
  page?: number;
  per_page?: number;
  search?: string;
  status?: 'active' | 'archived';
}

export const projectService = {
  async list(params?: ProjectListParams): Promise<PaginatedResponse<Project>> {
    return apiClient.get<PaginatedResponse<Project>>('/projects', params);
  },

  async get(id: string): Promise<{ data: Project }> {
    return apiClient.get<{ data: Project }>(`/projects/${id}`);
  },

  async create(data: ProjectCreate): Promise<{ data: Project }> {
    return apiClient.post<{ data: Project }>('/projects', data);
  },

  async update(id: string, data: ProjectUpdate): Promise<{ data: Project }> {
    return apiClient.put<{ data: Project }>(`/projects/${id}`, data);
  },

  async delete(id: string): Promise<void> {
    return apiClient.delete<void>(`/projects/${id}`);
  },
};
