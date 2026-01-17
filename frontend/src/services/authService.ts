import { apiClient } from './api';
import { User } from '@/types';

interface LoginData {
  email: string;
  password: string;
}

interface RegisterData {
  email: string;
  password: string;
  username: string;
  full_name?: string;
}

interface AuthResponse {
  data: User;
  tokens: {
    access_token: string;
    refresh_token: string;
  };
}

interface TokenRefreshResponse {
  access_token: string;
}

export const authService = {
  async login(data: LoginData): Promise<AuthResponse> {
    const response = await apiClient.post<AuthResponse>('/auth/login', data);
    // Store tokens
    localStorage.setItem('access_token', response.tokens.access_token);
    localStorage.setItem('refresh_token', response.tokens.refresh_token);
    return response;
  },

  async register(data: RegisterData): Promise<AuthResponse> {
    const response = await apiClient.post<AuthResponse>('/auth/register', data);
    // Store tokens
    localStorage.setItem('access_token', response.tokens.access_token);
    localStorage.setItem('refresh_token', response.tokens.refresh_token);
    return response;
  },

  async refreshToken(refreshToken: string): Promise<TokenRefreshResponse> {
    const response = await apiClient.post<TokenRefreshResponse>('/auth/refresh', {
      refresh_token: refreshToken,
    });
    // Update access token
    localStorage.setItem('access_token', response.access_token);
    return response;
  },

  logout(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  },

  isAuthenticated(): boolean {
    return !!localStorage.getItem('access_token');
  },
};
