import React from 'react';
import clsx from 'clsx'; // Import clsx

interface MatchSectionProps {
  children: React.ReactNode;
  className?: string; // To allow additional custom classes
}

const MatchSection: React.FC<MatchSectionProps> = ({ children, className }) => {
  const baseClasses = "mb-8 p-6 bg-white rounded-lg shadow-xl";
  const combinedClasses = clsx(baseClasses, className); // New way with clsx

  return <div className={combinedClasses}>{children}</div>;
};

export default MatchSection; 