import React, { useState } from 'react';
import { Menu, Sparkles, AlertCircle, HeartHandshake } from 'lucide-react';
import { Sidebar } from '../components/Sidebar/Sidebar';
import { DisclaimerBanner } from '../components/Common/DisclaimerBanner';
import { MessageList } from '../components/Chat/MessageList';
import { MessageInput } from '../components/Chat/MessageInput';
import { useChat } from '../context/ChatContext';

export const ChatDashboard: React.FC = () => {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const { 
    messages, 
    activeSession, 
    sendMessage, 
    isSendingMessage, 
    error 
  } = useChat();

  const handleSend = (text: string) => {
    sendMessage(text);
  };

  const handleSelectStarter = (prompt: string) => {
    sendMessage(prompt);
  };

  return (
    <div className="flex h-screen overflow-hidden bg-background">
      {/* Sidebar */}
      <Sidebar isOpen={sidebarOpen} onToggle={() => setSidebarOpen(!sidebarOpen)} />

      {/* Main Chat Interface */}
      <div className={`flex-1 flex flex-col h-screen min-w-0 transition-all duration-300 ${sidebarOpen ? 'md:ml-80' : 'md:ml-0'}`}>
        {/* Top Navbar */}
        <header className="h-14 bg-surface border-b border-accent-border px-4 flex items-center justify-between flex-shrink-0 z-10 shadow-xs">
          <div className="flex items-center space-x-3 min-w-0">
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="p-2 rounded-xl text-textMuted hover:text-textMain hover:bg-background transition-colors"
              title="Toggle sidebar"
            >
              <Menu className="w-5 h-5" />
            </button>

            <div className="truncate">
              <h2 className="text-sm font-semibold text-textMain truncate">
                {activeSession?.title || 'New Conversation'}
              </h2>
              <p className="text-[10px] text-textMuted flex items-center space-x-1">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 inline-block" />
                <span>RAG Grounded &bull; Clinical Safety Active</span>
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-2">
            <div className="hidden sm:flex items-center space-x-1 px-2.5 py-1 rounded-full bg-accent text-primary text-xs font-medium">
              <HeartHandshake className="w-3.5 h-3.5" />
              <span>Safe Supportive Space</span>
            </div>
          </div>
        </header>

        {/* Global Safety & Clinical Disclaimer Banner */}
        <DisclaimerBanner />

        {/* Error notification if any */}
        {error && (
          <div className="mx-4 mt-2 p-3 bg-crisis-bg border border-crisis-border rounded-xl text-xs text-crisis-text flex items-center space-x-2">
            <AlertCircle className="w-4 h-4 flex-shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {/* Message Stream Area */}
        <MessageList
          messages={messages}
          isLoading={isSendingMessage}
          onSelectStarter={handleSelectStarter}
        />

        {/* Composer Area */}
        <MessageInput
          onSend={handleSend}
          isLoading={isSendingMessage}
        />
      </div>
    </div>
  );
};

