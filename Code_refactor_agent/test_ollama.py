#!/usr/bin/env python3
"""Simple test script to verify Ollama connection and model works"""

import requests
import json

def test_ollama_connection():
    """Test if Ollama is responding and model is available"""
    try:
        # Test 1: Check if Ollama is running
        print("🔍 Testing Ollama connection...")
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        
        if response.status_code == 200:
            models = response.json()
            print("✅ Ollama is running!")
            print(f"Available models: {[m['name'] for m in models['models']]}")
            
            # Check if deepseek-r1:1.5b is available
            model_names = [m['name'] for m in models['models']]
            if 'deepseek-r1:1.5b' in model_names:
                print("✅ deepseek-r1:1.5b model is available!")
                
                # Test 2: Try a simple generation
                print("\n🔍 Testing model generation...")
                test_generation()
            else:
                print("❌ deepseek-r1:1.5b model not found!")
                print("Available models:", model_names)
        else:
            print(f"❌ Ollama responded with status {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to connect to Ollama: {e}")
        print("Make sure Ollama is running: ollama serve")

def test_generation():
    """Test simple text generation with the model"""
    try:
        payload = {
            "model": "deepseek-r1:1.5b",
            "prompt": "Hello, how are you? Please respond briefly.",
            "stream": False
        }
        
        response = requests.post(
            "http://localhost:11434/api/generate",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Model generation test successful!")
            print(f"Response: {result.get('response', 'No response')[:100]}...")
        else:
            print(f"❌ Generation failed with status {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Generation request failed: {e}")

if __name__ == "__main__":
    test_ollama_connection()