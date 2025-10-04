import React from 'react';
import { X } from 'lucide-react';
import './AuthorizationModal.css';

const AuthorizationModal = ({ 
  isOpen, 
  onClose, 
  onAuthorize, 
  appName 
}) => {
  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <button className="close-button" onClick={onClose}>
          <X size={20} />
        </button>
        
        <div className="modal-header">
          <h2>Authorize Know Me</h2>
          <p>Authorize Know Me to access your {appName} data?</p>
        </div>
        
        <div className="modal-body">
          <div className="permissions-list">
            <div className="permission-item">
              <span className="permission-icon">📱</span>
              <span>Access your posts and activity</span>
            </div>
            <div className="permission-item">
              <span className="permission-icon">📊</span>
              <span>Analyze engagement patterns</span>
            </div>
            <div className="permission-item">
              <span className="permission-icon">🔒</span>
              <span>Keep your data private and secure</span>
            </div>
          </div>
        </div>
        
        <div className="modal-footer">
          <button className="btn btn-secondary" onClick={onClose}>
            Cancel
          </button>
          <button className="btn btn-primary" onClick={onAuthorize}>
            Authorize
          </button>
        </div>
      </div>
    </div>
  );
};

export default AuthorizationModal;
