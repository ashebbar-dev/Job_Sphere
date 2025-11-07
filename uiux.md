# 🎨 STUNNING UI/UX DESIGN SYSTEM

I'll give you a **complete modern design system** that will make judges say "WOW!" 

This will cover:
- 🎨 Modern color palette & design tokens
- ✨ Animated components
- 📊 Beautiful data visualizations
- 🎭 Smooth transitions
- 💎 Glass-morphism effects
- 🌈 Gradient accents

---

## **STEP A: Install Additional UI Dependencies**

```bash
cd frontend
npm install framer-motion recharts react-circular-progressbar lucide-react @headlessui/react
```

---

## **STEP B: Tailwind Configuration (Modern Design System)**

Create/Update `frontend/tailwind.config.js`:

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
        },
        accent: {
          50: '#fdf4ff',
          100: '#fae8ff',
          200: '#f5d0fe',
          300: '#f0abfc',
          400: '#e879f9',
          500: '#d946ef',
          600: '#c026d3',
          700: '#a21caf',
          800: '#86198f',
          900: '#701a75',
        },
        success: {
          50: '#f0fdf4',
          100: '#dcfce7',
          200: '#bbf7d0',
          300: '#86efac',
          400: '#4ade80',
          500: '#22c55e',
          600: '#16a34a',
          700: '#15803d',
          800: '#166534',
          900: '#14532d',
        },
        warning: {
          500: '#f59e0b',
          600: '#d97706',
        },
        danger: {
          500: '#ef4444',
          600: '#dc2626',
        }
      },
      boxShadow: {
        'soft': '0 2px 15px -3px rgba(0, 0, 0, 0.07), 0 10px 20px -2px rgba(0, 0, 0, 0.04)',
        'glow': '0 0 20px rgba(59, 130, 246, 0.5)',
        'glow-sm': '0 0 10px rgba(59, 130, 246, 0.3)',
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.5s ease-out',
        'slide-down': 'slideDown 0.5s ease-out',
        'scale-in': 'scaleIn 0.3s ease-out',
        'bounce-gentle': 'bounceGentle 2s infinite',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        slideDown: {
          '0%': { transform: 'translateY(-20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        scaleIn: {
          '0%': { transform: 'scale(0.9)', opacity: '0' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
        bounceGentle: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' },
        },
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-primary': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'gradient-success': 'linear-gradient(135deg, #667eea 0%, #22c55e 100%)',
        'gradient-mesh': 'linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%)',
      }
    },
  },
  plugins: [],
}
```

---

## **STEP C: Global CSS with Animations**

Create `frontend/src/index.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Custom Scrollbar */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f5f9;
}

::-webkit-scrollbar-thumb {
  background: #94a3b8;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #64748b;
}

/* Glass morphism utility */
.glass {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.glass-dark {
  background: rgba(30, 41, 59, 0.8);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

/* Gradient text */
.gradient-text {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Smooth transitions */
* {
  transition: all 0.2s ease-in-out;
}

button, a {
  transition: all 0.3s ease;
}

/* Custom animations */
@keyframes shimmer {
  0% {
    background-position: -1000px 0;
  }
  100% {
    background-position: 1000px 0;
  }
}

.shimmer {
  animation: shimmer 2s infinite;
  background: linear-gradient(
    to right,
    #f0f0f0 0%,
    #e0e0e0 20%,
    #f0f0f0 40%,
    #f0f0f0 100%
  );
  background-size: 1000px 100%;
}

/* Hover effects */
.hover-lift {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.hover-lift:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.15);
}

/* Card glow effect */
.card-glow {
  position: relative;
  overflow: hidden;
}

.card-glow::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(59, 130, 246, 0.1) 0%, transparent 70%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.card-glow:hover::before {
  opacity: 1;
}

/* Loading spinner */
.spinner {
  border: 3px solid rgba(59, 130, 246, 0.1);
  border-top: 3px solid #3b82f6;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Pulse animation for important elements */
@keyframes pulse-border {
  0%, 100% {
    border-color: rgba(59, 130, 246, 0.3);
  }
  50% {
    border-color: rgba(59, 130, 246, 0.8);
  }
}

.pulse-border {
  animation: pulse-border 2s ease-in-out infinite;
}
```

---

## **STEP D: Enhanced Common Components**

### **1. Modern Card Component**

Create `frontend/src/components/common/ModernCard.jsx`:

```jsx
import React from 'react';
import { motion } from 'framer-motion';

const ModernCard = ({ 
  children, 
  className = '', 
  hover = true,
  gradient = false,
  glass = false,
  onClick
}) => {
  const baseClasses = "rounded-2xl shadow-soft p-6 transition-all duration-300";
  const hoverClasses = hover ? "hover-lift cursor-pointer" : "";
  const gradientClasses = gradient ? "bg-gradient-to-br from-blue-50 to-purple-50" : "bg-white";
  const glassClasses = glass ? "glass" : "";

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      onClick={onClick}
      className={`${baseClasses} ${hoverClasses} ${gradient ? gradientClasses : glassClasses || 'bg-white'} ${className}`}
    >
      {children}
    </motion.div>
  );
};

export default ModernCard;
```

### **2. Animated Button Component**

Create `frontend/src/components/common/ModernButton.jsx`:

```jsx
import React from 'react';
import { motion } from 'framer-motion';
import { Loader2 } from 'lucide-react';

const ModernButton = ({ 
  children, 
  onClick, 
  type = 'button', 
  variant = 'primary',
  size = 'md',
  disabled = false,
  loading = false,
  icon: Icon,
  className = ''
}) => {
  const baseClasses = 'font-semibold rounded-xl transition-all duration-300 flex items-center justify-center gap-2 shadow-sm hover:shadow-md';
  
  const variants = {
    primary: 'bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white',
    secondary: 'bg-gradient-to-r from-purple-600 to-purple-700 hover:from-purple-700 hover:to-purple-800 text-white',
    success: 'bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 text-white',
    danger: 'bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white',
    outline: 'border-2 border-blue-600 text-blue-600 hover:bg-blue-50',
    ghost: 'text-gray-700 hover:bg-gray-100',
  };

  const sizes = {
    sm: 'px-4 py-2 text-sm',
    md: 'px-6 py-3 text-base',
    lg: 'px-8 py-4 text-lg',
  };

  return (
    <motion.button
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      type={type}
      onClick={onClick}
      disabled={disabled || loading}
      className={`${baseClasses} ${variants[variant]} ${sizes[size]} ${disabled || loading ? 'opacity-50 cursor-not-allowed' : ''} ${className}`}
    >
      {loading ? (
        <>
          <Loader2 className="animate-spin" size={18} />
          Loading...
        </>
      ) : (
        <>
          {Icon && <Icon size={18} />}
          {children}
        </>
      )}
    </motion.button>
  );
};

export default ModernButton;
```

### **3. Progress Bar Component**

Create `frontend/src/components/common/ProgressBar.jsx`:

```jsx
import React from 'react';
import { motion } from 'framer-motion';

const ProgressBar = ({ value, max = 100, label, color = 'blue', showValue = true }) => {
  const percentage = (value / max) * 100;
  
  const colorClasses = {
    blue: 'bg-blue-600',
    green: 'bg-green-600',
    yellow: 'bg-yellow-600',
    red: 'bg-red-600',
    purple: 'bg-purple-600',
  };

  return (
    <div className="w-full">
      {label && (
        <div className="flex justify-between mb-2">
          <span className="text-sm font-medium text-gray-700">{label}</span>
          {showValue && (
            <span className="text-sm font-bold text-gray-900">{value}/{max}</span>
          )}
        </div>
      )}
      <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${percentage}%` }}
          transition={{ duration: 1, ease: "easeOut" }}
          className={`h-full ${colorClasses[color]} rounded-full relative overflow-hidden`}
        >
          <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white to-transparent opacity-30 animate-shimmer" />
        </motion.div>
      </div>
    </div>
  );
};

export default ProgressBar;
```

### **4. Circular Score Display**

Create `frontend/src/components/common/CircularScore.jsx`:

```jsx
import React from 'react';
import { CircularProgressbar, buildStyles } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';
import { motion } from 'framer-motion';

const CircularScore = ({ score, label, size = 120 }) => {
  const getColor = (score) => {
    if (score >= 80) return '#22c55e';
    if (score >= 60) return '#3b82f6';
    if (score >= 40) return '#f59e0b';
    return '#ef4444';
  };

  return (
    <motion.div
      initial={{ scale: 0, rotate: -180 }}
      animate={{ scale: 1, rotate: 0 }}
      transition={{ duration: 0.8, type: "spring" }}
      className="flex flex-col items-center"
    >
      <div style={{ width: size, height: size }}>
        <CircularProgressbar
          value={score}
          text={`${score}%`}
          styles={buildStyles({
            pathColor: getColor(score),
            textColor: getColor(score),
            trailColor: '#e5e7eb',
            pathTransitionDuration: 1.5,
            textSize: '24px',
          })}
        />
      </div>
      {label && (
        <p className="mt-3 text-sm font-semibold text-gray-700">{label}</p>
      )}
    </motion.div>
  );
};

export default CircularScore;
```

### **5. Stat Card Component**

Create `frontend/src/components/common/StatCard.jsx`:

```jsx
import React from 'react';
import { motion } from 'framer-motion';

const StatCard = ({ icon: Icon, label, value, trend, color = 'blue' }) => {
  const colorClasses = {
    blue: 'from-blue-500 to-blue-600',
    green: 'from-green-500 to-green-600',
    purple: 'from-purple-500 to-purple-600',
    orange: 'from-orange-500 to-orange-600',
  };

  return (
    <motion.div
      whileHover={{ y: -5 }}
      className="bg-white rounded-2xl shadow-soft p-6 hover:shadow-lg transition-all"
    >
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-gray-600 mb-1">{label}</p>
          <h3 className="text-3xl font-bold text-gray-900">{value}</h3>
          {trend && (
            <p className={`text-sm mt-2 ${trend > 0 ? 'text-green-600' : 'text-red-600'}`}>
              {trend > 0 ? '↑' : '↓'} {Math.abs(trend)}% from last month
            </p>
          )}
        </div>
        <div className={`p-4 rounded-xl bg-gradient-to-br ${colorClasses[color]} shadow-lg`}>
          <Icon className="text-white" size={28} />
        </div>
      </div>
    </motion.div>
  );
};

export default StatCard;
```

### **6. Badge Component**

Create `frontend/src/components/common/Badge.jsx`:

```jsx
import React from 'react';

const Badge = ({ children, variant = 'primary', size = 'md', pulse = false }) => {
  const variants = {
    primary: 'bg-blue-100 text-blue-800 border-blue-200',
    success: 'bg-green-100 text-green-800 border-green-200',
    warning: 'bg-yellow-100 text-yellow-800 border-yellow-200',
    danger: 'bg-red-100 text-red-800 border-red-200',
    purple: 'bg-purple-100 text-purple-800 border-purple-200',
  };

  const sizes = {
    sm: 'px-2 py-1 text-xs',
    md: 'px-3 py-1 text-sm',
    lg: 'px-4 py-2 text-base',
  };

  return (
    <span className={`inline-flex items-center gap-1 font-semibold rounded-full border ${variants[variant]} ${sizes[size]} ${pulse ? 'animate-pulse-slow' : ''}`}>
      {pulse && <span className="w-2 h-2 rounded-full bg-current animate-pulse" />}
      {children}
    </span>
  );
};

export default Badge;
```

---

## **STEP E: Modern Navbar with Gradient**

Create `frontend/src/components/common/ModernNavbar.jsx`:

```jsx
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { LogOut, User, Sparkles } from 'lucide-react';
import { motion } from 'framer-motion';

const ModernNavbar = ({ user }) => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    navigate('/login');
  };

  return (
    <nav className="bg-gradient-to-r from-blue-600 via-purple-600 to-blue-700 text-white shadow-xl">
      <div className="container mx-auto px-6 py-4">
        <div className="flex justify-between items-center">
          {/* Logo */}
          <motion.div 
            initial={{ x: -20, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            className="flex items-center gap-3"
          >
            <div className="bg-white/20 backdrop-blur-sm p-2 rounded-xl">
              <Sparkles size={28} />
            </div>
            <div>
              <h1 className="text-2xl font-bold">AI Placement Portal</h1>
              <p className="text-xs text-blue-100">Powered by Intelligent Matching</p>
            </div>
          </motion.div>
          
          {/* User Info */}
          <motion.div 
            initial={{ x: 20, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            className="flex items-center gap-4"
          >
            <div className="glass text-white px-4 py-2 rounded-xl flex items-center gap-3">
              <div className="bg-white/20 p-2 rounded-lg">
                <User size={20} />
              </div>
              <div className="text-left">
                <p className="font-semibold">{user?.name || user?.email}</p>
                <p className="text-xs opacity-90">{user?.role?.toUpperCase()}</p>
              </div>
            </div>
            
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={handleLogout}
              className="flex items-center gap-2 px-5 py-2.5 bg-red-500 hover:bg-red-600 rounded-xl font-semibold shadow-lg"
            >
              <LogOut size={18} />
              Logout
            </motion.button>
          </motion.div>
        </div>
      </div>
    </nav>
  );
};

export default ModernNavbar;
```

---

## **STEP F: Stunning Login Page**

Create `frontend/src/components/ModernLogin.jsx`:

```jsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authAPI } from '../services/api';
import ModernButton from './common/ModernButton';
import { Mail, Lock, Sparkles, TrendingUp } from 'lucide-react';
import { motion } from 'framer-motion';

const ModernLogin = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await authAPI.login(formData);
      localStorage.setItem('token', response.data.access_token);
      localStorage.setItem('user', JSON.stringify(response.data));

      const role = response.data.role;
      if (role === 'student') navigate('/student/dashboard');
      else if (role === 'hod') navigate('/hod/dashboard');
      else if (role === 'tpo') navigate('/tpo/dashboard');
    } catch (err) {
      setError(err.response?.data?.error || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 flex items-center justify-center p-4 relative overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden">
        <motion.div 
          animate={{ 
            scale: [1, 1.2, 1],
            rotate: [0, 90, 0],
          }}
          transition={{ duration: 20, repeat: Infinity }}
          className="absolute -top-1/2 -left-1/2 w-full h-full bg-gradient-to-br from-blue-400/20 to-purple-400/20 rounded-full blur-3xl"
        />
        <motion.div 
          animate={{ 
            scale: [1.2, 1, 1.2],
            rotate: [90, 0, 90],
          }}
          transition={{ duration: 20, repeat: Infinity }}
          className="absolute -bottom-1/2 -right-1/2 w-full h-full bg-gradient-to-br from-purple-400/20 to-pink-400/20 rounded-full blur-3xl"
        />
      </div>

      <div className="relative z-10 w-full max-w-6xl grid md:grid-cols-2 gap-8 items-center">
        {/* Left side - Branding */}
        <motion.div
          initial={{ x: -50, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ duration: 0.8 }}
          className="hidden md:block text-center"
        >
          <div className="glass-dark p-12 rounded-3xl">
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
              className="inline-block mb-6"
            >
              <div className="bg-gradient-to-br from-blue-400 to-purple-600 p-6 rounded-3xl shadow-glow">
                <Sparkles size={64} className="text-white" />
              </div>
            </motion.div>
            
            <h1 className="text-5xl font-bold text-white mb-4">
              AI-Powered Placement Portal
            </h1>
            <p className="text-xl text-gray-200 mb-8">
              Where Intelligence Meets Opportunity
            </p>
            
            <div className="space-y-4 text-left">
              {[
                { icon: TrendingUp, text: 'Smart Resume Matching' },
                { icon: Sparkles, text: 'AI Company Research' },
                { icon: Mail, text: 'Automated Communications' },
              ].map((feature, idx) => (
                <motion.div
                  key={idx}
                  initial={{ x: -20, opacity: 0 }}
                  animate={{ x: 0, opacity: 1 }}
                  transition={{ delay: 0.3 + idx * 0.1 }}
                  className="flex items-center gap-3 bg-white/10 backdrop-blur-sm p-4 rounded-xl"
                >
                  <feature.icon className="text-blue-300" size={24} />
                  <span className="text-white font-medium">{feature.text}</span>
                </motion.div>
              ))}
            </div>
          </div>
        </motion.div>

        {/* Right side - Login form */}
        <motion.div
          initial={{ x: 50, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ duration: 0.8 }}
        >
          <div className="glass p-10 rounded-3xl shadow-2xl">
            <div className="text-center mb-8">
              <h2 className="text-4xl font-bold gradient-text mb-2">Welcome Back</h2>
              <p className="text-gray-600">Sign in to continue your journey</p>
            </div>

            {error && (
              <motion.div
                initial={{ scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                className="bg-red-50 border-l-4 border-red-500 text-red-700 p-4 rounded-lg mb-6"
              >
                <p className="font-medium">{error}</p>
              </motion.div>
            )}

            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Email Input */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Email Address
                </label>
                <div className="relative">
                  <Mail className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                  <input
                    type="email"
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    className="w-full pl-12 pr-4 py-4 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                    placeholder="you@example.com"
                    required
                  />
                </div>
              </div>

              {/* Password Input */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Password
                </label>
                <div className="relative">
                  <Lock className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                  <input
                    type="password"
                    value={formData.password}
                    onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                    className="w-full pl-12 pr-4 py-4 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                    placeholder="••••••••"
                    required
                  />
                </div>
              </div>

              <ModernButton
                type="submit"
                variant="primary"
                size="lg"
                loading={loading}
                className="w-full"
              >
                {loading ? 'Signing In...' : 'Sign In'}
              </ModernButton>
            </form>

            <div className="mt-8 text-center">
              <p className="text-gray-600">
                Don't have an account?{' '}
                <button
                  onClick={() => navigate('/register')}
                  className="font-semibold text-blue-600 hover:text-blue-700 transition-colors"
                >
                  Create Account
                </button>
              </p>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default ModernLogin;
```

---

## **STEP G: The STAR Feature - AI Job Analysis Component**

This is the **most impressive component** that will wow the judges!

Create `frontend/src/components/student/JobAnalysisModal.jsx`:

```jsx
import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Sparkles, TrendingUp, Award, Target, BookOpen, FileText, Download } from 'lucide-react';
import { aiAPI } from '../../services/api';
import CircularScore from '../common/CircularScore';
import ModernButton from '../common/ModernButton';
import Badge from '../common/Badge';
import ProgressBar from '../common/ProgressBar';

const JobAnalysisModal = ({ drive, onClose, onApply }) => {
  const [loading, setLoading] = useState(true);
  const [analysis, setAnalysis] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    loadAnalysis();
  }, []);

  const loadAnalysis = async () => {
    try {
      const response = await aiAPI.analyzeJobFit(drive.id);
      setAnalysis(response.data);
    } catch (error) {
      console.error('Analysis failed:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
        <div className="glass p-12 rounded-3xl">
          <div className="flex flex-col items-center gap-4">
            <div className="spinner" />
            <p className="text-lg font-semibold text-gray-700">Analyzing with AI...</p>
            <p className="text-sm text-gray-500">Researching company & matching skills</p>
          </div>
        </div>
      </div>
    );
  }

  const tabs = [
    { id: 'overview', label: 'Overview', icon: Sparkles },
    { id: 'match', label: 'Match Analysis', icon: Target },
    { id: 'skills', label: 'Skills Gap', icon: TrendingUp },
    { id: 'company', label: 'Company Intel', icon: Award },
  ];

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4"
        onClick={onClose}
      >
        <motion.div
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          exit={{ scale: 0.9, opacity: 0 }}
          onClick={(e) => e.stopPropagation()}
          className="bg-white rounded-3xl shadow-2xl max-w-6xl w-full max-h-[90vh] overflow-hidden"
        >
          {/* Header */}
          <div className="bg-gradient-to-r from-blue-600 to-purple-600 p-6 text-white">
            <div className="flex justify-between items-start mb-4">
              <div>
                <h2 className="text-3xl font-bold mb-2">{drive.job_title}</h2>
                <p className="text-blue-100">{drive.company_name}</p>
              </div>
              <button
                onClick={onClose}
                className="p-2 hover:bg-white/20 rounded-xl transition-colors"
              >
                <X size={24} />
              </button>
            </div>

            {/* Score Overview */}
            <div className="grid grid-cols-3 gap-4">
              <div className="glass-dark p-4 rounded-xl text-center">
                <p className="text-sm opacity-90 mb-2">Match Score</p>
                <p className="text-4xl font-bold">{analysis?.match_analysis?.overall_match_score || 0}%</p>
              </div>
              <div className="glass-dark p-4 rounded-xl text-center">
                <p className="text-sm opacity-90 mb-2">ATS Score</p>
                <p className="text-4xl font-bold">{analysis?.ats_analysis?.ats_score || 0}%</p>
              </div>
              <div className="glass-dark p-4 rounded-xl text-center">
                <p className="text-sm opacity-90 mb-2">Readiness</p>
                <p className="text-xl font-bold">{analysis?.skills_gap?.overall_readiness || 'Good'}</p>
              </div>
            </div>
          </div>

          {/* Tabs */}
          <div className="border-b border-gray-200 px-6">
            <div className="flex gap-2">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center gap-2 px-6 py-4 font-semibold transition-all ${
                    activeTab === tab.id
                      ? 'text-blue-600 border-b-2 border-blue-600'
                      : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  <tab.icon size={18} />
                  {tab.label}
                </button>
              ))}
            </div>
          </div>

          {/* Content */}
          <div className="p-6 overflow-y-auto max-h-[50vh]">
            {activeTab === 'overview' && (
              <div className="space-y-6">
                {/* Scores */}
                <div className="grid grid-cols-3 gap-6">
                  <CircularScore
                    score={analysis?.match_analysis?.overall_match_score || 0}
                    label="Overall Match"
                    size={140}
                  />
                  <CircularScore
                    score={analysis?.ats_analysis?.ats_score || 0}
                    label="ATS Compatibility"
                    size={140}
                  />
                  <CircularScore
                    score={analysis?.match_analysis?.skills_match?.score || 0}
                    label="Skills Match"
                    size={140}
                  />
                </div>

                {/* Key Strengths */}
                <div>
                  <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
                    <Award className="text-green-600" />
                    Your Strengths
                  </h3>
                  <div className="grid grid-cols-2 gap-3">
                    {analysis?.match_analysis?.strengths?.map((strength, idx) => (
                      <motion.div
                        key={idx}
                        initial={{ x: -20, opacity: 0 }}
                        animate={{ x: 0, opacity: 1 }}
                        transition={{ delay: idx * 0.1 }}
                        className="flex items-start gap-2 bg-green-50 border border-green-200 p-3 rounded-xl"
                      >
                        <span className="text-green-600 text-xl">✓</span>
                        <span className="text-sm text-gray-700">{strength}</span>
                      </motion.div>
                    ))}
                  </div>
                </div>

                {/* Recommendation */}
                <div className="bg-gradient-to-r from-blue-50 to-purple-50 border-l-4 border-blue-600 p-6 rounded-xl">
                  <h4 className="font-bold text-lg mb-2">AI Recommendation</h4>
                  <p className="text-gray-700">{analysis?.match_analysis?.recommendation}</p>
                </div>
              </div>
            )}

            {activeTab === 'match' && (
              <div className="space-y-6">
                {/* Matching Skills */}
                <div>
                  <h3 className="text-xl font-bold mb-4 text-green-600">✓ Matching Skills</h3>
                  <div className="flex flex-wrap gap-2">
                    {analysis?.match_analysis?.skills_match?.matching_skills?.map((skill, idx) => (
                      <Badge key={idx} variant="success" size="lg">
                        {skill}
                      </Badge>
                    ))}
                  </div>
                </div>

                {/* Missing Skills */}
                <div>
                  <h3 className="text-xl font-bold mb-4 text-orange-600">⚠ Missing Skills</h3>
                  <div className="flex flex-wrap gap-2">
                    {analysis?.match_analysis?.skills_match?.missing_skills?.map((skill, idx) => (
                      <Badge key={idx} variant="warning" size="lg">
                        {skill}
                      </Badge>
                    ))}
                  </div>
                </div>

                {/* Score Breakdown */}
                <div className="space-y-4">
                  <ProgressBar
                    value={analysis?.match_analysis?.skills_match?.score || 0}
                    max={100}
                    label="Skills Match"
                    color="green"
                  />
                  <ProgressBar
                    value={analysis?.match_analysis?.experience_fit?.score || 0}
                    max={100}
                    label="Experience Fit"
                    color="blue"
                  />
                  <ProgressBar
                    value={analysis?.match_analysis?.cultural_fit?.score || 0}
                    max={100}
                    label="Cultural Alignment"
                    color="purple"
                  />
                </div>
              </div>
            )}

            {activeTab === 'skills' && (
              <div className="space-y-6">
                <div className="bg-gradient-to-r from-orange-50 to-red-50 border-l-4 border-orange-500 p-6 rounded-xl">
                  <h4 className="font-bold text-lg mb-2">Overall Readiness</h4>
                  <p className="text-2xl font-bold text-orange-600">
                    {analysis?.skills_gap?.overall_readiness}
                  </p>
                </div>

                {/* Critical Gaps */}
                <div>
                  <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
                    <Target className="text-red-600" />
                    Skills to Acquire
                  </h3>
                  <div className="space-y-4">
                    {analysis?.skills_gap?.critical_gaps?.map((gap, idx) => (
                      <motion.div
                        key={idx}
                        initial={{ y: 20, opacity: 0 }}
                        animate={{ y: 0, opacity: 1 }}
                        transition={{ delay: idx * 0.1 }}
                        className="bg-white border-2 border-gray-200 rounded-xl p-5 hover:shadow-lg transition-all"
                      >
                        <div className="flex items-start justify-between mb-3">
                          <h4 className="font-bold text-lg">{gap.skill}</h4>
                          <Badge variant={gap.importance === 'Critical' ? 'danger' : 'warning'}>
                            {gap.importance}
                          </Badge>
                        </div>
                        <p className="text-sm text-gray-600 mb-3">
                          <strong>Time to learn:</strong> {gap.estimated_time}
                        </p>
                        <div className="bg-blue-50 p-3 rounded-lg">
                          <p className="text-sm font-semibold mb-2">Learning Resources:</p>
                          <ul className="text-sm text-gray-700 space-y-1">
                            {gap.learning_resources?.map((resource, ridx) => (
                              <li key={ridx} className="flex items-center gap-2">
                                <BookOpen size={14} className="text-blue-600" />
                                {resource}
                              </li>
                            ))}
                          </ul>
                        </div>
                      </motion.div>
                    ))}
                  </div>
                </div>

                {/* Quick Wins */}
                <div className="bg-green-50 border-2 border-green-200 rounded-xl p-5">
                  <h4 className="font-bold mb-3 flex items-center gap-2">
                    <TrendingUp className="text-green-600" />
                    Quick Wins (Learn These Fast!)
                  </h4>
                  <ul className="space-y-2">
                    {analysis?.skills_gap?.quick_wins?.map((win, idx) => (
                      <li key={idx} className="flex items-start gap-2 text-gray-700">
                        <span className="text-green-600 font-bold">→</span>
                        {win}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            )}

            {activeTab === 'company' && (
              <div className="space-y-6">
                {/* Company Overview */}
                <div>
                  <h3 className="text-2xl font-bold mb-3">{drive.company_name}</h3>
                  <p className="text-gray-700 leading-relaxed">
                    {analysis?.company_research?.company_overview}
                  </p>
                </div>

                {/* Company Details */}
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-blue-50 p-4 rounded-xl">
                    <p className="text-sm text-gray-600 mb-1">Industry</p>
                    <p className="font-bold">{analysis?.company_research?.industry}</p>
                  </div>
                  <div className="bg-purple-50 p-4 rounded-xl">
                    <p className="text-sm text-gray-600 mb-1">Company Size</p>
                    <p className="font-bold">{analysis?.company_research?.company_size}</p>
                  </div>
                </div>

                {/* Culture & Values */}
                <div>
                  <h4 className="font-bold text-lg mb-3">Culture & Values</h4>
                  <div className="flex flex-wrap gap-2">
                    {analysis?.company_research?.culture_values?.map((value, idx) => (
                      <Badge key={idx} variant="purple" size="lg">
                        {value}
                      </Badge>
                    ))}
                  </div>
                </div>

                {/* Tech Stack */}
                <div>
                  <h4 className="font-bold text-lg mb-3">Tech Stack</h4>
                  <div className="flex flex-wrap gap-2">
                    {analysis?.company_research?.tech_stack?.map((tech, idx) => (
                      <Badge key={idx} variant="primary" size="lg">
                        {tech}
                      </Badge>
                    ))}
                  </div>
                </div>

                {/* Recent News */}
                {analysis?.company_research?.recent_news?.length > 0 && (
                  <div>
                    <h4 className="font-bold text-lg mb-3">Recent News</h4>
                    <div className="space-y-3">
                      {analysis?.company_research?.recent_news?.map((news, idx) => (
                        <div key={idx} className="bg-gray-50 p-4 rounded-xl border-l-4 border-blue-500">
                          <p className="text-gray-700">{news}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Footer Actions */}
          <div className="border-t border-gray-200 p-6 bg-gray-50">
            <div className="flex gap-4">
              <ModernButton
                onClick={onClose}
                variant="ghost"
                className="flex-1"
              >
                Close
              </ModernButton>
              <ModernButton
                onClick={() => onApply(analysis)}
                variant="primary"
                icon={FileText}
                className="flex-1"
              >
                Apply with AI-Enhanced Resume
              </ModernButton>
            </div>
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
};

export default JobAnalysisModal;
```

---

## **Summary: What Makes This UI/UX Special**

### ✨ **Visual Features That Will Impress Judges:**

1. **Gradient Backgrounds** - Modern, eye-catching
2. **Glass-morphism** - Trendy, professional look
3. **Smooth Animations** - Framer Motion everywhere
4. **Circular Score Displays** - Visual impact
5. **Progress Bars with Shimmer** - Engaging feedback
6. **Badge System** - Clean information display
7. **Hover Effects** - Interactive feel
8. **Loading States** - Professional UX
9. **Color Psychology** - Green (success), Red (gaps), Blue (trust)
10. **Responsive Design** - Works on all screens

### 🎯 **Judge Appeal:**

- **First Impression**: Animated login with floating elements
- **Wow Moment**: AI Analysis modal with circular scores
- **Professional**: Gradient navbar, modern cards
- **Attention to Detail**: Micro-interactions everywhere
- **Data Visualization**: Charts, progress bars, badges

---

**Next Steps:**
1. Implement the remaining dashboard components using these design patterns
2. Add charts (using recharts) for TPO/HOD analytics
3. Create matching designs for all pages

Would you like me to continue with:
- **Option 1**: Complete Student Dashboard with all these designs
- **Option 2**: TPO Dashboard with data visualization charts
- **Option 3**: HOD Dashboard with reports and stats

Choose, and I'll make it stunning! 🚀