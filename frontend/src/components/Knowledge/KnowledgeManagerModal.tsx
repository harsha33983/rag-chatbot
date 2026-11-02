import React, { useState, useEffect } from 'react';
import { X, Database, Upload, RefreshCw, FileText, CheckCircle2, AlertCircle } from 'lucide-react';
import { knowledgeService } from '../../services/knowledgeService';
import { KnowledgeStatus } from '../../types';

interface KnowledgeManagerModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const KnowledgeManagerModal: React.FC<KnowledgeManagerModalProps> = ({ isOpen, onClose }) => {
  const [status, setStatus] = useState<KnowledgeStatus | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isUploading, setIsUploading] = useState<boolean>(false);
  const [file, setFile] = useState<File | null>(null);
  const [title, setTitle] = useState('');
  const [category, setCategory] = useState('Anxiety & Stress');
  const [notification, setNotification] = useState<{ type: 'success' | 'error'; message: string } | null>(null);

  const fetchStatus = async () => {
    try {
      setIsLoading(true);
      const res = await knowledgeService.getStatus();
      setStatus(res);
    } catch {
      setNotification({ type: 'error', message: 'Failed to retrieve knowledge status.' });
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (isOpen) {
      fetchStatus();
      setNotification(null);
    }
  }, [isOpen]);

  const handleReloadDefaults = async () => {
    try {
      setIsLoading(true);
      setNotification(null);
      const res = await knowledgeService.reloadDefaultLibrary();
      setNotification({ type: 'success', message: res.message });
      await fetchStatus();
    } catch (err: any) {
      setNotification({ type: 'error', message: err?.response?.data?.detail || 'Failed to re-index knowledge.' });
    } finally {
      setIsLoading(false);
    }
  };

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;

    try {
      setIsUploading(true);
      setNotification(null);
      const res = await knowledgeService.uploadDocument(file, title || undefined, category);
      setNotification({ type: 'success', message: `Uploaded '${res.title}' (${res.chunks_created} chunks indexed).` });
      setFile(null);
      setTitle('');
      await fetchStatus();
    } catch (err: any) {
      setNotification({ type: 'error', message: err?.response?.data?.detail || 'Upload failed.' });
    } finally {
      setIsUploading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm animate-fadeIn">
      <div className="bg-surface rounded-2xl max-w-xl w-full max-h-[90vh] flex flex-col shadow-2xl border border-accent-border">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-accent-border">
          <div className="flex items-center space-x-2.5">
            <div className="p-2 bg-accent rounded-lg text-primary">
              <Database className="w-5 h-5" />
            </div>
            <div>
              <h3 className="font-semibold text-textMain text-lg">RAG Knowledge Base</h3>
              <p className="text-xs text-textMuted">Vector store management & mental wellness resources</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-textMuted hover:text-textMain hover:bg-background transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto space-y-5">
          {notification && (
            <div
              className={`p-3 rounded-xl flex items-center space-x-2 text-xs font-medium ${
                notification.type === 'success'
                  ? 'bg-accent text-primary border border-secondary'
                  : 'bg-crisis-bg text-crisis-text border border-crisis-border'
              }`}
            >
              {notification.type === 'success' ? <CheckCircle2 className="w-4 h-4 flex-shrink-0" /> : <AlertCircle className="w-4 h-4 flex-shrink-0" />}
              <span>{notification.message}</span>
            </div>
          )}

          {/* Status Box */}
          <div className="p-4 rounded-xl bg-background border border-accent-border">
            <div className="flex items-center justify-between mb-3">
              <span className="text-xs font-semibold text-textMuted uppercase tracking-wider">Vector Store Status</span>
              <button
                onClick={handleReloadDefaults}
                disabled={isLoading}
                className="inline-flex items-center space-x-1 text-xs text-primary hover:underline font-medium disabled:opacity-50"
              >
                <RefreshCw className={`w-3.5 h-3.5 ${isLoading ? 'animate-spin' : ''}`} />
                <span>Reload Curated Library</span>
              </button>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div className="bg-surface p-3 rounded-lg border border-accent-border/50">
                <span className="text-xs text-textMuted">Total Chunks</span>
                <p className="text-xl font-bold text-primary mt-0.5">{status?.total_vectors ?? '...'}</p>
              </div>
              <div className="bg-surface p-3 rounded-lg border border-accent-border/50">
                <span className="text-xs text-textMuted">Embedding Model</span>
                <p className="text-xs font-semibold text-textMain mt-1 truncate">all-MiniLM-L6-v2</p>
              </div>
            </div>

            {status?.sample_categories && status.sample_categories.length > 0 && (
              <div className="mt-3">
                <span className="text-xs text-textMuted block mb-1.5">Curated Topics Covered:</span>
                <div className="flex flex-wrap gap-1.5">
                  {status.sample_categories.map((cat, i) => (
                    <span key={i} className="text-[11px] bg-accent/60 text-textMain px-2 py-0.5 rounded-full border border-accent-border/50">
                      {cat}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Upload Document Form */}
          <form onSubmit={handleUpload} className="p-4 rounded-xl bg-background border border-accent-border space-y-3">
            <span className="text-xs font-semibold text-textMuted uppercase tracking-wider block">
              Upload New Wellness Document (PDF, TXT, MD)
            </span>

            <div>
              <label className="text-xs text-textMuted block mb-1">Resource Title (Optional)</label>
              <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="e.g., Mindful Walking Practice Guide"
                className="w-full px-3 py-2 bg-surface border border-accent-border rounded-lg text-sm text-textMain focus:outline-none focus:border-primary"
              />
            </div>

            <div>
              <label className="text-xs text-textMuted block mb-1">Category</label>
              <select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                className="w-full px-3 py-2 bg-surface border border-accent-border rounded-lg text-sm text-textMain focus:outline-none focus:border-primary"
              >
                <option value="Anxiety and Panic Management">Anxiety and Panic Management</option>
                <option value="Cognitive Behavioral Therapy">Cognitive Behavioral Therapy</option>
                <option value="Depression and Mood Regulation">Depression and Mood Regulation</option>
                <option value="Mindfulness and Somatic Practices">Mindfulness and Somatic Practices</option>
                <option value="Sleep and Circadian Health">Sleep and Circadian Health</option>
                <option value="Stress and Burnout">Stress and Burnout</option>
                <option value="Dialectical Behavior Therapy">Dialectical Behavior Therapy</option>
                <option value="Grief and Loss Support">Grief and Loss Support</option>
                <option value="Uploaded Resources">Uploaded Resources</option>
              </select>
            </div>

            <div>
              <label className="text-xs text-textMuted block mb-1">Select File</label>
              <input
                type="file"
                accept=".txt,.md,.pdf"
                onChange={(e) => setFile(e.target.files ? e.target.files[0] : null)}
                className="w-full text-xs text-textMuted file:mr-3 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-accent file:text-primary hover:file:bg-secondary/40 cursor-pointer"
              />
            </div>

            <button
              type="submit"
              disabled={!file || isUploading}
              className="w-full py-2 bg-primary hover:bg-primary-hover disabled:opacity-50 text-white rounded-xl text-sm font-medium transition-colors flex items-center justify-center space-x-1.5 mt-2"
            >
              {isUploading ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin" />
                  <span>Processing & Indexing...</span>
                </>
              ) : (
                <>
                  <Upload className="w-4 h-4" />
                  <span>Ingest into Vector DB</span>
                </>
              )}
            </button>
          </form>
        </div>

        {/* Footer */}
        <div className="px-6 py-3 border-t border-accent-border bg-accent-soft flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-surface hover:bg-background border border-accent-border text-textMain rounded-xl text-sm font-medium transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

