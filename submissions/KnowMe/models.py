from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from enum import Enum

class InputDataPoint(BaseModel):
    """Individual data point matching the input format"""
    post_id: str
    user_id: str
    timestamp: datetime
    day_of_week: str
    time_of_day: str
    caption_text: str
    hashtags: str
    image_context_label: str
    sentiment_score: float
    emotion_primary: str
    emotion_confidence: float
    topic_cluster: str
    text_length: int
    likes_count: int
    comments_count: int
    shares_count: int
    saved_count: int
    average_comment_sentiment: float
    engagement_score: float
    time_spent_on_post: int
    comments_read_count: int
    scrolled_back: bool
    interaction_type: str
    num_sessions_per_day: int
    avg_session_duration: float
    night_usage_minutes: int
    label_mental_state: str
    label_confidence: float
    wellbeing_index: float
    recommendation_flag: bool

class AnalysisRequest(BaseModel):
    """Request model for data analysis"""
    data_points: List[InputDataPoint]
    analysis_period_days: Optional[int] = 7
    user_preferences: Optional[Dict[str, Any]] = None

# Output format models
class ChartDataPoint(BaseModel):
    """Generic data point for charts"""
    date: Optional[str] = None
    sentiment_score: Optional[float] = None
    category: Optional[str] = None
    percentage: Optional[float] = None
    likes: Optional[int] = None
    comments: Optional[int] = None
    emotional_tone: Optional[float] = None
    word: Optional[str] = None
    frequency: Optional[int] = None
    id: Optional[int] = None
    text: Optional[str] = None

class ChartData(BaseModel):
    """Chart data structure"""
    chart_type: str
    title: str
    data: List[ChartDataPoint]
    value: Optional[float] = None
    range: Optional[Dict[str, float]] = None
    status: Optional[str] = None

class AnalysisResponse(BaseModel):
    """Structured response matching the required output format"""
    emotional_trend: ChartData
    mental_health_categories: ChartData
    engagement_vs_mood: ChartData
    topics_discussed: ChartData
    wellbeing_index: ChartData
    recommendations: ChartData

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)
