import React from 'react';
import { X, BookOpen, ExternalLink, Award } from 'lucide-react';
import { SourceReference } from '../../types';

interface SourcesModalProps {
  isOpen: boolean;
  onClose: () => void;
  sources: SourceReference[];
}

export const SourcesModal: React.FC<SourcesModalProps> = ({ isOpen, onClose, sources }) => {
  if (!isOpen || !sources || sources.length === 0) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm animate-fadeIn">
      <div className="bg-surface rounded-2xl max-w-2xl w-full max-h-[85vh] flex flex-col shadow-2xl border border-accent-border">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-accent-border">
          <div className="flex items-center space-x-2.5">
            <div className="p-2 bg-accent rounded-lg text-primary">
              <BookOpen className="w-5 h-5" />
            </div>
            <div>
              <h3 className="font-semibold text-textMain text-lg">Retrieved Knowledge Citations</h3>
              <p className="text-xs text-textMuted">
                {sources.length} clinical & wellness resource{sources.length > 1 ? 's' : ''} grounded this response
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-textMuted hover:text-textMain hover:bg-background transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content list */}
        <div className="p-6 overflow-y-auto space-y-4">
          {sources.map((src, index) => (
            <div
              key={index}
              className="p-4 rounded-xl border border-accent-border bg-background hover:border-secondary transition-all"
            >
              <div className="flex items-start justify-between mb-2">
                <div>
                  <span className="inline-block px-2 py-0.5 text-xs font-medium bg-accent text-primary rounded-full mb-1">
                    {src.category || 'Mental Wellness'}
                  </span>
                  <h4 className="font-semibold text-textMain text-base">{src.title}</h4>
                </div>
                <div className="flex items-center space-x-1 text-xs font-semibold px-2 py-1 bg-white rounded border border-accent-border text-primary">
                  <Award className="w-3.5 h-3.5" />
                  <span>Relevance: {Math.round(src.score * 100)}%</span>
                </div>
              </div>

              {src.author && (
                <p className="text-xs text-textMuted mb-2">
                  Source: <span className="font-medium text-textMain">{src.author}</span>
                </p>
              )}

              <p className="text-sm text-textMuted bg-surface p-3 rounded-lg border border-accent-border/50 leading-relaxed italic">
                "{src.snippet}"
              </p>

              {src.source_url && (
                <a
                  href={src.source_url}
                  target="_blank"
                  rel="noreferrer"
                  className="mt-3 inline-flex items-center space-x-1 text-xs font-medium text-primary hover:underline"
                >
                  <span>Visit original resource</span>
                  <ExternalLink className="w-3 h-3" />
                </a>
              )}
            </div>
          ))}
        </div>

        {/* Footer */}
        <div className="px-6 py-3 border-t border-accent-border bg-accent-soft flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-primary hover:bg-primary-hover text-white rounded-xl text-sm font-medium transition-colors"
          >
            Done
          </button>
        </div>
      </div>
    </div>
  );
};

