#!/bin/bash
# setup.sh - Setup script for Autonomous Code Refactoring Agent

echo "🔧 Setting up Autonomous Code Refactoring Agent..."

# Create project structure
echo "📁 Creating project structure..."
mkdir -p code_refactor_agent/{agents,tools,crew,ui}

# Create __init__.py files
touch code_refactor_agent/__init__.py
touch code_refactor_agent/agents/__init__.py
touch code_refactor_agent/tools/__init__.py
touch code_refactor_agent/crew/__init__.py
touch code_refactor_agent/ui/__init__.py

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Check if Ollama is installed
if command -v ollama &> /dev/null; then
    echo "✅ Ollama found"
    
    # Check if deepseek-coder model is available
    if ollama list | grep -q "deepseek-coder"; then
        echo "✅ DeepSeek Coder model found"
    else
        echo "📥 Downloading DeepSeek Coder model..."
        ollama pull deepseek-coder:6.7b
    fi
else
    echo "⚠️  Ollama not found. Please install Ollama first:"
    echo "   Visit: https://ollama.ai/"
    echo "   Or run: curl -fsSL https://ollama.ai/install.sh | sh"
fi

# Create example test project
echo "📝 Creating example test project..."
mkdir -p test_project
cat > test_project/example.py << 'EOF'
# Example Python file for testing the refactoring agent
import os
import sys

def calculate(x, y):
    # TODO: Add docstring
    result = x + y * 2
    if result > 100:
        return result
    else:
        return result * 2

class DataProcessor:
    def __init__(self):
        self.data = []
        self.processed = False
    
    def process_data(self, input_data):
        # This function is too complex and needs refactoring
        if input_data is None:
            return None
        
        processed_data = []
        for item in input_data:
            if isinstance(item, str):
                if len(item) > 10:
                    processed_item = item.upper()[:10]
                else:
                    processed_item = item.upper()
            elif isinstance(item, int):
                if item > 0:
                    processed_item = item * 2
                else:
                    processed_item = 0
            else:
                processed_item = str(item)
            
            processed_data.append(processed_item)
        
        self.data = processed_data
        self.processed = True
        return processed_data

def main():
    processor = DataProcessor()
    test_data = ["hello world", 42, -5, "short", "this is a very long string"]
    result = processor.process_data(test_data)
    print("Processed data:", result)
    
    calc_result = calculate(10, 20)
    print("Calculation result:", calc_result)

if __name__ == "__main__":
    main()
EOF

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 Quick Start:"
echo "1. Start Ollama service: ollama serve"
echo "2. Run analysis: python main.py --target-dir ./test_project --mode analysis"
echo "3. Launch UI: python main.py --ui"
echo ""
echo "📚 Usage Examples:"
echo "  # Analyze code only:"
echo "  python main.py --target-dir /path/to/project --mode analysis"
echo ""
echo "  # Full refactoring with backup:"
echo "  python main.py --target-dir /path/to/project --mode refactor --backup"
echo ""
echo "  # Launch web UI:"
echo "  python main.py --ui"
echo ""