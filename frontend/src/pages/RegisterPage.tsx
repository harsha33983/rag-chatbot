import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Sparkles, Lock, Mail, User, ArrowRight, AlertCircle } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export const RegisterPage: React.FC = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const { register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name || !email || !password || !confirmPassword) {
      setError('Please fill in all fields.');
      return;
    }

    if (password !== confirmPassword) {
      setError('Passwords do not match.');
      return;
    }

    if (password.length < 6) {
      setError('Password must be at least 6 characters.');
      return;
    }

    try {
      setIsSubmitting(true);
      setError(null);
      await register(name.trim(), email.trim(), password);
      navigate('/chat');
    } catch (err: any) {
      if (!err.response) {
        setError('Cannot connect to backend server. Please verify the backend is running at http://127.0.0.1:8000.');
      } else {
        setError(err.response.data?.detail || 'Registration failed. Email might already be registered.');
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-background flex flex-col justify-center items-center p-6 selection:bg-secondary/30">
      <div className="w-full max-w-md">
        {/* Brand header */}
        <div className="text-center mb-8">
          <Link to="/" className="inline-flex items-center space-x-2.5 mb-3 group">
            <div className="w-10 h-10 rounded-xl bg-primary flex items-center justify-center text-white shadow-soft group-hover:scale-105 transition-transform">
              <Sparkles className="w-6 h-6" />
            </div>
            <span className="font-bold text-2xl text-textMain tracking-tight">MindCare AI</span>
          </Link>
          <h2 className="text-xl font-bold text-textMain">Create Your Account</h2>
          <p className="text-xs text-textMuted mt-1">Begin your supportive, confidential wellness journey</p>
        </div>

        {/* Card */}
        <div className="bg-surface rounded-2xl border border-accent-border p-8 shadow-card">
          {error && (
            <div className="mb-5 p-3 rounded-xl bg-crisis-bg border border-crisis-border flex items-center space-x-2 text-xs text-crisis-text">
              <AlertCircle className="w-4 h-4 flex-shrink-0" />
              <span>{error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-textMain mb-1.5">Your Name</label>
              <div className="relative">
                <User className="w-4 h-4 text-textMuted absolute left-3.5 top-3" />
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="Alex Morgan"
                  required
                  className="w-full pl-10 pr-4 py-2.5 bg-background border border-accent-border rounded-xl text-sm text-textMain placeholder-textMuted focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-textMain mb-1.5">Email Address</label>
              <div className="relative">
                <Mail className="w-4 h-4 text-textMuted absolute left-3.5 top-3" />
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="you@example.com"
                  required
                  className="w-full pl-10 pr-4 py-2.5 bg-background border border-accent-border rounded-xl text-sm text-textMain placeholder-textMuted focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-textMain mb-1.5">Password</label>
              <div className="relative">
                <Lock className="w-4 h-4 text-textMuted absolute left-3.5 top-3" />
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="At least 6 characters"
                  required
                  className="w-full pl-10 pr-4 py-2.5 bg-background border border-accent-border rounded-xl text-sm text-textMain placeholder-textMuted focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-textMain mb-1.5">Confirm Password</label>
              <div className="relative">
                <Lock className="w-4 h-4 text-textMuted absolute left-3.5 top-3" />
                <input
                  type="password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  placeholder="Repeat your password"
                  required
                  className="w-full pl-10 pr-4 py-2.5 bg-background border border-accent-border rounded-xl text-sm text-textMain placeholder-textMuted focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={isSubmitting}
              className="w-full py-3 bg-primary hover:bg-primary-hover text-white rounded-xl text-sm font-semibold shadow-soft transition-all flex items-center justify-center space-x-2 disabled:opacity-50 mt-2"
            >
              <span>{isSubmitting ? 'Creating account...' : 'Get Started'}</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </form>
        </div>

        {/* Footer link */}
        <p className="text-center text-xs text-textMuted mt-6">
          Already have an account?{' '}
          <Link to="/login" className="text-primary font-semibold hover:underline">
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
};

