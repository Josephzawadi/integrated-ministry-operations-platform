import React from 'react';
import { Loader } from 'lucide-react';

const LoadingSpinner = ({ size = 'md' }) => {
  const sizes = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12',
  };

  return (
    <div className="flex justify-center items-center">
      <Loader className={`${sizes[size]} animate-spin text-primary-600`} />
    </div>
  );
};

export default LoadingSpinner;
