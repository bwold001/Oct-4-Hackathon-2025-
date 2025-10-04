"""
Test script for the Mental Health Data Analyzer API
Run this to test the API endpoints with sample data
"""

import requests
import json
from datetime import datetime, timedelta
import random

# API base URL
BASE_URL = "http://localhost:8000"

def generate_sample_data(num_points=10):
    """Generate sample data for testing"""
    data_points = []
    
    # Sample data templates
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
    
    emotions = ["positive", "mixed", "negative", "neutral"]
    mental_states = ["positive", "stressed", "anxious", "depressed", "neutral"]
    topics = ["work_stress", "fitness_wellness", "social_connection", "sleep_issues", "family_time"]
    
    for i in range(num_points):
        # Generate random timestamp within last 7 days
        days_ago = random.randint(0, 6)
        hours_ago = random.randint(0, 23)
        timestamp = datetime.now() - timedelta(days=days_ago, hours=hours_ago)
        
        caption = random.choice(captions)
        emotion = random.choice(emotions)
        mental_state = random.choice(mental_states)
        topic = random.choice(topics)
        
        # Generate realistic ranges for different metrics
        sentiment_score = random.uniform(30, 90)
        engagement_score = random.uniform(40, 95)
        wellbeing_index = random.uniform(40, 90)
        
        data_point = {
            "post_id": f"post_{i+1:03d}",
            "user_id": "user_123",
            "timestamp": timestamp.isoformat() + "Z",
            "day_of_week": timestamp.strftime("%A"),
            "time_of_day": "morning" if timestamp.hour < 12 else "afternoon" if timestamp.hour < 18 else "evening",
            "caption_text": caption,
            "hashtags": "#" + " #".join(caption.split("#")[1:]) if "#" in caption else "",
            "image_context_label": random.choice(["office_desk", "gym", "home", "outdoor", "social_gathering"]),
            "sentiment_score": round(sentiment_score, 1),
            "emotion_primary": emotion,
            "emotion_confidence": round(random.uniform(0.6, 0.95), 2),
            "topic_cluster": topic,
            "text_length": len(caption),
            "likes_count": random.randint(5, 50),
            "comments_count": random.randint(0, 15),
            "shares_count": random.randint(0, 8),
            "saved_count": random.randint(0, 5),
            "average_comment_sentiment": round(random.uniform(40, 90), 1),
            "engagement_score": round(engagement_score, 1),
            "time_spent_on_post": random.randint(30, 300),
            "comments_read_count": random.randint(0, 10),
            "scrolled_back": random.choice([True, False]),
            "interaction_type": random.choice(["post_creation", "comment", "like", "share"]),
            "num_sessions_per_day": random.randint(5, 15),
            "avg_session_duration": round(random.uniform(8, 25), 1),
            "night_usage_minutes": random.randint(10, 120),
            "label_mental_state": mental_state,
            "label_confidence": round(random.uniform(0.7, 0.95), 2),
            "wellbeing_index": round(wellbeing_index, 1),
            "recommendation_flag": random.choice([True, False])
        }
        
        data_points.append(data_point)
    
    return data_points

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_sample_data():
    """Test the sample data endpoint"""
    print("\nTesting sample data endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/sample-data")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Sample data points: {data['total_points']}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_analysis():
    """Test the main analysis endpoint"""
    print("\nTesting analysis endpoint...")
    try:
        # Generate sample data
        sample_data = generate_sample_data(8)
        
        # Prepare request
        request_data = {
            "data_points": sample_data,
            "analysis_period_days": 7
        }
        
        print(f"Sending {len(sample_data)} data points for analysis...")
        
        # Send request
        response = requests.post(
            f"{BASE_URL}/analyze",
            json=request_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("Analysis successful!")
            print(f"Emotional trend data points: {len(result['emotional_trend']['data'])}")
            print(f"Mental health categories: {len(result['mental_health_categories']['data'])}")
            print(f"Engagement data points: {len(result['engagement_vs_mood']['data'])}")
            print(f"Topic words: {len(result['topics_discussed']['data'])}")
            print(f"Recommendations: {len(result['recommendations']['data'])}")
            print(f"Wellbeing score: {result['wellbeing_index']['value']}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_batch_analysis():
    """Test the batch analysis endpoint"""
    print("\nTesting batch analysis endpoint...")
    try:
        # Generate multiple datasets
        datasets = []
        for i in range(2):
            sample_data = generate_sample_data(5)
            datasets.append({
                "data_points": sample_data,
                "analysis_period_days": 7
            })
        
        print(f"Sending {len(datasets)} datasets for batch analysis...")
        
        # Send request
        response = requests.post(
            f"{BASE_URL}/analyze-batch",
            json=datasets,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            results = response.json()
            print(f"Batch analysis successful! Processed {len(results)} datasets")
            return True
        else:
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Run all tests"""
    print("Mental Health Data Analyzer API Test Suite")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health_check),
        ("Sample Data", test_sample_data),
        ("Analysis", test_analysis),
        ("Batch Analysis", test_batch_analysis)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        success = test_func()
        results.append((test_name, success))
    
    print(f"\n{'='*50}")
    print("Test Results Summary:")
    print("=" * 50)
    
    for test_name, success in results:
        status = "PASS" if success else "FAIL"
        print(f"{test_name}: {status}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    print(f"\nOverall: {passed}/{total} tests passed")

if __name__ == "__main__":
    main()
