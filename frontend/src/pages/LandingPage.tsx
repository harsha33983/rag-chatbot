import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { 
  Sparkles, 
  ShieldCheck, 
  BookOpen, 
  History, 
  HeartHandshake, 
  Lock, 
  ArrowRight,
  LifeBuoy
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export const LandingPage: React.FC = () => {
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-background flex flex-col selection:bg-secondary/30">
      {/* Navigation */}
      <header className="sticky top-0 z-30 bg-surface/90 backdrop-blur-md border-b border-accent-border px-6 py-4">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-2.5">
            <div className="w-9 h-9 rounded-xl bg-primary flex items-center justify-center text-white shadow-soft">
              <Sparkles className="w-5 h-5" />
            </div>
            <span className="font-bold text-xl text-textMain tracking-tight">MindCare AI</span>
          </div>

          <div className="flex items-center space-x-3">
            {isAuthenticated ? (
              <button
                onClick={() => navigate('/chat')}
                className="px-5 py-2.5 bg-primary hover:bg-primary-hover text-white rounded-xl text-sm font-semibold transition-all shadow-soft flex items-center space-x-2"
              >
                <span>Go to Dashboard</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            ) : (
              <>
                <Link
                  to="/login"
                  className="px-4 py-2 text-sm font-medium text-textMain hover:text-primary transition-colors"
                >
                  Sign In
                </Link>
                <Link
                  to="/register"
                  className="px-5 py-2.5 bg-primary hover:bg-primary-hover text-white rounded-xl text-sm font-semibold transition-all shadow-soft"
                >
                  Get Started Free
                </Link>
              </>
            )}
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <main className="flex-1">
        <section className="py-16 md:py-24 px-6 text-center max-w-4xl mx-auto">
          <div className="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-accent border border-accent-border text-primary text-xs font-semibold mb-6 shadow-sm">
            <HeartHandshake className="w-4 h-4" />
            <span>Curated RAG-Powered Mental Wellness</span>
          </div>

          <h1 className="text-4xl md:text-6xl font-extrabold text-textMain tracking-tight leading-tight md:leading-tight mb-6">
            Your Space to Talk, Reflect and Feel Heard.
          </h1>

          <p className="text-lg md:text-xl text-textMuted max-w-2xl mx-auto mb-10 leading-relaxed">
            An AI-powered mental wellness companion that offers supportive, empathetic conversations grounded in trusted, clinical knowledge.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <button
              onClick={() => navigate(isAuthenticated ? '/chat' : '/register')}
              className="w-full sm:w-auto px-8 py-3.5 bg-primary hover:bg-primary-hover text-white rounded-xl text-base font-semibold shadow-soft hover:shadow-lg transition-all flex items-center justify-center space-x-2"
            >
              <span>Start Conversation</span>
              <ArrowRight className="w-5 h-5" />
            </button>

            <Link
              to="/login"
              className="w-full sm:w-auto px-8 py-3.5 bg-surface border border-accent-border hover:border-secondary text-textMain rounded-xl text-base font-medium transition-all"
            >
              Sign In to Your History
            </Link>
          </div>

          {/* Quick reassurance */}
          <div className="mt-8 flex items-center justify-center space-x-6 text-xs text-textMuted">
            <span className="flex items-center space-x-1.5">
              <Lock className="w-3.5 h-3.5 text-primary" />
              <span>Private & Encrypted</span>
            </span>
            <span className="flex items-center space-x-1.5">
              <ShieldCheck className="w-3.5 h-3.5 text-primary" />
              <span>Multi-tier Crisis Safety Screening</span>
            </span>
            <span className="flex items-center space-x-1.5">
              <BookOpen className="w-3.5 h-3.5 text-primary" />
              <span>Grounded Knowledge Retrieval</span>
            </span>
          </div>
        </section>

        {/* Feature Highlights Grid */}
        <section className="py-16 px-6 bg-surface border-y border-accent-border">
          <div className="max-w-6xl mx-auto">
            <div className="text-center mb-14">
              <h2 className="text-2xl md:text-3xl font-bold text-textMain mb-3">
                Built for Safety, Empathy, and Scientific Grounding
              </h2>
              <p className="text-sm md:text-base text-textMuted max-w-xl mx-auto">
                Unlike generic chatbots, MindCare AI integrates clinically vetted psychoeducation with strict safety boundaries.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {/* Feature 1 */}
              <div className="p-6 rounded-2xl bg-background border border-accent-border shadow-card hover:border-primary transition-all">
                <div className="w-12 h-12 rounded-xl bg-accent flex items-center justify-center text-primary mb-4">
                  <BookOpen className="w-6 h-6" />
                </div>
                <h3 className="text-lg font-bold text-textMain mb-2">RAG Knowledge Retrieval</h3>
                <p className="text-sm text-textMuted leading-relaxed">
                  Every response is informed by a curated library of mental wellness resources, covering CBT restructuring, DBT distress tolerance, somatic grounding, and circadian sleep hygiene.
                </p>
              </div>

              {/* Feature 2 */}
              <div className="p-6 rounded-2xl bg-background border border-accent-border shadow-card hover:border-primary transition-all">
                <div className="w-12 h-12 rounded-xl bg-crisis-bg text-crisis-red mb-4">
                  <LifeBuoy className="w-6 h-6" />
                </div>
                <h3 className="text-lg font-bold text-textMain mb-2">Dedicated Crisis Screening</h3>
                <p className="text-sm text-textMuted leading-relaxed">
                  A mandatory pre-generation safety layer detects acute self-harm, suicidal ideation, and emergencies, instantly connecting users to emergency services (112 in India, 988 in the US/Canada).
                </p>
              </div>

              {/* Feature 3 */}
              <div className="p-6 rounded-2xl bg-background border border-accent-border shadow-card hover:border-primary transition-all">
                <div className="w-12 h-12 rounded-xl bg-accent flex items-center justify-center text-primary mb-4">
                  <History className="w-6 h-6" />
                </div>
                <h3 className="text-lg font-bold text-textMain mb-2">30-Turn Persistent Memory</h3>
                <p className="text-sm text-textMuted leading-relaxed">
                  PostgreSQL-backed multi-turn conversational history preserves context across multiple turns and sessions with strict user-level privacy and cryptographic isolation.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Safety & Medical Disclaimer Section */}
        <section className="py-14 px-6 max-w-4xl mx-auto">
          <div className="p-6 md:p-8 rounded-2xl bg-accent-soft border border-accent-border flex flex-col md:flex-row items-center gap-6">
            <div className="w-14 h-14 rounded-2xl bg-accent flex items-center justify-center text-primary flex-shrink-0">
              <ShieldCheck className="w-7 h-7" />
            </div>
            <div>
              <h3 className="text-lg font-bold text-textMain mb-1.5">
                Our Commitment to Ethical & Safe AI
              </h3>
              <p className="text-xs md:text-sm text-textMuted leading-relaxed">
                MindCare AI is an automated wellness companion designed for psychoeducation, reflection, and coping support. It does not provide medical diagnoses, prescribe medications, or replace professional psychiatric and clinical therapy. If you are experiencing a medical or psychological emergency, please contact <strong>112</strong> (India), <strong>988</strong> (USA/Canada), or your nearest emergency center.
              </p>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="bg-surface border-t border-accent-border py-8 px-6 text-center text-xs text-textMuted">
        <div className="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center space-x-2">
            <Sparkles className="w-4 h-4 text-primary" />
            <span className="font-semibold text-textMain">MindCare AI</span>
            <span>&bull; MVP 1.0</span>
          </div>
          <p>&copy; {new Date().getFullYear()} MindCare AI. Grounded Mental Wellness Companion.</p>
        </div>
      </footer>
    </div>
  );
};

