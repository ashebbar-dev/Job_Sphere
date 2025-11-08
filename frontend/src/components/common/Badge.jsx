import React from 'react';

const Badge = ({ children, variant = 'primary', size = 'md', pulse = false }) => {
  const variants = {
    primary: 'bg-blue-100 text-blue-800 border-blue-200',
    success: 'bg-green-100 text-green-800 border-green-200',
    warning: 'bg-yellow-100 text-yellow-800 border-yellow-200',
    danger: 'bg-red-100 text-red-800 border-red-200',
    purple: 'bg-purple-100 text-purple-800 border-purple-200',
    info: 'bg-cyan-100 text-cyan-800 border-cyan-200',
    outline: 'bg-white text-gray-700 border-gray-300',
  };

  const sizes = {
    sm: 'px-2 py-1 text-xs',
    md: 'px-3 py-1 text-sm',
    lg: 'px-4 py-2 text-base',
  };

  const variantClasses = variants[variant] || variants.primary;
  return (
    <span className={`inline-flex items-center gap-1 font-semibold rounded-full border ${variantClasses} ${sizes[size]} ${pulse ? 'animate-pulse-slow' : ''}`}>
      {pulse && <span className="w-2 h-2 rounded-full bg-current animate-pulse" />}
      {children}
    </span>
  );
};

export default Badge;
