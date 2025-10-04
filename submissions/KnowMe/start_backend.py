#!/usr/bin/env python3
"""
Startup script for the KnowMe backend
"""
import subprocess
import sys
import os

def main():
    print("🚀 Starting KnowMe Backend...")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('main.py'):
        print("❌ Error: main.py not found. Please run this from the project root directory.")
        sys.exit(1)
    
    # Check if requirements are installed
    try:
        import fastapi
        import openai
        print("✅ Dependencies found")
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("Please run: pip install -r requirements.txt")
        sys.exit(1)
    
    # Check for OpenAI API key
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️  Warning: OPENAI_API_KEY not set in environment")
        print("Please set your OpenAI API key in config.py or as an environment variable")
    
    print("🌐 Starting server on http://localhost:8000")
    print("📚 API docs available at http://localhost:8000/docs")
    print("=" * 50)
    
    # Start the server
    try:
        subprocess.run([sys.executable, "main.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Server failed to start: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
