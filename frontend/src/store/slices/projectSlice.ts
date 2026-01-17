import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { projectService } from '@/services/projectService';
import { Project } from '@/types';

interface ProjectState {
  projects: Project[];
  currentProject: Project | null;
  isLoading: boolean;
  error: string | null;
  pagination: {
    page: number;
    per_page: number;
    total: number;
    total_pages: number;
  };
}

const initialState: ProjectState = {
  projects: [],
  currentProject: null,
  isLoading: false,
  error: null,
  pagination: {
    page: 1,
    per_page: 20,
    total: 0,
    total_pages: 0,
  },
};

export const fetchProjects = createAsyncThunk(
  'projects/fetchProjects',
  async (params?: { page?: number; per_page?: number; search?: string; status?: 'active' | 'archived' }) => {
    const response = await projectService.list(params);
    return response;
  }
);

export const fetchProject = createAsyncThunk(
  'projects/fetchProject',
  async (id: string) => {
    const response = await projectService.get(id);
    return response.data;
  }
);

export const createProject = createAsyncThunk(
  'projects/createProject',
  async (data: { name: string; description?: string; repository_url: string; tech_stack: string[] }) => {
    const response = await projectService.create(data);
    return response.data;
  }
);

const projectSlice = createSlice({
  name: 'projects',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    clearCurrentProject: (state) => {
      state.currentProject = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchProjects.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchProjects.fulfilled, (state, action) => {
        state.isLoading = false;
        state.projects = action.payload.data;
        state.pagination = action.payload.meta;
      })
      .addCase(fetchProjects.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.error.message || 'Failed to fetch projects';
      })
      .addCase(fetchProject.fulfilled, (state, action) => {
        state.currentProject = action.payload;
      })
      .addCase(createProject.fulfilled, (state, action) => {
        state.projects.unshift(action.payload);
      });
  },
});

export const { clearError, clearCurrentProject } = projectSlice.actions;
export default projectSlice.reducer;
