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
