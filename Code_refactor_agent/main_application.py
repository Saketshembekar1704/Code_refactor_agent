# main.py
import os
import sys
import argparse
from dotenv import load_dotenv
from crew.refactor_crew import RefactorCrew
import json
from datetime import datetime

def setup_environment():
    """Setup environment variables and configuration"""
    load_dotenv()
    
    # Set default LLM configuration for CrewAI to work with Ollama
    if not os.getenv("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = "ollama"  # Placeholder for local LLM
    
    # Configure Ollama settings with the faster 1.5B model
    os.environ["OPENAI_API_BASE"] = os.getenv("OLLAMA_URL", "http://localhost:11434/v1")
    os.environ["OPENAI_MODEL_NAME"] = os.getenv("OLLAMA_MODEL", "ollama/deepseek-r1:1.5b")

def main():
    """Main application entry point"""
    parser = argparse.ArgumentParser(description="Autonomous Code Refactoring Agent")
    parser.add_argument("--target-dir", required=True, help="Target directory to refactor")
    parser.add_argument("--mode", choices=["analysis", "refactor"], default="analysis", 
                       help="Operation mode: analysis only or full refactoring")
    parser.add_argument("--ui", action="store_true", help="Launch Streamlit UI")
    parser.add_argument("--backup", action="store_true", default=True, help="Create backup before changes")
    
    args = parser.parse_args()
    
    # Setup environment
    setup_environment()
    
    if args.ui:
        # Launch Streamlit UI (point to streamlit_ui.py, not old name)
        print("Launching Streamlit UI...")
        os.system("streamlit run ui/streamlit_ui.py")
        return
    
    if not os.path.exists(args.target_dir):
        print(f"Error: Directory '{args.target_dir}' not found")
        sys.exit(1)
    
    print(f"🔧 Autonomous Code Refactoring Agent")
    print(f"Target Directory: {args.target_dir}")
    print(f"Mode: {args.mode}")
    print("=" * 50)
    
    # Initialize crew
    crew = RefactorCrew()
    
    try:
        # optional backup for refactor mode
        if args.mode == "refactor" and args.backup:
            print("💾 Creating backup...")
            backup_dir = args.target_dir + "_backup"
            import shutil
            try:
                shutil.copytree(args.target_dir, backup_dir)
                print(f"✅ Backup created: {backup_dir}")
            except Exception as e:
                print(f"❌ Backup failed: {e}")
                sys.exit(1)

        # unified kickoff call
        inputs = {
            "target_directory": args.target_dir,
            "mode": args.mode,
        }
        print("🚀 Running crew...")
        result = crew.kickoff(inputs)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if args.mode == "analysis":
            # Save analysis result
            text_filename = f"analysis_report_{timestamp}.txt"
            with open(text_filename, "w", encoding="utf-8") as f:
                f.write("Code Refactoring Agent - Analysis Report\n")
                f.write("=" * 50 + "\n")
                f.write(f"Timestamp: {datetime.now().isoformat()}\n")
                f.write(f"Target Directory: {args.target_dir}\n")
                f.write(f"Mode: {args.mode}\n\n")
                f.write(json.dumps(result, indent=2, ensure_ascii=False))
            print(f"\n💾 Analysis report saved: {text_filename}")
            print("\n📊 Analysis Summary:")
            print("-" * 30)
            print(result.get("summary", result))
        else:
            # Save refactor result
            report_filename = f"refactoring_report_{timestamp}.json"
            with open(report_filename, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Refactoring report saved to: {report_filename}")
            print("\n📋 Refactoring Summary:")
            print("-" * 30)
            print(result.get("summary", result))

    except KeyboardInterrupt:
        print("\n⏹️  Process interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()