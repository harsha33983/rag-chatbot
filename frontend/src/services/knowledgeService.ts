import api from './api';
import { KnowledgeStatus } from '../types';

export const knowledgeService = {
  async getStatus(): Promise<KnowledgeStatus> {
    const response = await api.get<KnowledgeStatus>('/knowledge/status');
    return response.data;
  },

  async reloadDefaultLibrary(): Promise<{ message: string; documents_processed: number; total_chunks: number }> {
    const response = await api.post('/knowledge/ingest', { reload_default_library: true });
    return response.data;
  },

  async uploadDocument(file: File, title?: string, category?: string): Promise<any> {
    const formData = new FormData();
    formData.append('file', file);
    if (title) formData.append('title', title);
    if (category) formData.append('category', category);

    const response = await api.post('/knowledge/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }
};

