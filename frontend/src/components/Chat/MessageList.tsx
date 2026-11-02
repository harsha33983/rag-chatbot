import React, { useEffect, useRef } from 'react';
import { Sparkles, Compass, Shield, Wind, Moon, HeartHandshake } from 'lucide-react';
import { Message } from '../../types';
import { MessageItem } from './MessageItem';

interface MessageListProps {
  messages: Message[];
  isLoading: boolean;
  onSelectStarter: (text: string) => void;
}

const STARTER_PROMPTS = [
  {
    icon: Wind,
    title: "Grounding Exercise",
    prompt: "I'm feeling anxious right now. Can you guide me through the 5-4-3-2-1 somatic grounding technique?"
  },
  {
    icon: Moon,
    title: "Sleep Hygiene",
    prompt: "I've been struggling to fall asleep lately. What evidence-based sleep hygiene tips can help reset my circadian rhythm?"
  },
  {
    icon: Compass,
    title: "CBT Restructuring",
    prompt: "How can I identify and challenge cognitive distortions like catastrophizing when I have negative thoughts?"
  },
  {
    icon: HeartHandshake,
    title: "Burnout Support",
    prompt: "I feel completely exhausted and burned out by work. How do I establish healthy cognitive boundaries?"
  }
];

export const MessageList: React.FC<MessageListProps> = ({ messages, isLoading, onSelectStarter }) => {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  if (messages.length === 0) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center p-6 text-center max-w-3xl mx-auto my-auto animate-fadeIn">
        {/* Brand Icon */}
        <div className="w-16 h-16 rounded-2xl bg-accent flex items-center justify-center text-primary mb-5 shadow-soft">
          <Sparkles className="w-8 h-8" />
        </div>

        <h2 className="text-2xl font-bold text-textMain mb-2">Welcome to MindCare AI</h2>
        <p className="text-sm text-textMuted max-w-lg mb-6 leading-relaxed">
          Hello! I'm MindCare AI. I'm here to listen and help you explore your thoughts in a calm, non-judgmental space grounded in trusted mental wellness knowledge.
        </p>

        {/* Safety Disclaimer pill */}
        <div className="flex items-center space-x-2 text-xs text-textMuted bg-surface border border-accent-border px-4 py-2 rounded-full mb-8 shadow-sm">
          <Shield className="w-4 h-4 text-primary" />
          <span>Automated wellness companion &bull; Not a clinical substitute &bull; Emergency 112 (India) / 988 (USA)</span>
        </div>

        {/* Conversation Starters Grid */}
        <div className="w-full">
          <p className="text-xs font-semibold text-textMuted uppercase tracking-wider mb-3">
            Suggested Conversation Starters
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-left">
            {STARTER_PROMPTS.map((starter, i) => {
              const Icon = starter.icon;
              return (
                <button
                  key={i}
                  onClick={() => onSelectStarter(starter.prompt)}
                  className="p-4 rounded-xl bg-surface border border-accent-border hover:border-primary hover:shadow-soft transition-all text-left flex items-start space-x-3 group"
                >
                  <div className="p-2 rounded-lg bg-accent text-primary group-hover:bg-primary group-hover:text-white transition-colors">
                    <Icon className="w-4 h-4" />
                  </div>
                  <div>
                    <h4 className="text-sm font-semibold text-textMain group-hover:text-primary transition-colors">
                      {starter.title}
                    </h4>
                    <p className="text-xs text-textMuted line-clamp-2 mt-0.5">
                      {starter.prompt}
                    </p>
                  </div>
                </button>
              );
            })}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto px-4 md:px-8 py-6 space-y-2">
      {messages.map((msg) => (
        <MessageItem key={msg.id} message={msg} />
      ))}

      {/* Typing Indicator */}
      {isLoading && (
        <div className="flex items-start max-w-3xl space-x-3 my-4">
          <div className="w-9 h-9 rounded-full bg-primary text-white flex items-center justify-center flex-shrink-0 shadow-sm">
            <Sparkles className="w-4 h-4" />
          </div>
          <div className="bg-surface border border-accent-border rounded-2xl rounded-tl-none px-5 py-3.5 shadow-card flex items-center space-x-2">
            <div className="flex space-x-1.5">
              <div className="w-2 h-2 rounded-full bg-primary/70 animate-bounce" style={{ animationDelay: '0ms' }} />
              <div className="w-2 h-2 rounded-full bg-primary/70 animate-bounce" style={{ animationDelay: '150ms' }} />
              <div className="w-2 h-2 rounded-full bg-primary/70 animate-bounce" style={{ animationDelay: '300ms' }} />
            </div>
            <span className="text-xs text-textMuted ml-2">MindCare AI is reflecting & retrieving knowledge...</span>
          </div>
        </div>
      )}

      <div ref={bottomRef} />
    </div>
  );
};

