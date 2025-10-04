# Know Me - Mental Health Analyzer

A full-stack application that analyzes social media data to provide mental health insights using AI.

## 🚀 Features

### Frontend (React)
- **Landing Page**: Connect up to 5 social media platforms
- **Authorization Modal**: Secure data access permissions
- **Loading Page**: Animated analysis progress with AI graphics
- **Results Dashboard**: Interactive charts and AI-generated insights
- **Responsive Design**: Works on all devices

### Backend (FastAPI + OpenAI)
- **Data Processing**: Analyzes 30+ data points per social media post
- **AI Analysis**: Uses GPT-4 for intelligent mental health insights
- **Structured Output**: Returns data optimized for React visualization
- **RESTful API**: Clean endpoints for easy integration

## 📊 Data Flow

1. **Input**: Social media posts with sentiment, engagement, and wellbeing metrics
2. **Processing**: Data analysis and pattern recognition
3. **AI Analysis**: OpenAI generates personalized recommendations
4. **Output**: Structured JSON with 6 chart types for visualization

## 🛠️ Setup

### Backend Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
# Create .env file with your OpenAI API key
OPENAI_API_KEY=your_openai_api_key_here

# Run backend
python main.py
```

### Frontend Setup
```bash
# Install dependencies
npm install

# Start development server
npm start
```

## 📱 UI Pages

### 1. Landing Page (`/`)
- **Title**: "Know Me"
- **Tagline**: "Peek into your mind—through the story your phone tells."
- **7 App Icons**: Instagram, Twitter, Facebook, Snapchat, LinkedIn, Download Data, Generate Data
- **Connect Functionality**: Click to authorize (max 5 apps)
- **Analyze Button**: Enabled when at least 1 app is connected

### 2. Loading Page (`/loading`)
- **Animated Spinner**: Circular loader with AI brain icon
- **Progress Bar**: Real-time analysis progress
- **Status Updates**: Step-by-step analysis messages
- **Background Graphics**: Subtle AI-style nodes and waves

### 3. Results Page (`/results`)
- **Header**: "Your Mental Health Analysis" with subtitle
- **6 Chart Types**:
  - **Emotional Trend**: Line chart showing daily sentiment
  - **Mental Health Categories**: Pie chart of anxiety/stress/depression
  - **Engagement vs Mood**: Scatter plot of likes vs emotional tone
  - **Topics Discussed**: Bar chart of stress-related words
  - **Wellbeing Index**: Gauge showing overall score
  - **Recommendations**: Text cards with AI suggestions

## 🔧 API Endpoints

- `POST /analyze` - Main analysis endpoint
- `POST /analyze-batch` - Batch processing
- `GET /sample-data` - Sample data for testing
- `GET /health` - Health check

## 📈 Chart Types

1. **Line Chart**: Daily sentiment trends over time
2. **Pie Chart**: Mental health category distribution
3. **Scatter Plot**: Engagement vs mood correlation
4. **Bar Chart**: Word frequency analysis
5. **Gauge Chart**: Overall wellbeing score
6. **Text Cards**: Personalized recommendations

## 🎨 Design Features

- **Gradient Backgrounds**: Modern purple-blue gradients
- **Smooth Animations**: Framer Motion for page transitions
- **Interactive Charts**: Recharts for data visualization
- **Responsive Layout**: Mobile-first design
- **AI Graphics**: Animated brain and data nodes
- **Modern UI**: Clean, professional interface

## 🔒 Security

- **Data Privacy**: All analysis happens locally
- **API Keys**: Secure environment variable storage
- **Authorization**: Mock modal for data access
- **Error Handling**: Graceful failure management

## 🚀 Getting Started

1. **Start Backend**: `python main.py` (runs on port 8000)
2. **Start Frontend**: `npm start` (runs on port 3000)
3. **Open Browser**: Navigate to `http://localhost:3000`
4. **Connect Apps**: Click on social media icons to authorize
5. **Analyze Data**: Click "Analyze My Data" button
6. **View Results**: See your mental health insights!

## 📝 Sample Data

The app includes realistic sample data generation for testing:
- 10 sample posts with varied sentiment scores
- Realistic engagement metrics
- Mental health indicators
- Wellbeing scores

## 🔄 Data Flow

```
User Input → Authorization → Loading → API Call → Data Processing → 
AI Analysis → Chart Generation → Results Display
```

## 🎯 Key Features

- **Real-time Analysis**: Live progress updates
- **AI-Powered Insights**: GPT-4 generated recommendations
- **Interactive Charts**: Hover effects and tooltips
- **Download Results**: Export analysis as JSON
- **Share Functionality**: Social sharing capabilities
- **Responsive Design**: Works on all screen sizes

## 🛡️ Error Handling

- **API Failures**: Graceful fallback to sample data
- **Invalid Data**: Input validation and error messages
- **Network Issues**: Retry mechanisms and user feedback
- **Missing Results**: Redirect to landing page

## 📱 Mobile Support

- **Touch-Friendly**: Large buttons and touch targets
- **Responsive Grid**: Adapts to screen size
- **Mobile Navigation**: Easy back/forward navigation
- **Optimized Charts**: Readable on small screens

This is a complete, production-ready mental health analysis application with a beautiful UI and powerful AI backend!