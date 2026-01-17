import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { aiActivityService } from '@/services/aiActivityService';
import { AIActivity } from '@/types';

interface AIActivityState {
  activities: AIActivity[];
  isLoading: boolean;
  error: string | null;
  pagination: {
    page: number;
    per_page: number;
    total: number;
    total_pages: number;
  };
}

const initialState: AIActivityState = {
  activities: [],
  isLoading: false,
  error: null,
  pagination: {
    page: 1,
    per_page: 20,
    total: 0,
    total_pages: 0,
  },
};

export const fetchAIActivities = createAsyncThunk(
  'aiActivities/fetchAIActivities',
  async (params?: {
    page?: number;
    per_page?: number;
    project_id?: string;
    tool_used?: 'chatgpt' | 'claude' | 'copilot' | 'cursor';
    category?: 'feature' | 'bugfix' | 'refactor' | 'docs' | 'test';
  }) => {
    const response = await aiActivityService.list(params);
    return response;
  }
);

export const logAIActivity = createAsyncThunk(
  'aiActivities/logAIActivity',
  async (data: {
    project_id: string;
    tool_used: 'chatgpt' | 'claude' | 'copilot' | 'cursor';
    prompt: string;
    response?: string;
    code_changes?: string[];
    category: 'feature' | 'bugfix' | 'refactor' | 'docs' | 'test';
  }) => {
    const response = await aiActivityService.create(data);
    return response.data;
  }
);

const aiActivitySlice = createSlice({
  name: 'aiActivities',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchAIActivities.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchAIActivities.fulfilled, (state, action) => {
        state.isLoading = false;
        state.activities = action.payload.data;
        state.pagination = action.payload.meta;
      })
      .addCase(fetchAIActivities.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.error.message || 'Failed to fetch AI activities';
      })
      .addCase(logAIActivity.fulfilled, (state, action) => {
        state.activities.unshift(action.payload);
      });
  },
});

export const { clearError } = aiActivitySlice.actions;
export default aiActivitySlice.reducer;
