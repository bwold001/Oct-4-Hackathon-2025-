import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

export const generateDataWithAI = async () => {
  try {
    // Call the backend to generate data using OpenAI
    const response = await axios.post(`${API_BASE_URL}/generate-data`, {
      num_posts: 10,
      analysis_period_days: 7
    });
    
    return response.data;
  } catch (error) {
    console.error('Error generating data:', error);
    throw error;
  }
};

export const analyzeData = async (dataPoints) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/analyze`, {
      data_points: dataPoints,
      analysis_period_days: 7
    });
    
    return response.data;
  } catch (error) {
    console.error('Error analyzing data:', error);
    throw error;
  }
};
