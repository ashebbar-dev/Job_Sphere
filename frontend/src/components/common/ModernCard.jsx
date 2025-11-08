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
