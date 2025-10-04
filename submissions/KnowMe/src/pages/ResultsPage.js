import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import Chart from '../components/Chart';
import { ArrowLeft, RefreshCw, Download, Share2 } from 'lucide-react';
import './ResultsPage.css';

const ResultsPage = () => {
  const navigate = useNavigate();
  const [analysisData, setAnalysisData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Load analysis results from localStorage
    const results = localStorage.getItem('analysisResults');
    if (results) {
      try {
        const parsedResults = JSON.parse(results);
        setAnalysisData(parsedResults);
      } catch (error) {
        console.error('Error parsing analysis results:', error);
        // If parsing fails, redirect back to landing page
        navigate('/');
      }
    } else {
      // If no results found, redirect back to landing page
      navigate('/');
    }
    setLoading(false);
  }, [navigate]);

  const handleNewAnalysis = () => {
    localStorage.removeItem('analysisResults');
    navigate('/');
  };

  const handleDownload = () => {
    if (analysisData) {
      const dataStr = JSON.stringify(analysisData, null, 2);
      const dataBlob = new Blob([dataStr], { type: 'application/json' });
      const url = URL.createObjectURL(dataBlob);
      const link = document.createElement('a');
      link.href = url;
      link.download = 'mental-health-analysis.json';
      link.click();
      URL.revokeObjectURL(url);
    }
  };

  const handleShare = () => {
    if (navigator.share) {
      navigator.share({
        title: 'My Mental Health Analysis',
        text: 'Check out my mental health analysis from Know Me!',
        url: window.location.href
      });
    } else {
      // Fallback: copy to clipboard
      navigator.clipboard.writeText(window.location.href);
      alert('Link copied to clipboard!');
    }
  };

  if (loading) {
    return (
      <div className="results-page">
        <div className="container">
          <div className="loading-state">
            <div className="spinner"></div>
            <p>Loading your analysis results...</p>
          </div>
        </div>
      </div>
    );
  }

  if (!analysisData) {
    return (
      <div className="results-page">
        <div className="container">
          <div className="error-state">
            <h2>No analysis data found</h2>
            <p>Please run a new analysis to see your results.</p>
            <button className="btn btn-primary" onClick={handleNewAnalysis}>
              Start New Analysis
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="results-page">
      <div className="container">
        {/* Header */}
        <motion.div 
          className="results-header"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <div className="header-actions">
            <button 
              className="btn btn-secondary back-btn"
              onClick={() => navigate('/')}
            >
              <ArrowLeft size={20} />
              Back
            </button>
            <div className="action-buttons">
              <button 
                className="btn btn-secondary"
                onClick={handleDownload}
                title="Download Results"
              >
                <Download size={20} />
              </button>
              <button 
                className="btn btn-secondary"
                onClick={handleShare}
                title="Share Results"
              >
                <Share2 size={20} />
              </button>
            </div>
          </div>
          
          <div className="header-content">
            <h1>Your Mental Health Analysis</h1>
            <p>Here's what your social media activity reveals about your current wellbeing.</p>
          </div>
        </motion.div>

        {/* Charts Grid */}
        <div className="charts-grid">
          {/* Emotional Trend Chart */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
          >
            <Chart
              type="line"
              data={analysisData.emotional_trend.data}
              title={analysisData.emotional_trend.title}
            />
          </motion.div>

          {/* Mental Health Categories Chart */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <Chart
              type="pie"
              data={analysisData.mental_health_categories.data}
              title={analysisData.mental_health_categories.title}
            />
          </motion.div>

          {/* Engagement vs Mood Chart */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
          >
            <Chart
              type="scatter"
              data={analysisData.engagement_vs_mood.data}
              title={analysisData.engagement_vs_mood.title}
            />
          </motion.div>

          {/* Topics Discussed Chart */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
          >
            <Chart
              type="bar"
              data={analysisData.topics_discussed.data}
              title={analysisData.topics_discussed.title}
            />
          </motion.div>

          {/* Wellbeing Index Chart */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.5 }}
          >
            <Chart
              type="gauge"
              data={[]}
              title={analysisData.wellbeing_index.title}
              config={{
                value: analysisData.wellbeing_index.value,
                status: analysisData.wellbeing_index.status
              }}
            />
          </motion.div>

          {/* Recommendations Chart */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.6 }}
          >
            <Chart
              type="text_cards"
              data={analysisData.recommendations.data}
              title={analysisData.recommendations.title}
            />
          </motion.div>
        </div>

        {/* Action Buttons */}
        <motion.div 
          className="results-actions"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.7 }}
        >
          <button 
            className="btn btn-primary"
            onClick={handleNewAnalysis}
          >
            <RefreshCw size={20} />
            Run New Analysis
          </button>
        </motion.div>
      </div>
    </div>
  );
};

export default ResultsPage;
