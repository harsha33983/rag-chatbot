import api from './api';
import { User } from '../types';

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export const authService = {
  async register(name: string, email: string, password: string): Promise<AuthResponse> {
    const response = await api.post<AuthResponse>('/auth/register', { name, email, password });
    if (response.data.access_token) {
      localStorage.setItem('mindcare_token', response.data.access_token);
      localStorage.setItem('mindcare_user', JSON.stringify(response.data.user));
    }
    return response.data;
  },

  async login(email: string, password: string): Promise<AuthResponse> {
    const response = await api.post<AuthResponse>('/auth/login', { email, password });
    if (response.data.access_token) {
      localStorage.setItem('mindcare_token', response.data.access_token);
      localStorage.setItem('mindcare_user', JSON.stringify(response.data.user));
    }
    return response.data;
  },

  async logout(): Promise<void> {
    try {
      await api.post('/auth/logout');
    } finally {
      localStorage.removeItem('mindcare_token');
      localStorage.removeItem('mindcare_user');
    }
  },

  async getMe(): Promise<User> {
    const response = await api.get<User>('/auth/me');
    return response.data;
  },

  getCurrentUser(): User | null {
    const userStr = localStorage.getItem('mindcare_user');
    if (userStr) {
      try {
        return JSON.parse(userStr);
      } catch {
        return null;
      }
    }
    return null;
  },

  getToken(): string | null {
    return localStorage.getItem('mindcare_token');
  }
};

