import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { Session, Message } from '../types';
import { chatService } from '../services/chatService';
import { useAuth } from './AuthContext';

interface ChatContextType {
  sessions: Session[];
  activeSessionId: string | null;
  activeSession: Session | null;
  messages: Message[];
  isLoadingSessions: boolean;
  isLoadingMessages: boolean;
  isSendingMessage: boolean;
  error: string | null;
  selectSession: (sessionId: string) => Promise<void>;
  startNewChat: () => void;
  sendMessage: (content: string) => Promise<void>;
  renameSession: (sessionId: string, newTitle: string) => Promise<void>;
  deleteSession: (sessionId: string) => Promise<void>;
  loadSessions: () => Promise<void>;
}

const ChatContext = createContext<ChatContextType | undefined>(undefined);

export const ChatProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated } = useAuth();
  const [sessions, setSessions] = useState<Session[]>([]);
  const [activeSessionId, setActiveSessionId] = useState<string | null>(null);
  const [activeSession, setActiveSession] = useState<Session | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoadingSessions, setIsLoadingSessions] = useState<boolean>(false);
  const [isLoadingMessages, setIsLoadingMessages] = useState<boolean>(false);
  const [isSendingMessage, setIsSendingMessage] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const loadSessions = useCallback(async () => {
    if (!isAuthenticated) return;
    setIsLoadingSessions(true);
    setError(null);
    try {
      const data = await chatService.getSessions();
      setSessions(data);
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Failed to load conversations.');
    } finally {
      setIsLoadingSessions(false);
    }
  }, [isAuthenticated]);

  useEffect(() => {
    if (isAuthenticated) {
      loadSessions();
    } else {
      setSessions([]);
      setActiveSessionId(null);
      setActiveSession(null);
      setMessages([]);
    }
  }, [isAuthenticated, loadSessions]);

  const selectSession = async (sessionId: string) => {
    setActiveSessionId(sessionId);
    setIsLoadingMessages(true);
    setError(null);
    try {
      const session = await chatService.getSession(sessionId);
      setActiveSession(session);
      setMessages(session.messages || []);
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Failed to retrieve conversation.');
    } finally {
      setIsLoadingMessages(false);
    }
  };

  const startNewChat = () => {
    setActiveSessionId(null);
    setActiveSession(null);
    setMessages([]);
    setError(null);
  };

  const sendMessage = async (content: string) => {
    if (!content.trim() || isSendingMessage) return;

    setError(null);
    const tempUserMsg: Message = {
      id: `temp-${Date.now()}`,
      session_id: activeSessionId || '',
      role: 'user',
      content: content.trim(),
      created_at: new Date().toISOString()
    };

    // Optimistically show user message
    setMessages((prev) => [...prev, tempUserMsg]);
    setIsSendingMessage(true);

    try {
      const assistantMsg = await chatService.sendMessage(content.trim(), activeSessionId || undefined);
      
      // Update session ID if this was a new conversation
      if (!activeSessionId) {
        setActiveSessionId(assistantMsg.session_id);
      }

      // Add assistant message and replace temp with authoritative state
      setMessages((prev) => [...prev, assistantMsg]);

      // Refresh sessions to show updated title and timestamp
      await loadSessions();
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'An error occurred while generating a response.');
    } finally {
      setIsSendingMessage(false);
    }
  };

  const renameSession = async (sessionId: string, newTitle: string) => {
    try {
      const updated = await chatService.updateSessionTitle(sessionId, newTitle);
      setSessions((prev) =>
        prev.map((s) => (s.id === sessionId ? { ...s, title: updated.title } : s))
      );
      if (activeSessionId === sessionId) {
        setActiveSession((prev) => (prev ? { ...prev, title: updated.title } : null));
      }
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Failed to rename conversation.');
    }
  };

  const deleteSession = async (sessionId: string) => {
    try {
      await chatService.deleteSession(sessionId);
      setSessions((prev) => prev.filter((s) => s.id !== sessionId));
      if (activeSessionId === sessionId) {
        startNewChat();
      }
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Failed to delete conversation.');
    }
  };

  return (
    <ChatContext.Provider
      value={{
        sessions,
        activeSessionId,
        activeSession,
        messages,
        isLoadingSessions,
        isLoadingMessages,
        isSendingMessage,
        error,
        selectSession,
        startNewChat,
        sendMessage,
        renameSession,
        deleteSession,
        loadSessions,
      }}
    >
      {children}
    </ChatContext.Provider>
  );
};

export const useChat = () => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
};

