import React from 'react';
import './LoadingDots.css';

export default function LoadingDots() {
  return (
    <div className="flex space-x-1 ml-12 mt-6 animate-loading-dots">
      <div className="dot-pulse" />
    </div>
  );
}
