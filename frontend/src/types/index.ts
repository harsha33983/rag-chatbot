export interface User {
  id: string;
  name: string;
  email: string;
  created_at: string;
}

export interface SourceReference {
  document_id: string;
  title: string;
  category?: string;
  author?: string;
  source_url?: string;
  snippet: string;
  score: number;
}

export interface Message {
  id: string;
  session_id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: SourceReference[];
  is_crisis?: boolean;
  created_at: string;
}

export interface Session {
  id: string;
  user_id: string;
  title: string;
  created_at: string;
  updated_at: string;
  messages?: Message[];
}

export interface KnowledgeStatus {
  total_vectors: number;
  collection_name: string;
  embedding_model: string;
  status: string;
  sample_categories: string[];
}

