import os
import ast
from litellm import completion
from dotenv import load_dotenv

load_dotenv()

# Force Ollama configuration
os.environ["OPENAI_API_BASE"] = "http://localhost:11434"
os.environ["OPENAI_API_KEY"] = "ollama"
os.environ["OPENAI_MODEL_NAME"] = "ollama/deepseek-r1:1.5b"

file_path = "test_project/complex_test.py"
with open(file_path, "r", encoding="utf-8") as f:
    original_source = f.read()

prompt = f"""
You are an expert Python refactoring agent.
Please refactor the following Python code to significantly improve its quality.

Your tasks:
1. Identify and extract duplicate code into helper functions or methods.
2. Simplify complex conditionals (e.g. nested if/else statements).
3. Improve variable and function naming to be descriptive and follow PEP 8.
4. Add missing docstrings.

Return ONLY the fully refactored Python code. Do not include markdown formatting like ```python, and do not include any explanations. The output should be directly executable.

Original Code:
{original_source}
"""

print("Sending request to litellm...")
try:
    response = completion(
        model=os.environ["OPENAI_MODEL_NAME"],
        messages=[{"role": "user", "content": prompt}],
        api_base=os.environ["OPENAI_API_BASE"],
        api_key=os.environ["OPENAI_API_KEY"]
    )
    
    new_source = response.choices[0].message.content.strip()
    print("--- RAW RESPONSE ---")
    print(new_source[:500] + "...\n(truncated)")
    
    if new_source.startswith("```python"):
        new_source = new_source[9:]
    if new_source.startswith("```"):
        new_source = new_source[3:]
    if new_source.endswith("```"):
        new_source = new_source[:-3]
        
    new_source = new_source.strip()
    
    print("--- PARSED SOURCE ---")
    print(new_source[:500] + "...\n(truncated)")
    
    ast.parse(new_source)
    print("Syntax check passed.")
    
except Exception as e:
    print(f"Error: {e}")
