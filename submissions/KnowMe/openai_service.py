import json
from typing import Dict, Any, List
from openai import OpenAI
from config import settings
from models import AnalysisResponse, ChartData, ChartDataPoint
from data_processor import DataProcessor
from datetime import datetime, timedelta
import random
import re

class OpenAIService:
    """Service for interacting with OpenAI API to generate mental health insights"""
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.data_processor = DataProcessor()
    
    async def analyze_mental_health_data(self, data_points: List[Dict[str, Any]]) -> AnalysisResponse:
        """Analyze mental health data using OpenAI and return structured response"""
        
        # Process the data first
        processed_data = self.data_processor.process_data(data_points)
        chart_data = self.data_processor.prepare_chart_data(processed_data)
        
        # Prepare context for OpenAI
        context = self._prepare_analysis_context(processed_data)
        
        # Generate recommendations using OpenAI
        recommendations = await self._generate_recommendations(context)
        
        # Update recommendations in chart data
        chart_data['recommendations'].data = [
            ChartDataPoint(id=i+1, text=rec) 
            for i, rec in enumerate(recommendations)
        ]
        
        return AnalysisResponse(
            emotional_trend=chart_data['emotional_trend'],
            mental_health_categories=chart_data['mental_health_categories'],
            engagement_vs_mood=chart_data['engagement_vs_mood'],
            topics_discussed=chart_data['topics_discussed'],
            wellbeing_index=chart_data['wellbeing_index'],
            recommendations=chart_data['recommendations']
        )
    
    async def generate_sample_data(self, num_posts: int = 10, analysis_period_days: int = 7) -> List[Dict[str, Any]]:
        """Generate realistic sample data using OpenAI"""
        
        system_prompt = """You are a data generator for mental health analysis. Generate realistic social media posts that would be used for mental health analysis.
        
        For each post, generate data that includes:
        - Realistic captions about daily life, work, relationships, health, etc.
        - Appropriate hashtags
        - Sentiment scores (0-100)
        - Engagement metrics (likes, comments, shares)
        - Mental health indicators
        - Wellbeing scores
        
        Make the data realistic and varied - some positive posts, some stressful, some neutral.
        Include posts about work stress, relationships, fitness, sleep, family, etc.
        """
        
        user_prompt = f"""Generate {num_posts} realistic social media posts for mental health analysis.
        
        Each post should have all these fields:
        - post_id: unique identifier
        - user_id: "user_123"
        - timestamp: ISO format within last {analysis_period_days} days
        - day_of_week: day name
        - time_of_day: "morning", "afternoon", or "evening"
        - caption_text: realistic social media caption
        - hashtags: relevant hashtags
        - image_context_label: context like "office_desk", "gym", "home", "outdoor", "social_gathering"
        - sentiment_score: 0-100
        - emotion_primary: "positive", "mixed", "negative", "neutral"
        - emotion_confidence: 0.7-1.0
        - topic_cluster: "work_stress", "fitness_wellness", "social_connection", "sleep_issues", "family_time"
        - text_length: character count
        - likes_count: 5-50
        - comments_count: 0-15
        - shares_count: 0-8
        - saved_count: 0-5
        - average_comment_sentiment: 0-100
        - engagement_score: 30-95
        - time_spent_on_post: 30-300 seconds
        - comments_read_count: 0-10
        - scrolled_back: true/false
        - interaction_type: "post_creation"
        - num_sessions_per_day: 5-15
        - avg_session_duration: 8-25 minutes
        - night_usage_minutes: 10-120
        - label_mental_state: "positive", "stressed", "anxious", "depressed", "neutral"
        - label_confidence: 0.7-1.0
        - wellbeing_index: 30-90
        - recommendation_flag: true/false
        
        Return as a JSON array of objects.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.8,
                max_tokens=4000
            )
            
            generated_text = response.choices[0].message.content.strip()
            
            # Parse JSON response
            try:
                sample_data = json.loads(generated_text)
                if isinstance(sample_data, list) and len(sample_data) >= num_posts:
                    return sample_data[:num_posts]
                else:
                    return self._get_fallback_sample_data(num_posts)
            except json.JSONDecodeError:
                return self._get_fallback_sample_data(num_posts)
                
        except Exception as e:
            print(f"Error generating sample data with OpenAI: {e}")
            return self._get_fallback_sample_data(num_posts)
    
    def _get_fallback_sample_data(self, num_posts: int) -> List[Dict[str, Any]]:
        """Fallback sample data if OpenAI fails"""
        sample_data = []
        
        captions = [
            "Feeling overwhelmed with work today, but trying to stay positive! #work #stress #motivation",
            "Great workout session! Feeling much better now. #fitness #wellness #selfcare",
            "Had a rough day, but grateful for my friends who always support me. #grateful #friends #support",
            "Can't sleep again... too much on my mind. #insomnia #anxiety #sleep",
            "Celebrating a small win at work today! #achievement #work #success",
            "Feeling lonely lately, need to reach out to people more. #loneliness #social #connection",
            "Beautiful sunset walk helped clear my mind. #nature #mindfulness #peace",
            "Stressed about the upcoming presentation, but I'll get through it. #presentation #stress #confidence",
            "Spent quality time with family today, feeling blessed. #family #gratitude #love",
            "Another day of working from home, missing the office social interaction. #wfh #isolation #work"
        ]
        
        emotions = ['positive', 'mixed', 'negative', 'neutral']
        mental_states = ['positive', 'stressed', 'anxious', 'depressed', 'neutral']
        topics = ['work_stress', 'fitness_wellness', 'social_connection', 'sleep_issues', 'family_time']
        
        for i in range(num_posts):
            timestamp = datetime.now() - timedelta(days=random.randint(0, 6), hours=random.randint(0, 23))
            caption = random.choice(captions)
            emotion = random.choice(emotions)
            mental_state = random.choice(mental_states)
            topic = random.choice(topics)
            
            # Extract hashtags from caption using regex
            hashtags = ' '.join(re.findall(r'#\w+', caption))
            
            sample_data.append({
                "post_id": f"post_{i+1:03d}",
                "user_id": "user_123",
                "timestamp": timestamp.isoformat() + "Z",
                "day_of_week": timestamp.strftime("%A"),
                "time_of_day": "morning" if timestamp.hour < 12 else "afternoon" if timestamp.hour < 18 else "evening",
                "caption_text": caption,
                "hashtags": hashtags,
                "image_context_label": random.choice(["office_desk", "gym", "home", "outdoor", "social_gathering"]),
                "sentiment_score": round(random.uniform(20, 80), 1),
                "emotion_primary": emotion,
                "emotion_confidence": round(random.uniform(0.7, 1.0), 2),
                "topic_cluster": topic,
                "text_length": len(caption),
                "likes_count": random.randint(5, 50),
                "comments_count": random.randint(0, 15),
                "shares_count": random.randint(0, 8),
                "saved_count": random.randint(0, 5),
                "average_comment_sentiment": round(random.uniform(20, 80), 1),
                "engagement_score": round(random.uniform(30, 95), 1),
                "time_spent_on_post": random.randint(30, 300),
                "comments_read_count": random.randint(0, 10),
                "scrolled_back": random.choice([True, False]),
                "interaction_type": "post_creation",
                "num_sessions_per_day": random.randint(5, 15),
                "avg_session_duration": round(random.uniform(8, 25), 1),
                "night_usage_minutes": random.randint(10, 120),
                "label_mental_state": mental_state,
                "label_confidence": round(random.uniform(0.7, 1.0), 2),
                "wellbeing_index": round(random.uniform(30, 90), 1),
                "recommendation_flag": random.choice([True, False])
            })
        
        return sample_data
    
    def _prepare_analysis_context(self, processed_data: Dict[str, Any]) -> str:
        """Prepare context string for OpenAI analysis"""
        daily_data = processed_data['daily_data']
        mental_health = processed_data['mental_health_indicators']
        wellbeing = processed_data['wellbeing_metrics']
        topics = processed_data['topic_analysis']
        
        context = f"""
        Mental Health Analysis Context:
        
        Daily Sentiment Trends:
        {json.dumps(daily_data, indent=2, default=str)}
        
        Mental Health Category Distribution:
        {json.dumps(mental_health, indent=2)}
        
        Wellbeing Metrics:
        - Overall Wellbeing Score: {wellbeing['wellbeing_score']:.1f}/100
        - Average Sentiment: {wellbeing['sentiment_score']:.1f}/100
        - Engagement Score: {wellbeing['engagement_score']:.1f}/100
        - Status: {wellbeing['status']}
        
        Top Stress-Related Topics:
        {json.dumps(topics, indent=2)}
        
        Analysis Period: {len(daily_data)} days
        """
        
        return context
    
    async def _generate_recommendations(self, context: str) -> List[str]:
        """Generate personalized recommendations using OpenAI"""
        
        system_prompt = """You are a mental health AI assistant specializing in social media and digital wellness analysis. 
        Based on the provided data about a user's social media posts, engagement patterns, and wellbeing metrics, 
        generate 4 personalized, actionable recommendations to improve their mental health and digital wellness.
        
        Focus on:
        1. Practical, implementable suggestions
        2. Digital wellness and screen time management
        3. Mental health improvement strategies
        4. Social connection and engagement optimization
        
        Keep recommendations concise (1-2 sentences each) and encouraging in tone.
        """
        
        user_prompt = f"""
        Please analyze this mental health data and provide 4 personalized recommendations:
        
        {context}
        
        Return only the recommendations as a JSON array of strings, no additional text.
        Example format: ["Recommendation 1", "Recommendation 2", "Recommendation 3", "Recommendation 4"]
        """
        
        try:
            response = self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            recommendations_text = response.choices[0].message.content.strip()
            
            # Parse JSON response
            try:
                recommendations = json.loads(recommendations_text)
                if isinstance(recommendations, list) and len(recommendations) >= 4:
                    return recommendations[:4]  # Ensure we have exactly 4
                else:
                    return self._get_fallback_recommendations()
            except json.JSONDecodeError:
                return self._get_fallback_recommendations()
                
        except Exception as e:
            print(f"Error generating recommendations: {e}")
            return self._get_fallback_recommendations()
    
    def _get_fallback_recommendations(self) -> List[str]:
        """Fallback recommendations if OpenAI fails"""
        return [
            "Try a 10-minute mindfulness meditation before starting your day.",
            "Take a short walk after lunch to reduce mid-day stress.",
            "Limit late-night screen time to improve sleep quality.",
            "Reach out to a friend or colleague for social connection."
        ]
    
    async def enhance_analysis_with_ai(self, chart_data: Dict[str, ChartData]) -> Dict[str, ChartData]:
        """Enhance the analysis with AI-generated insights"""
        
        # This could be expanded to use AI for more sophisticated analysis
        # For now, we'll return the processed data as-is
        return chart_data