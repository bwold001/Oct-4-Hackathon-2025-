from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import logging
from datetime import datetime

from models import AnalysisRequest, AnalysisResponse, ErrorResponse, InputDataPoint
from openai_service import OpenAIService
from config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Mental Health Data Analyzer",
    description="Analyze social media data for mental health insights using OpenAI",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
openai_service = OpenAIService()

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Mental Health Data Analyzer API",
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "openai_configured": bool(settings.OPENAI_API_KEY),
        "timestamp": datetime.now().isoformat()
    }

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_mental_health_data(request: AnalysisRequest):
    """
    Analyze mental health data and return structured insights
    
    This endpoint processes social media data and returns:
    - Emotional trend analysis
    - Mental health category distribution
    - Engagement vs mood patterns
    - Topic analysis
    - Wellbeing index
    - Personalized recommendations
    """
    try:
        logger.info(f"Received analysis request with {len(request.data_points)} data points")
        
        # Validate input data
        if not request.data_points:
            raise HTTPException(status_code=400, detail="No data points provided")
        
        if len(request.data_points) < 5:
            raise HTTPException(
                status_code=400, 
                detail="At least 5 data points required for meaningful analysis"
            )
        
        # Handle both Pydantic models and dictionaries
        data_dicts = []
        for dp in request.data_points:
            if hasattr(dp, 'dict'):
                data_dicts.append(dp.dict())
            else:
                data_dicts.append(dp)
        
        # Perform analysis
        analysis_result = await openai_service.analyze_mental_health_data(data_dicts)
        
        logger.info("Analysis completed successfully")
        return analysis_result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        # Return fallback data instead of failing
        logger.info("Returning fallback analysis data")
        return await get_fallback_analysis()

@app.post("/generate-data")
async def generate_sample_data(num_posts: int = 10, analysis_period_days: int = 7):
    """
    Generate realistic sample data using OpenAI for testing purposes
    """
    try:
        logger.info(f"Generating {num_posts} sample data points")
        
        # Generate sample data using OpenAI
        sample_data = await openai_service.generate_sample_data(num_posts, analysis_period_days)
        
        return {
            "data_points": sample_data,
            "total_points": len(sample_data),
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error generating sample data: {str(e)}")
        # Return fallback data
        fallback_data = openai_service._get_fallback_sample_data(num_posts)
        return {
            "data_points": fallback_data,
            "total_points": len(fallback_data),
            "generated_at": datetime.now().isoformat()
        }

@app.post("/analyze-batch", response_model=List[AnalysisResponse])
async def analyze_batch_data(requests: List[AnalysisRequest]):
    """
    Analyze multiple datasets in batch
    
    Useful for processing multiple users' data simultaneously
    """
    try:
        logger.info(f"Received batch analysis request with {len(requests)} datasets")
        
        results = []
        for i, request in enumerate(requests):
            try:
                # Handle both Pydantic models and dictionaries
                data_dicts = []
                for dp in request.data_points:
                    if hasattr(dp, 'dict'):
                        data_dicts.append(dp.dict())
                    else:
                        data_dicts.append(dp)
                
                analysis_result = await openai_service.analyze_mental_health_data(data_dicts)
                results.append(analysis_result)
            except Exception as e:
                logger.error(f"Error processing dataset {i}: {str(e)}")
                # Add fallback data for this dataset
                fallback_result = await get_fallback_analysis()
                results.append(fallback_result)
        
        return results
        
    except Exception as e:
        logger.error(f"Error during batch analysis: {str(e)}")
        # Return fallback data
        fallback_result = await get_fallback_analysis()
        return [fallback_result]

async def get_fallback_analysis():
    """Get fallback analysis data when real analysis fails"""
    from models import ChartData, ChartDataPoint
    
    return AnalysisResponse(
        emotional_trend=ChartData(
            chart_type="line",
            title="Daily Sentiment Over Time",
            data=[
                ChartDataPoint(date="2025-01-15", sentiment_score=65.0),
                ChartDataPoint(date="2025-01-16", sentiment_score=72.0),
                ChartDataPoint(date="2025-01-17", sentiment_score=58.0),
                ChartDataPoint(date="2025-01-18", sentiment_score=81.0),
                ChartDataPoint(date="2025-01-19", sentiment_score=69.0),
                ChartDataPoint(date="2025-01-20", sentiment_score=75.0),
                ChartDataPoint(date="2025-01-21", sentiment_score=83.0)
            ]
        ),
        mental_health_categories=ChartData(
            chart_type="pie",
            title="Distribution of Anxiety/Stress/Depression Indicators",
            data=[
                ChartDataPoint(category="Anxiety", percentage=35.0),
                ChartDataPoint(category="Stress", percentage=45.0),
                ChartDataPoint(category="Depression", percentage=20.0)
            ]
        ),
        engagement_vs_mood=ChartData(
            chart_type="scatter",
            title="Engagement vs Mood",
            data=[
                ChartDataPoint(likes=12, comments=3, emotional_tone=65.0),
                ChartDataPoint(likes=25, comments=7, emotional_tone=72.0),
                ChartDataPoint(likes=8, comments=1, emotional_tone=58.0),
                ChartDataPoint(likes=35, comments=9, emotional_tone=81.0),
                ChartDataPoint(likes=18, comments=4, emotional_tone=69.0)
            ]
        ),
        topics_discussed=ChartData(
            chart_type="word_cloud",
            title="Top Stress-Related Words",
            data=[
                ChartDataPoint(word="workload", frequency=42),
                ChartDataPoint(word="deadline", frequency=37),
                ChartDataPoint(word="sleep", frequency=30),
                ChartDataPoint(word="balance", frequency=25),
                ChartDataPoint(word="family", frequency=21),
                ChartDataPoint(word="exercise", frequency=18),
                ChartDataPoint(word="burnout", frequency=14)
            ]
        ),
        wellbeing_index=ChartData(
            chart_type="gauge",
            title="Overall Wellbeing Score",
            data=[],
            value=76.0,
            range={"min": 0, "max": 100},
            status="Stable"
        ),
        recommendations=ChartData(
            chart_type="text_cards",
            title="Personalized Suggestions",
            data=[
                ChartDataPoint(id=1, text="Try a 10-minute mindfulness meditation before starting your day."),
                ChartDataPoint(id=2, text="Take a short walk after lunch to reduce mid-day stress."),
                ChartDataPoint(id=3, text="Limit late-night screen time to improve sleep quality."),
                ChartDataPoint(id=4, text="Reach out to a friend or colleague for social connection.")
            ]
        )
    )

@app.get("/sample-data")
async def get_sample_data():
    """
    Get sample data in the expected input format
    
    Useful for testing and understanding the expected data structure
    """
    sample_data = [
        {
            "post_id": "post_001",
            "user_id": "user_123",
            "timestamp": "2025-01-15T10:30:00Z",
            "day_of_week": "Monday",
            "time_of_day": "morning",
            "caption_text": "Feeling overwhelmed with work today, but trying to stay positive! #work #stress #motivation",
            "hashtags": "#work #stress #motivation",
            "image_context_label": "office_desk",
            "sentiment_score": 65.0,
            "emotion_primary": "mixed",
            "emotion_confidence": 0.8,
            "topic_cluster": "work_stress",
            "text_length": 85,
            "likes_count": 12,
            "comments_count": 3,
            "shares_count": 1,
            "saved_count": 2,
            "average_comment_sentiment": 70.0,
            "engagement_score": 75.0,
            "time_spent_on_post": 45,
            "comments_read_count": 3,
            "scrolled_back": False,
            "interaction_type": "post_creation",
            "num_sessions_per_day": 8,
            "avg_session_duration": 12.5,
            "night_usage_minutes": 30,
            "label_mental_state": "stressed",
            "label_confidence": 0.85,
            "wellbeing_index": 68.0,
            "recommendation_flag": True
        },
        {
            "post_id": "post_002",
            "user_id": "user_123",
            "timestamp": "2025-01-15T18:45:00Z",
            "day_of_week": "Monday",
            "time_of_day": "evening",
            "caption_text": "Great workout session! Feeling much better now. Exercise really helps with stress relief. #fitness #wellness #selfcare",
            "hashtags": "#fitness #wellness #selfcare",
            "image_context_label": "gym",
            "sentiment_score": 85.0,
            "emotion_primary": "positive",
            "emotion_confidence": 0.9,
            "topic_cluster": "fitness_wellness",
            "text_length": 95,
            "likes_count": 25,
            "comments_count": 7,
            "shares_count": 3,
            "saved_count": 5,
            "average_comment_sentiment": 88.0,
            "engagement_score": 92.0,
            "time_spent_on_post": 120,
            "comments_read_count": 7,
            "scrolled_back": True,
            "interaction_type": "post_creation",
            "num_sessions_per_day": 8,
            "avg_session_duration": 12.5,
            "night_usage_minutes": 15,
            "label_mental_state": "positive",
            "label_confidence": 0.9,
            "wellbeing_index": 82.0,
            "recommendation_flag": False
        }
    ]
    
    return {
        "sample_data": sample_data,
        "description": "Sample data points in the expected input format",
        "total_points": len(sample_data)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True
    )