import React, { useState, useRef, useEffect } from 'react';
import { Send, Sparkles } from 'lucide-react';

interface MessageInputProps {
  onSend: (message: string) => void;
  isLoading: boolean;
  disabled?: boolean;
}

export const MessageInput: React.FC<MessageInputProps> = ({ onSend, isLoading, disabled }) => {
  const [text, setText] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 160)}px`;
    }
  }, [text]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleSubmit = () => {
    if (!text.trim() || isLoading || disabled) return;
    onSend(text.trim());
    setText('');
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  };

  return (
    <div className="border-t border-accent-border bg-surface/80 backdrop-blur-md px-4 py-3 md:px-8">
      <div className="max-w-4xl mx-auto">
        <div className="relative flex items-end bg-background border border-accent-border rounded-2xl p-2 focus-within:border-primary focus-within:ring-2 focus-within:ring-primary/20 transition-all shadow-sm">
          <textarea
            ref={textareaRef}
            value={text}
            onChange={(e) => setText(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Share what is on your mind, or ask about coping strategies..."
            rows={1}
            disabled={disabled || isLoading}
            className="flex-1 bg-transparent px-3 py-1.5 text-sm text-textMain placeholder-textMuted focus:outline-none resize-none max-h-40 leading-relaxed"
          />

          <button
            onClick={handleSubmit}
            disabled={!text.trim() || isLoading || disabled}
            className={`p-2.5 rounded-xl transition-all flex items-center justify-center flex-shrink-0 ${
              text.trim() && !isLoading
                ? 'bg-primary hover:bg-primary-hover text-white shadow-sm'
                : 'bg-accent text-textMuted/50 cursor-not-allowed'
            }`}
            title="Send message (Enter)"
          >
            {isLoading ? (
              <Sparkles className="w-4 h-4 animate-spin text-white" />
            ) : (
              <Send className="w-4 h-4" />
            )}
          </button>
        </div>

        <div className="flex items-center justify-between mt-2 px-1 text-[11px] text-textMuted">
          <span>Press <strong>Enter</strong> to send &bull; <strong>Shift + Enter</strong> for line break</span>
          <span>MindCare AI &bull; Grounded RAG Mental Wellness</span>
        </div>
      </div>
    </div>
  );
};

