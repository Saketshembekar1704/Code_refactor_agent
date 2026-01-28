# Simple test version of refactor_crew.py with better error handling

from crewai import Crew, Task, Process
from langchain_ollama import OllamaLLM
import os
import json

class SimpleRefactorTest:
    def __init__(self):
        """Initialize with simple Ollama configuration and error handling"""
        try:
            print("🔍 Initializing Ollama LLM (1.5B model for speed)...")
            # Use OllamaLLM directly with timeout
            self.llm = OllamaLLM(
                model="deepseek-r1:1.5b",
                base_url="http://localhost:11434",
                timeout=30  # 30 second timeout
            )
            print("✅ LLM initialized successfully!")
            
        except Exception as e:
            print(f"❌ Failed to initialize LLM: {e}")
            raise
            
    def test_llm_call(self):
        """Test a simple LLM call"""
        try:
            print("🔍 Testing LLM call...")
            response = self.llm.invoke("Hello! Please respond with just 'Hi there!'")
            print(f"✅ LLM call successful! Response: {response}")
            return True
        except Exception as e:
            print(f"❌ LLM call failed: {e}")
            return False

if __name__ == "__main__":
    print("🧪 Testing Ollama LLM Configuration")
    print("=" * 40)
    
    try:
        test = SimpleRefactorTest()
        success = test.test_llm_call()
        
        if success:
            print("\n✅ All tests passed! The LLM configuration is working.")
        else:
            print("\n❌ LLM test failed. Check your Ollama setup.")
            
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        print("\nTroubleshooting steps:")
        print("1. Make sure Ollama is running: ollama serve")
        print("2. Check if the model is available: ollama list")
        print("3. If model is missing, pull it: ollama pull deepseek-r1:14b")