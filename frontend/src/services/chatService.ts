 import api from './api';
import { Session, Message } from '../types';

export const chatService = {
  async getSessions(): Promise<Session[]> {
    const response = await api.get<Session[]>('/chat/sessions');
    return response.data;
  },

  async createSession(): Promise<Session> {
    const response = await api.post<Session>('/chat/sessions');
    return response.data;
  },

  async getSession(sessionId: string): Promise<Session> {
    const response = await api.get<Session>(`/chat/sessions/${sessionId}`);
    return response.data;
  },

  async updateSessionTitle(sessionId: string, title: string): Promise<Session> {
    const response = await api.patch<Session>(`/chat/sessions/${sessionId}`, { title });
    return response.data;
  },

  async deleteSession(sessionId: string): Promise<void> {
    await api.delete(`/chat/sessions/${sessionId}`);
  },

  async sendMessage(message: string, sessionId?: string): Promise<Message> {
    const response = await api.post<Message>('/chat', {
      message,
      session_id: sessionId || null
    });
    return response.data;
  }
};
