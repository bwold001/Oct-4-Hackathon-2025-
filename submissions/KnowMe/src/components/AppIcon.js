import React from 'react';
import { 
  Instagram, 
  Twitter, 
  Facebook, 
  Camera, 
  Linkedin, 
  Download, 
  Database,
  Check
} from 'lucide-react';

const AppIcon = ({ 
  app, 
  isConnected, 
  onClick, 
  disabled = false 
}) => {
  const getIcon = () => {
    const iconProps = { size: 32, color: isConnected ? '#9ca3af' : '#4f46e5' };
    
    switch (app) {
      case 'instagram':
        return <Instagram {...iconProps} />;
      case 'twitter':
        return <Twitter {...iconProps} />;
      case 'facebook':
        return <Facebook {...iconProps} />;
      case 'snapchat':
        return <Camera {...iconProps} />;
      case 'linkedin':
        return <Linkedin {...iconProps} />;
      case 'download':
        return <Download {...iconProps} />;
      case 'generate':
        return <Database {...iconProps} />;
      default:
        return <Database {...iconProps} />;
    }
  };

  const getAppName = () => {
    switch (app) {
      case 'instagram':
        return 'Instagram';
      case 'twitter':
        return 'Twitter (X)';
      case 'facebook':
        return 'Facebook';
      case 'snapchat':
        return 'Snapchat';
      case 'linkedin':
        return 'LinkedIn';
      case 'download':
        return 'Download Data';
      case 'generate':
        return 'Generate Data';
      default:
        return 'Unknown';
    }
  };

  return (
    <div 
      className={`app-icon ${isConnected ? 'connected' : ''} ${disabled ? 'disabled' : ''}`}
      onClick={!disabled ? onClick : undefined}
    >
      <div className="icon-container">
        {getIcon()}
        {isConnected && (
          <div className="checkmark">
            <Check size={16} color="white" />
          </div>
        )}
      </div>
      <span className="app-name">{getAppName()}</span>
    </div>
  );
};

export default AppIcon;
