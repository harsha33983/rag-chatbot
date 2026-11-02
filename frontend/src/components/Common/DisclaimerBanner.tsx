import React, { useState } from 'react';
import { ShieldAlert, X, PhoneCall } from 'lucide-react';

export const DisclaimerBanner: React.FC = () => {
  const [dismissed, setDismissed] = useState(false);

  if (dismissed) return null;

  return (
    <div className="bg-accent-soft border-b border-accent-border px-4 py-2.5 text-xs md:text-sm text-textMain flex items-center justify-between transition-all">
      <div className="flex items-center space-x-2 max-w-5xl mx-auto">
        <ShieldAlert className="w-4 h-4 text-primary flex-shrink-0" />
        <span>
          <strong>MindCare AI is an educational wellness companion</strong>, not a clinical healthcare provider or substitute for professional medical therapy. If you are experiencing an acute crisis, dial <strong>112</strong> (India) or <strong>988</strong> (USA/Canada).
        </span>
      </div>
      <button
        onClick={() => setDismissed(true)}
        className="p-1 text-textMuted hover:text-textMain rounded transition-colors ml-2"
        title="Dismiss notice"
      >
        <X className="w-4 h-4" />
      </button>
    </div>
  );
};

