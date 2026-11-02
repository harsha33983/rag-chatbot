import React, { useState } from 'react';
import { Copy, Check, BookOpen, AlertTriangle, Sparkles, User as UserIcon } from 'lucide-react';
import { Message } from '../../types';
import { SourcesModal } from './SourcesModal';

interface MessageItemProps {
  message: Message;
}

export const MessageItem: React.FC<MessageItemProps> = ({ message }) => {
  const [copied, setCopied] = useState(false);
  const [showSources, setShowSources] = useState(false);
  const isUser = message.role === 'user';
  const isCrisis = message.is_crisis;

  const handleCopy = () => {
    navigator.clipboard.writeText(message.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const formattedTime = new Date(message.created_at).toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit'
  });

  // Render markdown with basic formatting
  const renderFormattedContent = (content: string) => {
    const lines = content.split('\n');
    return lines.map((line, idx) => {
      // Headers
      if (line.startsWith('### ')) {
        return <h3 key={idx} className="text-base font-semibold text-textMain mt-3 mb-1">{line.replace('### ', '')}</h3>;
      }
      if (line.startsWith('## ')) {
        return <h2 key={idx} className="text-lg font-bold text-textMain mt-3 mb-1">{line.replace('## ', '')}</h2>;
      }
      // Bullet items
      if (line.trim().startsWith('- ') || line.trim().startsWith('* ')) {
        const clean = line.trim().substring(2);
        return (
          <li key={idx} className="ml-4 list-disc text-sm leading-relaxed my-0.5">
            {renderInlineMarkdown(clean)}
          </li>
        );
      }
      // Numbered items
      const numberedMatch = line.trim().match(/^(\d+)\.\s+(.*)/);
      if (numberedMatch) {
        return (
          <div key={idx} className="flex items-start space-x-2 my-1 text-sm leading-relaxed">
            <span className="font-semibold text-primary">{numberedMatch[1]}.</span>
            <span>{renderInlineMarkdown(numberedMatch[2])}</span>
          </div>
        );
      }
      // Empty line
      if (!line.trim()) {
        return <div key={idx} className="h-2" />;
      }
      // Standard paragraph
      return (
        <p key={idx} className="text-sm leading-relaxed my-1">
          {renderInlineMarkdown(line)}
        </p>
      );
    });
  };

  const renderInlineMarkdown = (text: string) => {
    // Bold **text**
    const parts = text.split(/(\*\*.*?\*\*)/g);
    return parts.map((part, i) => {
      if (part.startsWith('**') && part.endsWith('**')) {
        return <strong key={i} className="font-semibold">{part.slice(2, -2)}</strong>;
      }
      return part;
    });
  };

  return (
    <>
      <div className={`flex w-full my-4 ${isUser ? 'justify-end' : 'justify-start'}`}>
        <div className={`flex items-start max-w-3xl space-x-3 ${isUser ? 'flex-row-reverse space-x-reverse' : 'flex-row'}`}>
          {/* Avatar */}
          <div
            className={`w-9 h-9 rounded-full flex items-center justify-center flex-shrink-0 shadow-sm ${
              isUser
                ? 'bg-secondary text-textMain'
                : isCrisis
                ? 'bg-crisis-red text-white'
                : 'bg-primary text-white'
            }`}
          >
            {isUser ? (
              <UserIcon className="w-4 h-4" />
            ) : isCrisis ? (
              <AlertTriangle className="w-4 h-4" />
            ) : (
              <Sparkles className="w-4 h-4" />
            )}
          </div>

          {/* Message Bubble Container */}
          <div className="flex flex-col">
            <div
              className={`rounded-2xl px-5 py-4 shadow-card transition-all ${
                isUser
                  ? 'bg-primary text-white rounded-tr-none'
                  : isCrisis
                  ? 'bg-crisis-bg border border-crisis-border text-crisis-text rounded-tl-none'
                  : 'bg-surface border border-accent-border text-textMain rounded-tl-none'
              }`}
            >
              <div className="markdown-content">{renderFormattedContent(message.content)}</div>

              {/* Source citations pill & adapted tone badge */}
              {!isUser && (
                <div className="mt-3 pt-3 border-t border-accent-border/70 flex flex-wrap items-center gap-2">
                  {message.sources && message.sources.length > 0 && (
                    <button
                      onClick={() => setShowSources(true)}
                      className="inline-flex items-center space-x-1.5 px-3 py-1 bg-accent text-primary hover:bg-secondary/40 rounded-full text-xs font-medium transition-colors"
                    >
                      <BookOpen className="w-3.5 h-3.5" />
                      <span>View Grounded Citations ({message.sources.length})</span>
                    </button>
                  )}

                  {message.sentiment && (message.sentiment.tone_strategy || message.sentiment.label) && (
                    <span
                      title="Tone adapted dynamically based on 6-class sentiment screening (non-clinical wellness support)"
                      className="inline-flex items-center space-x-1 px-2.5 py-1 bg-secondary text-textMain border border-accent-border rounded-full text-[11px] font-medium"
                    >
                      <Sparkles className="w-3 h-3 text-primary" />
                      <span>Adapted Tone: {message.sentiment.tone_strategy || message.sentiment.label}</span>
                    </span>
                  )}
                </div>
              )}
            </div>

            {/* Bubble Footer: Timestamp & Copy */}
            <div className={`flex items-center space-x-2 mt-1 px-1 text-xs text-textMuted ${isUser ? 'justify-end' : 'justify-start'}`}>
              {isUser && message.sentiment && message.sentiment.label && (
                <span className="text-[11px] text-textMuted italic mr-1">
                  Emotion detected: {message.sentiment.label} ({Math.round((message.sentiment.confidence || 0) * 100)}%)
                </span>
              )}
              <span>{formattedTime}</span>
              {!isUser && (
                <button
                  onClick={handleCopy}
                  className="p-1 hover:text-textMain rounded transition-colors flex items-center space-x-1"
                  title="Copy message"
                >
                  {copied ? (
                    <>
                      <Check className="w-3.5 h-3.5 text-primary" />
                      <span className="text-[10px] text-primary">Copied</span>
                    </>
                  ) : (
                    <Copy className="w-3.5 h-3.5" />
                  )}
                </button>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Sources modal if opened */}
      {message.sources && (
        <SourcesModal
          isOpen={showSources}
          onClose={() => setShowSources(false)}
          sources={message.sources}
        />
      )}
    </>
  );
};

