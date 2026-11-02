import React, { useState } from 'react';
import { 
  Plus, 
  MessageSquare, 
  Trash2, 
  Edit3, 
  Check, 
  X, 
  LogOut, 
  Database, 
  Sparkles,
  ChevronLeft,
  ChevronRight,
  User as UserIcon
} from 'lucide-react';
import { useChat } from '../../context/ChatContext';
import { useAuth } from '../../context/AuthContext';
import { KnowledgeManagerModal } from '../Knowledge/KnowledgeManagerModal';

interface SidebarProps {
  isOpen: boolean;
  onToggle: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ isOpen, onToggle }) => {
  const { 
    sessions, 
    activeSessionId, 
    selectSession, 
    startNewChat, 
    renameSession, 
    deleteSession,
    isLoadingSessions 
  } = useChat();
  const { user, logout } = useAuth();

  const [editingId, setEditingId] = useState<string | null>(null);
  const [editingTitle, setEditingTitle] = useState<string>('');
  const [showKnowledgeModal, setShowKnowledgeModal] = useState<boolean>(false);

  const handleStartRename = (id: string, currentTitle: string, e: React.MouseEvent) => {
    e.stopPropagation();
    setEditingId(id);
    setEditingTitle(currentTitle);
  };

  const handleSaveRename = async (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    if (editingTitle.trim()) {
      await renameSession(id, editingTitle.trim());
    }
    setEditingId(null);
  };

  const handleCancelRename = (e: React.MouseEvent) => {
    e.stopPropagation();
    setEditingId(null);
  };

  const handleDelete = async (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    if (window.confirm("Are you sure you want to delete this conversation?")) {
      await deleteSession(id);
    }
  };

  return (
    <>
      <aside
        className={`fixed inset-y-0 left-0 z-40 bg-surface border-r border-accent-border transition-all duration-300 ease-in-out flex flex-col ${
          isOpen ? 'w-72 md:w-80 translate-x-0' : 'w-72 -translate-x-full md:w-0 md:translate-x-0 md:hidden'
        }`}
      >
        {/* Brand Header */}
        <div className="p-4 border-b border-accent-border flex items-center justify-between">
          <div className="flex items-center space-x-2.5">
            <div className="w-9 h-9 rounded-xl bg-primary flex items-center justify-center text-white shadow-soft">
              <Sparkles className="w-5 h-5" />
            </div>
            <div>
              <h1 className="font-bold text-textMain text-base tracking-tight">MindCare AI</h1>
              <p className="text-[11px] text-textMuted">Empathetic RAG Companion</p>
            </div>
          </div>
          <button
            onClick={onToggle}
            className="md:hidden p-1.5 rounded-lg text-textMuted hover:bg-background hover:text-textMain transition-colors"
          >
            <ChevronLeft className="w-5 h-5" />
          </button>
        </div>

        {/* New Chat Button */}
        <div className="p-4">
          <button
            onClick={startNewChat}
            className="w-full py-2.5 px-4 bg-primary hover:bg-primary-hover text-white rounded-xl text-sm font-medium flex items-center justify-center space-x-2 shadow-soft transition-all"
          >
            <Plus className="w-4 h-4" />
            <span>New Conversation</span>
          </button>
        </div>

        {/* Conversation List */}
        <div className="flex-1 overflow-y-auto px-3 py-2 space-y-1">
          <div className="px-2 py-1 text-[11px] font-semibold text-textMuted uppercase tracking-wider">
            Recent Conversations
          </div>

          {isLoadingSessions && sessions.length === 0 ? (
            <div className="p-4 text-center text-xs text-textMuted">Loading sessions...</div>
          ) : sessions.length === 0 ? (
            <div className="p-4 text-center text-xs text-textMuted">No previous conversations. Start a new one!</div>
          ) : (
            sessions.map((sess) => {
              const isActive = sess.id === activeSessionId;
              const isEditing = sess.id === editingId;

              return (
                <div
                  key={sess.id}
                  onClick={() => selectSession(sess.id)}
                  className={`group relative flex items-center justify-between px-3 py-2.5 rounded-xl text-sm cursor-pointer transition-all ${
                    isActive
                      ? 'bg-accent text-textMain font-medium border border-secondary/50 shadow-sm'
                      : 'text-textMuted hover:bg-background hover:text-textMain'
                  }`}
                >
                  <div className="flex items-center space-x-2.5 flex-1 min-w-0 pr-2">
                    <MessageSquare className={`w-4 h-4 flex-shrink-0 ${isActive ? 'text-primary' : 'text-textMuted'}`} />

                    {isEditing ? (
                      <input
                        type="text"
                        value={editingTitle}
                        onChange={(e) => setEditingTitle(e.target.value)}
                        onClick={(e) => e.stopPropagation()}
                        onKeyDown={(e) => {
                          if (e.key === 'Enter') handleSaveRename(sess.id, e as any);
                          if (e.key === 'Escape') handleCancelRename(e as any);
                        }}
                        autoFocus
                        className="w-full text-xs bg-surface border border-primary px-1.5 py-0.5 rounded focus:outline-none"
                      />
                    ) : (
                      <span className="truncate text-xs md:text-sm">{sess.title}</span>
                    )}
                  </div>

                  {/* Actions: Rename / Delete */}
                  {isEditing ? (
                    <div className="flex items-center space-x-1">
                      <button
                        onClick={(e) => handleSaveRename(sess.id, e)}
                        className="p-1 text-primary hover:bg-white rounded transition-colors"
                        title="Save title"
                      >
                        <Check className="w-3.5 h-3.5" />
                      </button>
                      <button
                        onClick={handleCancelRename}
                        className="p-1 text-textMuted hover:bg-white rounded transition-colors"
                        title="Cancel"
                      >
                        <X className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  ) : (
                    <div className="opacity-0 group-hover:opacity-100 flex items-center space-x-1 transition-opacity">
                      <button
                        onClick={(e) => handleStartRename(sess.id, sess.title, e)}
                        className="p-1 text-textMuted hover:text-primary rounded transition-colors"
                        title="Rename"
                      >
                        <Edit3 className="w-3.5 h-3.5" />
                      </button>
                      <button
                        onClick={(e) => handleDelete(sess.id, e)}
                        className="p-1 text-textMuted hover:text-crisis-red rounded transition-colors"
                        title="Delete"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  )}
                </div>
              );
            })
          )}
        </div>

        {/* Footer: Knowledge Base Management & User Profile */}
        <div className="p-3 border-t border-accent-border space-y-2 bg-accent-soft">
          <button
            onClick={() => setShowKnowledgeModal(true)}
            className="w-full flex items-center space-x-2.5 px-3 py-2 rounded-xl text-xs font-medium text-textMain hover:bg-surface border border-accent-border/50 transition-all"
          >
            <Database className="w-4 h-4 text-primary" />
            <span>Knowledge Base & Ingestion</span>
          </button>

          <div className="flex items-center justify-between pt-1">
            <div className="flex items-center space-x-2 min-w-0">
              <div className="w-8 h-8 rounded-full bg-secondary flex items-center justify-center text-textMain text-xs font-bold">
                {user?.name ? user.name[0].toUpperCase() : 'U'}
              </div>
              <div className="truncate">
                <p className="text-xs font-semibold text-textMain truncate">{user?.name || 'User'}</p>
                <p className="text-[10px] text-textMuted truncate">{user?.email}</p>
              </div>
            </div>

            <button
              onClick={logout}
              className="p-1.5 text-textMuted hover:text-crisis-red rounded-lg hover:bg-surface transition-colors"
              title="Logout"
            >
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        </div>
      </aside>

      {/* Backdrop for mobile */}
      {isOpen && (
        <div
          onClick={onToggle}
          className="fixed inset-0 z-30 bg-black/30 backdrop-blur-xs md:hidden"
        />
      )}

      {/* Knowledge Base Modal */}
      <KnowledgeManagerModal
        isOpen={showKnowledgeModal}
        onClose={() => setShowKnowledgeModal(false)}
      />
    </>
  );
};

