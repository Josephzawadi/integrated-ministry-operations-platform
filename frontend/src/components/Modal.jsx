import React from 'react';

const Modal = ({ isOpen, title, children, onClose, footerContent }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full mx-4">
        <div className="flex justify-between items-center border-b p-6">
          <h2 className="text-xl font-semibold">{title}</h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 text-2xl"
          >
            ✕
          </button>
        </div>
        <div className="p-6">
          {children}
        </div>
        {footerContent && (
          <div className="border-t p-6 flex justify-end space-x-3">
            {footerContent}
          </div>
        )}
      </div>
    </div>
  );
};

export default Modal;
