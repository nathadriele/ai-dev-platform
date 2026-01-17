import { apiClient } from './api';
import { UsageAnalytics, ProductivityMetrics } from '@/types';

interface UsageAnalyticsParams {
  project_id?: string;
  start_date?: string;
  end_date?: string;
}

interface ProductivityParams {
  project_id?: string;
}

export const analyticsService = {
  async getUsage(params?: UsageAnalyticsParams): Promise<{ data: UsageAnalytics }> {
    return apiClient.get<{ data: UsageAnalytics }>('/analytics/usage', params);
  },

  async getProductivity(params?: ProductivityParams): Promise<{ data: ProductivityMetrics }> {
    return apiClient.get<{ data: ProductivityMetrics }>('/analytics/productivity', params);
  },
};
