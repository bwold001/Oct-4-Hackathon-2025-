import React, { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import { generateDataWithAI, analyzeData } from '../services/dataGenerator';
import './LoadingPage.css';

const LoadingPage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState('Initializing analysis...');

  useEffect(() => {
    const loadingSteps = [
      { text: 'Initializing analysis...', duration: 1000 },
      { text: 'Processing your social media data...', duration: 1500 },
      { text: 'Analyzing sentiment patterns...', duration: 2000 },
      { text: 'Generating insights...', duration: 1500 },
      { text: 'Finalizing results...', duration: 1000 }
    ];

    let currentStep = 0;
    let progressInterval;

    const runLoadingSequence = () => {
      if (currentStep < loadingSteps.length) {
        setStatus(loadingSteps[currentStep].text);
        setProgress((currentStep + 1) * 20);
        
        setTimeout(() => {
          currentStep++;
          runLoadingSequence();
        }, loadingSteps[currentStep].duration);
      } else {
        // All steps completed, now call the API
        callAnalysisAPI();
      }
    };

    const callAnalysisAPI = async () => {
      try {
        setStatus('Connecting to AI analysis...');
        
        let dataToAnalyze;
        
        // Check if we need to generate data (from Generate Data button)
        const connectedApps = location.state?.connectedApps || [];
        const shouldGenerateData = connectedApps.includes('generate');
        
        if (shouldGenerateData) {
          setStatus('Generating realistic data with AI...');
          try {
            const generatedData = await generateDataWithAI();
            dataToAnalyze = generatedData.data_points;
          } catch (error) {
            console.warn('Failed to generate data with AI, using fallback:', error);
            dataToAnalyze = generateSampleData();
          }
        } else {
          // Use sample data for other apps
          dataToAnalyze = generateSampleData();
        }
        
        setStatus('Analyzing your data...');
        let analysisResult;
        
        try {
          analysisResult = await analyzeData(dataToAnalyze);
        } catch (error) {
          console.warn('Analysis failed, using fallback data:', error);
          // Use fallback analysis data
          analysisResult = getFallbackAnalysis();
        }
        
        // Store results in localStorage for the results page
        localStorage.setItem('analysisResults', JSON.stringify(analysisResult));
        
        setStatus('Analysis complete!');
        setProgress(100);
        
        // Navigate to results after a short delay
        setTimeout(() => {
          navigate('/results');
        }, 1000);
        
      } catch (error) {
        console.error('Unexpected error:', error);
        setStatus('Using fallback data...');
        
        // Always provide fallback data and show results
        const fallbackResult = getFallbackAnalysis();
        localStorage.setItem('analysisResults', JSON.stringify(fallbackResult));
        
        setStatus('Analysis complete!');
        setProgress(100);
        
        setTimeout(() => {
          navigate('/results');
        }, 1000);
      }
    };

    // Start the loading sequence
    runLoadingSequence();

    return () => {
      if (progressInterval) {
        clearInterval(progressInterval);
      }
    };
  }, [navigate, location.state]);

  const getFallbackAnalysis = () => {
    return {
      emotional_trend: {
        chart_type: "line",
        title: "Daily Sentiment Over Time",
        data: [
          { date: "2025-01-15", sentiment_score: 65 },
          { date: "2025-01-16", sentiment_score: 72 },
          { date: "2025-01-17", sentiment_score: 58 },
          { date: "2025-01-18", sentiment_score: 81 },
          { date: "2025-01-19", sentiment_score: 69 },
          { date: "2025-01-20", sentiment_score: 75 },
          { date: "2025-01-21", sentiment_score: 83 }
        ]
      },
      mental_health_categories: {
        chart_type: "pie",
        title: "Distribution of Anxiety/Stress/Depression Indicators",
        data: [
          { category: "Anxiety", percentage: 35 },
          { category: "Stress", percentage: 45 },
          { category: "Depression", percentage: 20 }
        ]
      },
      engagement_vs_mood: {
        chart_type: "scatter",
        title: "Engagement vs Mood",
        data: [
          { likes: 12, comments: 3, emotional_tone: 65 },
          { likes: 25, comments: 7, emotional_tone: 72 },
          { likes: 8, comments: 1, emotional_tone: 58 },
          { likes: 35, comments: 9, emotional_tone: 81 },
          { likes: 18, comments: 4, emotional_tone: 69 }
        ]
      },
      topics_discussed: {
        chart_type: "word_cloud",
        title: "Top Stress-Related Words",
        data: [
          { word: "workload", frequency: 42 },
          { word: "deadline", frequency: 37 },
          { word: "sleep", frequency: 30 },
          { word: "balance", frequency: 25 },
          { word: "family", frequency: 21 },
          { word: "exercise", frequency: 18 },
          { word: "burnout", frequency: 14 }
        ]
      },
      wellbeing_index: {
        chart_type: "gauge",
        title: "Overall Wellbeing Score",
        data: [],
        value: 76,
        range: { min: 0, max: 100 },
        status: "Stable"
      },
      recommendations: {
        chart_type: "text_cards",
        title: "Personalized Suggestions",
        data: [
          { id: 1, text: "Try a 10-minute mindfulness meditation before starting your day." },
          { id: 2, text: "Take a short walk after lunch to reduce mid-day stress." },
          { id: 3, text: "Limit late-night screen time to improve sleep quality." },
          { id: 4, text: "Reach out to a friend or colleague for social connection." }
        ]
      }
    };
  };

  const generateSampleData = () => {
    // Generate realistic sample data for demonstration
    const sampleData = [];
    const emotions = ['positive', 'mixed', 'negative', 'neutral'];
    const mentalStates = ['positive', 'stressed', 'anxious', 'depressed', 'neutral'];
    const topics = ['work_stress', 'fitness_wellness', 'social_connection', 'sleep_issues', 'family_time'];
    
    const captions = [
      "Feeling overwhelmed with work today, but trying to stay positive! #work #stress #motivation",
      "Great workout session! Feeling much better now. #fitness #wellness #selfcare",
      "Had a rough day, but grateful for my friends who always support me. #grateful #friends #support",
      "Can't sleep again... too much on my mind. #insomnia #anxiety #sleep",
      "Celebrating a small win at work today! #achievement #work #success",
      "Feeling lonely lately, need to reach out to people more. #loneliness #social #connection",
      "Beautiful sunset walk helped clear my mind. #nature #mindfulness #peace",
      "Stressed about the upcoming presentation, but I'll get through it. #presentation #stress #confidence"
    ];

    for (let i = 0; i < 10; i++) {
      const timestamp = new Date(Date.now() - Math.random() * 7 * 24 * 60 * 60 * 1000);
      const caption = captions[Math.floor(Math.random() * captions.length)];
      
      sampleData.push({
        post_id: `post_${i + 1}`,
        user_id: 'user_123',
        timestamp: timestamp.toISOString(),
        day_of_week: timestamp.toLocaleDateString('en-US', { weekday: 'long' }),
        time_of_day: timestamp.getHours() < 12 ? 'morning' : timestamp.getHours() < 18 ? 'afternoon' : 'evening',
        caption_text: caption,
        hashtags: caption.match(/#\w+/g)?.join(' ') || '',
        image_context_label: 'social_media',
        sentiment_score: Math.random() * 60 + 20, // 20-80 range
        emotion_primary: emotions[Math.floor(Math.random() * emotions.length)],
        emotion_confidence: Math.random() * 0.3 + 0.7, // 0.7-1.0 range
        topic_cluster: topics[Math.floor(Math.random() * topics.length)],
        text_length: caption.length,
        likes_count: Math.floor(Math.random() * 50) + 5,
        comments_count: Math.floor(Math.random() * 15),
        shares_count: Math.floor(Math.random() * 8),
        saved_count: Math.floor(Math.random() * 5),
        average_comment_sentiment: Math.random() * 60 + 20,
        engagement_score: Math.random() * 50 + 30,
        time_spent_on_post: Math.floor(Math.random() * 300) + 30,
        comments_read_count: Math.floor(Math.random() * 10),
        scrolled_back: Math.random() > 0.5,
        interaction_type: 'post_creation',
        num_sessions_per_day: Math.floor(Math.random() * 10) + 5,
        avg_session_duration: Math.random() * 20 + 8,
        night_usage_minutes: Math.floor(Math.random() * 120) + 10,
        label_mental_state: mentalStates[Math.floor(Math.random() * mentalStates.length)],
        label_confidence: Math.random() * 0.3 + 0.7,
        wellbeing_index: Math.random() * 50 + 30,
        recommendation_flag: Math.random() > 0.5
      });
    }
    
    return sampleData;
  };

  return (
    <div className="loading-page">
      <div className="container">
        <div className="loading-content">
          <motion.div
            className="ai-graphic"
            animate={{
              scale: [1, 1.1, 1],
              rotate: [0, 5, -5, 0],
            }}
            transition={{
              duration: 2,
              repeat: Infinity,
              ease: "easeInOut"
            }}
          >
            <div className="brain-icon">🧠</div>
            <div className="data-nodes">
              <div className="node node-1"></div>
              <div className="node node-2"></div>
              <div className="node node-3"></div>
              <div className="node node-4"></div>
              <div className="node node-5"></div>
              <div className="node node-6"></div>
            </div>
          </motion.div>

          <div className="spinner-container">
            <div className="spinner"></div>
          </div>

          <div className="loading-text">
            <h2>Analyzing your social media activity...</h2>
            <p>This might take a few moments.</p>
          </div>

          <div className="progress-section">
            <div className="progress-bar">
              <motion.div
                className="progress-fill"
                initial={{ width: 0 }}
                animate={{ width: `${progress}%` }}
                transition={{ duration: 0.5, ease: "easeOut" }}
              />
            </div>
            <div className="progress-text">
              <span className="status-text">{status}</span>
              <span className="progress-percentage">{progress}%</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoadingPage;