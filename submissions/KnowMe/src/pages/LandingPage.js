import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import AppIcon from '../components/AppIcon';
import AuthorizationModal from '../components/AuthorizationModal';
import './LandingPage.css';

const LandingPage = () => {
  const navigate = useNavigate();
  const [connectedApps, setConnectedApps] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [selectedApp, setSelectedApp] = useState('');

  const apps = [
    'instagram',
    'twitter', 
    'facebook',
    'snapchat',
    'linkedin',
    'download',
    'generate'
  ];

  const handleAppClick = (app) => {
    if (connectedApps.includes(app)) return;
    
    setSelectedApp(app);
    setShowModal(true);
  };

  const handleAuthorize = () => {
    setConnectedApps([...connectedApps, selectedApp]);
    setShowModal(false);
    setSelectedApp('');
  };

  const handleCancel = () => {
    setShowModal(false);
    setSelectedApp('');
  };

  const handleAnalyze = () => {
    navigate('/loading', { 
      state: { connectedApps: connectedApps } 
    });
  };

  const getAppName = (app) => {
    switch (app) {
      case 'instagram': return 'Instagram';
      case 'twitter': return 'Twitter (X)';
      case 'facebook': return 'Facebook';
      case 'snapchat': return 'Snapchat';
      case 'linkedin': return 'LinkedIn';
      case 'download': return 'Download Data';
      case 'generate': return 'Generate Data';
      default: return 'Unknown';
    }
  };

  return (
    <div className="landing-page">
      <div className="container">
        <div className="hero-section">
          <h1 className="title">Know Me</h1>
          <p className="tagline">
            Peek into your mind—through the story your phone tells.
          </p>
        </div>

        <div className="apps-section">
          <h2 className="section-title">Connect Your Social Media</h2>
          <p className="section-subtitle">
            Choose up to 5 applications to analyze your mental health patterns
          </p>
          
          <div className="apps-grid">
            {apps.map((app) => (
              <AppIcon
                key={app}
                app={app}
                isConnected={connectedApps.includes(app)}
                onClick={() => handleAppClick(app)}
                disabled={!connectedApps.includes(app) && connectedApps.length >= 5}
              />
            ))}
          </div>
        </div>

        <div className="analyze-section">
          <button
            className={`btn btn-primary analyze-btn ${connectedApps.length === 0 ? 'disabled' : ''}`}
            onClick={handleAnalyze}
            disabled={connectedApps.length === 0}
          >
            Analyze My Data
          </button>
          <p className="analyze-note">
            {connectedApps.length === 0 
              ? 'Connect at least one app to begin analysis'
              : `${connectedApps.length} app${connectedApps.length > 1 ? 's' : ''} connected`
            }
          </p>
        </div>
      </div>

      <AuthorizationModal
        isOpen={showModal}
        onClose={handleCancel}
        onAuthorize={handleAuthorize}
        appName={getAppName(selectedApp)}
      />
    </div>
  );
};

export default LandingPage;