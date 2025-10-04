import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any
from models import InputDataPoint, ChartDataPoint, ChartData
import re
from collections import Counter

class DataProcessor:
    """Processes input data and prepares it for OpenAI analysis"""
    
    def __init__(self):
        self.mental_health_keywords = {
            'anxiety': ['anxiety', 'worried', 'nervous', 'panic', 'stress', 'overwhelmed'],
            'depression': ['depressed', 'sad', 'down', 'hopeless', 'empty', 'worthless'],
            'stress': ['stressed', 'pressure', 'deadline', 'overwhelmed', 'burnout', 'exhausted']
        }
    
    def process_data(self, data_points: List[InputDataPoint]) -> Dict[str, Any]:
        """Process raw data points and extract insights"""
        df = pd.DataFrame([dp.dict() for dp in data_points])
        
        # Convert timestamp to datetime if it's not already
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Sort by timestamp
        df = df.sort_values('timestamp')
        
        # Calculate daily aggregates
        daily_data = self._calculate_daily_aggregates(df)
        
        # Extract mental health indicators
        mental_health_indicators = self._extract_mental_health_indicators(df)
        
        # Analyze engagement patterns
        engagement_patterns = self._analyze_engagement_patterns(df)
        
        # Extract topic analysis
        topic_analysis = self._analyze_topics(df)
        
        # Calculate wellbeing metrics
        wellbeing_metrics = self._calculate_wellbeing_metrics(df)
        
        return {
            'daily_data': daily_data,
            'mental_health_indicators': mental_health_indicators,
            'engagement_patterns': engagement_patterns,
            'topic_analysis': topic_analysis,
            'wellbeing_metrics': wellbeing_metrics,
            'raw_data': df
        }
    
    def _calculate_daily_aggregates(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate daily aggregated metrics"""
        df['date'] = df['timestamp'].dt.date
        
        daily_agg = df.groupby('date').agg({
            'sentiment_score': 'mean',
            'engagement_score': 'mean',
            'wellbeing_index': 'mean',
            'likes_count': 'sum',
            'comments_count': 'sum',
            'shares_count': 'sum',
            'time_spent_on_post': 'sum',
            'night_usage_minutes': 'sum'
        }).reset_index()
        
        return daily_agg.to_dict('records')
    
    def _extract_mental_health_indicators(self, df: pd.DataFrame) -> Dict[str, float]:
        """Extract mental health category percentages"""
        total_posts = len(df)
        categories = {'Anxiety': 0, 'Stress': 0, 'Depression': 0}
        
        for _, row in df.iterrows():
            text = str(row['caption_text']).lower()
            hashtags = str(row['hashtags']).lower()
            combined_text = f"{text} {hashtags}"
            
            # Check for anxiety indicators
            if any(keyword in combined_text for keyword in self.mental_health_keywords['anxiety']):
                categories['Anxiety'] += 1
            
            # Check for stress indicators
            if any(keyword in combined_text for keyword in self.mental_health_keywords['stress']):
                categories['Stress'] += 1
            
            # Check for depression indicators
            if any(keyword in combined_text for keyword in self.mental_health_keywords['depression']):
                categories['Depression'] += 1
        
        # Convert to percentages
        for category in categories:
            categories[category] = (categories[category] / total_posts) * 100
        
        return categories
    
    def _analyze_engagement_patterns(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Analyze engagement vs mood patterns"""
        patterns = []
        
        for _, row in df.iterrows():
            patterns.append({
                'likes': int(row['likes_count']),
                'comments': int(row['comments_count']),
                'emotional_tone': float(row['sentiment_score'])
            })
        
        return patterns
    
    def _analyze_topics(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Extract stress-related words and their frequencies"""
        all_text = []
        
        for _, row in df.iterrows():
            # Combine caption and hashtags
            text = f"{row['caption_text']} {row['hashtags']}"
            all_text.append(text)
        
        # Extract words (simple tokenization)
        words = []
        for text in all_text:
            # Remove special characters and split
            clean_text = re.sub(r'[^\w\s]', ' ', str(text).lower())
            words.extend(clean_text.split())
        
        # Filter for stress-related words
        stress_words = [
            'workload', 'deadline', 'sleep', 'balance', 'family', 
            'exercise', 'burnout', 'pressure', 'stress', 'tired',
            'overwhelmed', 'anxious', 'worried', 'exhausted'
        ]
        
        word_freq = Counter(words)
        stress_word_freq = {word: word_freq[word] for word in stress_words if word in word_freq}
        
        # Sort by frequency and take top 7
        sorted_words = sorted(stress_word_freq.items(), key=lambda x: x[1], reverse=True)[:7]
        
        return [{'word': word, 'frequency': freq} for word, freq in sorted_words]
    
    def _calculate_wellbeing_metrics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate overall wellbeing metrics"""
        avg_wellbeing = df['wellbeing_index'].mean()
        avg_sentiment = df['sentiment_score'].mean()
        avg_engagement = df['engagement_score'].mean()
        
        # Determine status based on wellbeing score
        if avg_wellbeing >= 80:
            status = "Excellent"
        elif avg_wellbeing >= 60:
            status = "Good"
        elif avg_wellbeing >= 40:
            status = "Stable"
        else:
            status = "Needs Attention"
        
        return {
            'wellbeing_score': float(avg_wellbeing),
            'sentiment_score': float(avg_sentiment),
            'engagement_score': float(avg_engagement),
            'status': status
        }
    
    def prepare_chart_data(self, processed_data: Dict[str, Any]) -> Dict[str, ChartData]:
        """Prepare data in the required chart format"""
        daily_data = processed_data['daily_data']
        mental_health = processed_data['mental_health_indicators']
        engagement = processed_data['engagement_patterns']
        topics = processed_data['topic_analysis']
        wellbeing = processed_data['wellbeing_metrics']
        
        # Emotional trend chart
        emotional_trend_data = [
            ChartDataPoint(
                date=str(day['date']),
                sentiment_score=round(day['sentiment_score'], 1)
            )
            for day in daily_data
        ]
        
        # Mental health categories chart
        mental_health_data = [
            ChartDataPoint(
                category=category,
                percentage=round(percentage, 1)
            )
            for category, percentage in mental_health.items()
        ]
        
        # Engagement vs mood chart
        engagement_data = [
            ChartDataPoint(
                likes=pattern['likes'],
                comments=pattern['comments'],
                emotional_tone=round(pattern['emotional_tone'], 1)
            )
            for pattern in engagement[:5]  # Limit to 5 data points for visualization
        ]
        
        # Topics discussed chart
        topics_data = [
            ChartDataPoint(
                word=topic['word'],
                frequency=topic['frequency']
            )
            for topic in topics
        ]
        
        # Wellbeing index chart
        wellbeing_data = ChartData(
            chart_type="gauge",
            title="Overall Wellbeing Score",
            data=[],
            value=round(wellbeing['wellbeing_score'], 1),
            range={"min": 0, "max": 100},
            status=wellbeing['status']
        )
        
        # Recommendations (will be generated by OpenAI)
        recommendations_data = ChartData(
            chart_type="text_cards",
            title="Personalized Suggestions",
            data=[]
        )
        
        return {
            'emotional_trend': ChartData(
                chart_type="line",
                title="Daily Sentiment Over Time",
                data=emotional_trend_data
            ),
            'mental_health_categories': ChartData(
                chart_type="pie",
                title="Distribution of Anxiety/Stress/Depression Indicators",
                data=mental_health_data
            ),
            'engagement_vs_mood': ChartData(
                chart_type="scatter",
                title="Engagement vs Mood",
                data=engagement_data
            ),
            'topics_discussed': ChartData(
                chart_type="word_cloud",
                title="Top Stress-Related Words",
                data=topics_data
            ),
            'wellbeing_index': wellbeing_data,
            'recommendations': recommendations_data
        }
