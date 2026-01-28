# .env
# LLM Configuration
 OPENAI_API_KEY=ollama
 OPENAI_API_BASE=http://localhost:11434/v1
 OPENAI_MODEL_NAME=deepseek-coder:14b
 OLLAMA_MODEL=deepseek-coder:14b

# Alternative LLM Providers (uncomment and configure as needed)
# OPENAI_API_KEY=your_openai_api_key_here
# ANTHROPIC_API_KEY=your_anthropic_api_key_here

# CrewAI Configuration
CREWAI_TELEMETRY_OPT_OUT=true

# Application Settings
BACKUP_ENABLED=true
MAX_COMPLEXITY_THRESHOLD=10
DEFAULT_MODE=analysis