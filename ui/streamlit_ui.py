# ui/streamlit_app.py
import streamlit as st
import os
import json
import tempfile
import shutil
import zipfile
from io import BytesIO
import sys
import time
import re

# Try to import optional dependencies with error handling
try:
    import git
    GIT_AVAILABLE = True
except ImportError:
    GIT_AVAILABLE = False

from pathlib import Path

# Add parent directory to path to import crew modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock RefactorCrew class for when the real one isn't available
class MockRefactorCrew:
    """Mock RefactorCrew for testing the UI without the actual crew implementation"""
    
    def __init__(self):
        pass
    
    def kickoff(self, inputs=None):
        """Mock kickoff method that simulates analysis/refactoring"""
        target_dir = inputs.get('target_directory', '') if inputs else ''
        mode = inputs.get('mode', 'analysis') if inputs else 'analysis'
        
        # Simulate some processing time
        time.sleep(2)
        
        if mode == 'analysis':
            return self._mock_analysis_result(target_dir)
        else:
            return self._mock_refactor_result(target_dir)
    
    def _mock_analysis_result(self, target_dir):
        """Generate mock analysis results"""
        return {
            "status": "completed",
            "mode": "analysis",
            "target_directory": target_dir,
            "summary": "Mock analysis completed successfully",
            "findings": {
                "code_quality_issues": [
                    "Long functions detected in module.py",
                    "Missing docstrings in 3 functions",
                    "Complex conditional statements found"
                ],
                "complexity_metrics": {
                    "average_complexity": 6.2,
                    "high_complexity_functions": 2,
                    "total_functions_analyzed": 15
                },
                "documentation_coverage": {
                    "functions_with_docstrings": "60%",
                    "classes_with_docstrings": "80%",
                    "modules_with_docstrings": "40%"
                }
            },
            "recommendations": [
                "Break down long functions into smaller ones",
                "Add comprehensive docstrings",
                "Simplify complex conditional logic"
            ]
        }
    
    def _mock_refactor_result(self, target_dir):
        """Generate mock refactoring results"""
        return {
            "status": "completed",
            "mode": "refactor",
            "target_directory": target_dir,
            "summary": "Mock refactoring completed successfully",
            "changes_applied": [
                "Added docstrings to 8 functions",
                "Refactored 2 complex functions",
                "Improved code formatting",
                "Added type hints where missing"
            ],
            "files_modified": [
                "main.py",
                "utils.py",
                "models/user.py"
            ],
            "backup_created": True
        }

# Try to import crew with error handling and fallback to mock
try:
    from crew.refactor_crew import RefactorCrew
    CREW_AVAILABLE = True
    USING_MOCK = False
except ImportError as e:
    RefactorCrew = MockRefactorCrew
    CREW_AVAILABLE = True  # We have a mock version
    USING_MOCK = True

def main():
    try:
        st.set_page_config(
            page_title="RefactorCrew: Autonomous Code Refactoring Agent",
            page_icon="🔧",
            layout="wide"
        )
        
        # Inject custom CSS to make the main container wider and code output
        # look like a proper code editor instead of a narrow phone screen.
        st.markdown(
            """
            <style>
                /* ── Global layout: use full viewport width ── */
                .block-container {
                    max-width: 100% !important;
                    padding: 1rem 2rem !important;
                }

                /* Remove every inner width cap Streamlit might set */
                .element-container,
                .stMarkdown,
                .stExpander,
                [data-testid="stExpander"],
                [data-testid="stExpanderDetails"],
                .streamlit-expanderContent {
                    max-width: 100% !important;
                    width: 100% !important;
                }

                /* ── Code blocks / diff viewer: full-width, editor-style ── */
                .stCodeBlock,
                .stCode,
                [data-testid="stCodeBlock"],
                [data-testid="stCode"] {
                    max-width: 100% !important;
                    width: 100% !important;
                }

                .stCodeBlock pre,
                .stCode pre,
                [data-testid="stCodeBlock"] pre,
                [data-testid="stCode"] pre {
                    max-width: 100% !important;
                    width: 100% !important;
                    white-space: pre !important;
                    overflow-x: auto !important;
                    font-family: 'Cascadia Code', 'Fira Code', 'JetBrains Mono',
                                 'Consolas', 'Courier New', monospace !important;
                    font-size: 0.875rem !important;
                    line-height: 1.65 !important;
                    tab-size: 4 !important;
                    border-radius: 8px !important;
                    padding: 1rem 1.25rem !important;
                }

                pre code, .stCodeBlock code, [data-testid="stCodeBlock"] code {
                    white-space: pre !important;
                    word-break: normal !important;
                    overflow-wrap: normal !important;
                    font-size: inherit !important;
                    line-height: inherit !important;
                    font-family: inherit !important;
                }

                /* ── Expander styling ── */
                .streamlit-expanderContent,
                [data-testid="stExpanderDetails"] {
                    padding: 0.75rem 1rem !important;
                    max-width: 100% !important;
                    width: 100% !important;
                }

                .streamlit-expanderHeader,
                [data-testid="stExpander"] summary {
                    font-size: 1.05rem !important;
                    font-weight: 600 !important;
                }

                /* ── Text areas (raw output) ── */
                .stTextArea textarea {
                    font-family: 'Cascadia Code', 'Fira Code', 'Consolas',
                                 'Courier New', monospace !important;
                    font-size: 0.875rem !important;
                    line-height: 1.55 !important;
                    max-width: 100% !important;
                    width: 100% !important;
                }

                /* ── Custom diff container (HTML-rendered diffs) ── */
                .diff-container {
                    width: 100% !important;
                    max-width: 100% !important;
                    overflow-x: auto;
                    background: #ffffff;
                    border: 1px solid #e1e4e8;
                    border-radius: 8px;
                    padding: 1rem 1.25rem;
                    font-family: 'Cascadia Code', 'Fira Code', 'JetBrains Mono',
                                 'Consolas', 'Courier New', monospace;
                    font-size: 0.875rem;
                    line-height: 1.65;
                    color: #24292e;
                }
                .diff-container .diff-line {
                    white-space: pre;
                    display: block;
                    padding: 1px 0;
                }
                .diff-container .diff-add {
                    background: #e6ffec;
                    color: #22863a;
                }
                .diff-container .diff-del {
                    background: #ffebe9;
                    color: #cb2431;
                }
                .diff-container .diff-hunk {
                    color: #6f42c1;
                    font-style: italic;
                }
                .diff-container .diff-header {
                    color: #005cc5;
                    font-weight: bold;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )
        
        # Initialize session state
        if 'target_directory' not in st.session_state:
            st.session_state.target_directory = None
        if 'results_ready' not in st.session_state:
            st.session_state.results_ready = False
        
        st.title("🔧 RefactorCrew: Autonomous Code Refactoring & Documentation Agent")
        
        # Show system status with mock warning
        with st.expander("🔧 System Status"):
            st.write(f"✅ Streamlit: Working")
            st.write(f"{'✅' if GIT_AVAILABLE else '❌'} Git Support: {'Available' if GIT_AVAILABLE else 'Not Available'}")
            if USING_MOCK:
                st.write(f"⚠️ Refactor Crew: Using Mock Version (Real crew not found)")
                st.warning("The actual RefactorCrew module was not found. Using mock implementation for UI testing.")
            else:
                st.write(f"✅ Refactor Crew: Available")
            st.write(f"📁 Current Directory: {os.getcwd()}")
        
        st.markdown("---")
        
        # Sidebar for configuration
        with st.sidebar:
            st.header("Configuration")
            
            # LLM Configuration
            st.subheader("LLM Settings")
            llm_provider = st.selectbox(
                "LLM Provider",
                ["Ollama (Local)", "OpenAI", "Anthropic"],
                index=0
            )
            
            if llm_provider == "Ollama (Local)":
                model_name = st.text_input("Model Name", value="deepseek-r1:1.5b")
                ollama_url = st.text_input("Ollama URL", value="http://localhost:11434")
            
            st.markdown("---")
            
            # Operation Mode
            st.subheader("Operation Mode")
            mode = st.radio(
                "Select Mode",
                ["Analysis Only", "Full Refactoring"],
                help="Analysis Only: Just analyze code without making changes. Full Refactoring: Analyze and automatically refactor."
            )
            
            # Safety Settings
            st.subheader("Safety Settings")
            create_backup = st.checkbox("Create Backup Before Changes", value=True)
            max_complexity = st.slider("Max Complexity Threshold", 1, 30, 10)
        
        # Main interface
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.header("Input Source")
            
            # Modify input methods based on available dependencies
            input_methods = ["Upload Zip File", "Local Directory Path"]
            if GIT_AVAILABLE:
                input_methods.insert(1, "Clone Git Repository")
            
            input_method = st.radio("Choose Input Method", input_methods)
            
            target_directory = None
            
            if input_method == "Upload Zip File":
                uploaded_file = st.file_uploader(
                    "Upload Python Project (ZIP)", 
                    type=['zip'],
                    help="Upload a zip file containing your Python project"
                )
                
                if uploaded_file:
                    if st.button("Extract and Prepare"):
                        try:
                            # Create temp directory and extract
                            temp_dir = tempfile.mkdtemp()
                            zip_path = os.path.join(temp_dir, "project.zip")
                            
                            with open(zip_path, "wb") as f:
                                f.write(uploaded_file.getbuffer())
                            
                            extract_dir = os.path.join(temp_dir, "extracted")
                            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                                zip_ref.extractall(extract_dir)
                            
                            st.session_state.target_directory = extract_dir
                            st.success(f"Project extracted to: {extract_dir}")
                        except Exception as e:
                            st.error(f"Failed to extract zip file: {str(e)}")
            
            elif input_method == "Clone Git Repository" and GIT_AVAILABLE:
                repo_url = st.text_input(
                    "Git Repository URL",
                    placeholder="https://github.com/username/repository.git"
                )
                
                if repo_url and st.button("Clone Repository"):
                    try:
                        temp_dir = tempfile.mkdtemp()
                        clone_dir = os.path.join(temp_dir, "cloned_repo")
                        
                        with st.spinner("Cloning repository..."):
                            git.Repo.clone_from(repo_url, clone_dir)
                        
                        st.session_state.target_directory = clone_dir
                        st.success(f"Repository cloned to: {clone_dir}")
                        
                    except Exception as e:
                        st.error(f"Failed to clone repository: {str(e)}")
            
            elif input_method == "Local Directory Path":
                dir_path = st.text_input(
                    "Local Directory Path",
                    placeholder="C:/path/to/your/python/project"
                )
                
                if dir_path:
                    if os.path.exists(dir_path):
                        st.session_state.target_directory = dir_path
                        st.success(f"Using directory: {dir_path}")
                    else:
                        st.error("Directory not found!")
        
        with col2:
            st.header("Project Overview")
            
            target_directory = st.session_state.target_directory
            
            if target_directory and os.path.exists(target_directory):
                # Show project structure
                st.subheader("Python Files Found")
                python_files = []
                try:
                    for root, dirs, files in os.walk(target_directory):
                        for file in files:
                            if file.endswith('.py'):
                                python_files.append(os.path.join(root, file))
                    
                    if python_files:
                        st.write(f"Found {len(python_files)} Python files:")
                        for i, file_path in enumerate(python_files[:10], 1):  # Show first 10
                            relative_path = os.path.relpath(file_path, target_directory)
                            st.write(f"{i}. {relative_path}")
                        
                        if len(python_files) > 10:
                            st.write(f"... and {len(python_files) - 10} more files")
                    else:
                        st.warning("No Python files found in the directory!")
                except Exception as e:
                    st.error(f"Error scanning directory: {str(e)}")
            else:
                st.info("Please select and prepare a Python project to see the overview.")
        
        # Action buttons
        st.markdown("---")
        st.header("Actions")
        
        # NOTE: we no longer block when CREW_AVAILABLE is False,
        # because RefactorCrew is now implemented and imported directly.
        # If import fails, you'll see an error at the top instead of a disabled UI.

        col3, col4, col5 = st.columns(3)
        
        target_dir = st.session_state.target_directory
        
        # Capture button clicks inside columns but DO NOT render
        # results here – columns constrain output to 1/3 width.
        with col3:
            run_analysis_clicked = st.button("🔍 Run Analysis", disabled=not target_dir)
        
        with col4:
            run_refactor_clicked = st.button("🔧 Start Refactoring", disabled=not target_dir)
        
        with col5:
            download_clicked = st.button("📥 Download Results", disabled=not st.session_state.results_ready)
        
        # ── Render results at FULL page width (outside columns) ──
        if run_analysis_clicked and target_dir:
            run_analysis(target_dir, mode, create_backup)
        
        if run_refactor_clicked and target_dir:
            run_refactoring(target_dir, create_backup)
        
        if download_clicked and target_dir:
            create_download_package(target_dir)

    except Exception as e:
        st.error(f"Application error: {str(e)}")
        st.error("Please check the console for more details.")
        st.exception(e)

def run_analysis(target_directory: str, mode: str, create_backup: bool):
    """Run the analysis workflow"""
    st.header("🔍 Code Analysis Results")
    
    if USING_MOCK:
        st.info("🧪 Running in mock mode - This is a demonstration of the UI functionality.")
    
    with st.spinner("Analyzing codebase..."):
        try:
            crew = RefactorCrew()
            
            # Use the correct method - kickoff with inputs
            inputs = {
                'target_directory': target_directory,
                'mode': 'analysis'
            }
            result = crew.kickoff(inputs=inputs)
            
            st.success("✅ Analysis completed successfully!")
            
            # Store results for download
            st.session_state.analysis_result = result
            st.session_state.results_ready = True
            
            # Display analysis results
            st.subheader("📊 Analysis Results")
            
            # Handle both mock and real results
            if isinstance(result, dict):
                # Mock result format
                display_structured_results(result)
            else:
                # Original result format
                result_text = str(result)
                with st.expander("📋 Raw Analysis Output", expanded=True):
                    st.text_area("Analysis Output", result_text, height=400)
                
                try:
                    json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
                    if json_match:
                        json_data = json.loads(json_match.group())
                        display_analysis_results(json_data)
                    elif hasattr(result, 'raw'):
                        display_analysis_results(result.raw)
                except Exception as e:
                    st.info("Structured analysis view not available. See raw output above.")
                
        except Exception as e:
            st.error(f"❌ Analysis failed: {str(e)}")
            with st.expander("🔍 Error Details"):
                st.exception(e)

def display_structured_results(result_data):
    """Display structured results from mock or real crew"""
    
    # Create tabs for different aspects
    tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Code Quality", "Complexity", "Documentation"])
    
    with tab1:
        st.markdown("### Analysis Overview")
        st.write(f"**Status:** {result_data.get('status', 'Unknown')}")
        st.write(f"**Mode:** {result_data.get('mode', 'Unknown')}")
        st.write(f"**Summary:** {result_data.get('summary', 'No summary available')}")
        
        if 'recommendations' in result_data:
            st.markdown("### Recommendations")
            for rec in result_data['recommendations']:
                st.write(f"• {rec}")
    
    with tab2:
        st.markdown("### Code Quality Issues")
        findings = result_data.get('findings', {})
        quality_issues = findings.get('code_quality_issues', [])
        
        if quality_issues:
            for issue in quality_issues:
                st.write(f"❗ {issue}")
        else:
            st.info("No specific code quality issues found or data not available.")
    
    with tab3:
        st.markdown("### Complexity Metrics")
        complexity = result_data.get('findings', {}).get('complexity_metrics', {})
        
        if complexity:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Average Complexity", complexity.get('average_complexity', 'N/A'))
            with col2:
                st.metric("High Complexity Functions", complexity.get('high_complexity_functions', 'N/A'))
            with col3:
                st.metric("Total Functions", complexity.get('total_functions_analyzed', 'N/A'))
        else:
            st.info("Complexity metrics not available.")
    
    with tab4:
        st.markdown("### Documentation Coverage")
        documentation = result_data.get('findings', {}).get('documentation_coverage', {})
        
        if documentation:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Functions with Docstrings", documentation.get('functions_with_docstrings', 'N/A'))
            with col2:
                st.metric("Classes with Docstrings", documentation.get('classes_with_docstrings', 'N/A'))
            with col3:
                st.metric("Modules with Docstrings", documentation.get('modules_with_docstrings', 'N/A'))
        else:
            st.info("Documentation coverage data not available.")

def render_diff_html(diff_text: str) -> str:
    """Convert a unified diff string to syntax-highlighted HTML."""
    import html as _html
    lines_html = []
    for line in diff_text.splitlines():
        escaped = _html.escape(line)
        if line.startswith('@@'):
            lines_html.append(f'<span class="diff-line diff-hunk">{escaped}</span>')
        elif line.startswith('---') or line.startswith('+++'):
            lines_html.append(f'<span class="diff-line diff-header">{escaped}</span>')
        elif line.startswith('+'):
            lines_html.append(f'<span class="diff-line diff-add">{escaped}</span>')
        elif line.startswith('-'):
            lines_html.append(f'<span class="diff-line diff-del">{escaped}</span>')
        else:
            lines_html.append(f'<span class="diff-line">{escaped}</span>')
    return '<div class="diff-container">' + '\n'.join(lines_html) + '</div>'


def run_refactoring(target_directory: str, create_backup: bool):
    """Run the full refactoring workflow"""
    st.header("🔧 Refactoring Process")
    
    if USING_MOCK:
        st.info("🧪 Running in mock mode - No actual changes will be made to your files.")
    
    if create_backup:
        with st.spinner("Creating backup..."):
            backup_dir = target_directory + "_backup_" + str(int(time.time()))
            try:
                if os.path.exists(backup_dir):
                    shutil.rmtree(backup_dir)
                shutil.copytree(target_directory, backup_dir)
                st.success(f"✅ Backup created at: {backup_dir}")
            except Exception as e:
                st.error(f"❌ Backup failed: {str(e)}")
                return
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        crew = RefactorCrew()
        
        # Update progress
        progress_bar.progress(25)
        status_text.text("🔍 Analyzing code...")
        
        # Safe isolation path
        work_dir = target_directory.rstrip('/') + "_refactored"
        if os.path.exists(work_dir):
            shutil.rmtree(work_dir)
        shutil.copytree(target_directory, work_dir)

        inputs = {
            'target_directory': work_dir,
            'mode': 'refactor'
        }
        
        progress_bar.progress(50)
        status_text.text("🔧 Applying refactoring...")
        
        result = crew.kickoff(inputs=inputs)
        
        progress_bar.progress(100)
        status_text.text("✅ Refactoring completed!")
        
        st.success(f"🎉 Refactoring completed safely in isolated directory: {work_dir}")

        # Store results
        st.session_state.refactor_result = result
        st.session_state.results_ready = True
        
        # Display results
        st.subheader("Refactoring Summary")
        
        if isinstance(result, dict):
            # Mock result format
            if 'changes_applied' in result:
                st.markdown("### Changes Applied:")
                if result['changes_applied']:
                    for change in result['changes_applied']:
                        st.write(f"✅ {change}")
                else:
                    st.info("No changes were needed.")
            
            if 'files_modified' in result:
                st.markdown("### Files Modified:")
                if result['files_modified']:
                    for file in result['files_modified']:
                        st.write(f"📝 {file}")
                else:
                    st.info("No files were modified.")

            if 'file_diffs' in result and result['file_diffs']:
                st.markdown("### Code Changes:")
                for file, diff in result['file_diffs'].items():
                    with st.expander(f"View changes for {file}"):
                        st.markdown(render_diff_html(diff), unsafe_allow_html=True)
        else:
            # Original format
            with st.expander("📋 Refactoring Details", expanded=True):
                st.text_area("Results", str(result), height=400)
        
        st.info("✅ Refactoring complete! You can now download the results.")
            
    except Exception as e:
        st.error(f"❌ Refactoring failed: {str(e)}")
        with st.expander("🔍 Error Details"):
            st.exception(e)

def display_analysis_results(analysis_data):
    """Display formatted analysis results"""
    st.subheader("📊 Analysis Summary")
    
    # Create tabs for different aspects
    tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Code Quality", "Complexity", "Documentation"])
    
    with tab1:
        st.markdown("### Overall Health Score")
        # This would be calculated based on various metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Quality Score", "B+", "Based on analysis")
        with col2:
            st.metric("Issues Found", "Multiple", "See details")
        with col3:
            st.metric("Files Analyzed", "Several", "Python files")
    
    with tab2:
        st.markdown("### Code Quality Issues")
        if isinstance(analysis_data, dict):
            # Display structured data
            st.json(analysis_data)
        elif isinstance(analysis_data, str):
            # Try to parse as JSON
            try:
                parsed = json.loads(analysis_data)
                st.json(parsed)
            except:
                st.text(analysis_data)
        else:
            st.text(str(analysis_data))
    
    with tab3:
        st.markdown("### Complexity Metrics")
        st.info("Complexity analysis details would be extracted from the analysis results")
        if isinstance(analysis_data, (dict, str)):
            # Look for complexity-related information
            analysis_str = str(analysis_data)
            if "complexity" in analysis_str.lower():
                complexity_lines = [line for line in analysis_str.split('\n') if 'complexity' in line.lower()]
                for line in complexity_lines:
                    st.write(f"• {line}")
    
    with tab4:
        st.markdown("### Documentation Coverage")
        st.info("Documentation analysis details would be extracted from the analysis results")
        if isinstance(analysis_data, (dict, str)):
            # Look for documentation-related information
            analysis_str = str(analysis_data)
            if "docstring" in analysis_str.lower() or "documentation" in analysis_str.lower():
                doc_lines = [line for line in analysis_str.split('\n') 
                           if any(keyword in line.lower() for keyword in ['docstring', 'documentation', 'comment'])]
                for line in doc_lines:
                    st.write(f"• {line}")

def create_download_package(target_directory: str):
    """Create a downloadable package of the refactored code"""
    st.subheader("📥 Download Refactored Code")
    
    try:
        # Create zip file
        zip_buffer = BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for root, dirs, files in os.walk(target_directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, target_directory)
                    zip_file.write(file_path, arcname)
        
        zip_buffer.seek(0)
        
        st.download_button(
            label="📥 Download Refactored Project",
            data=zip_buffer.getvalue(),
            file_name=f"refactored_project_{int(time.time())}.zip",
            mime="application/zip",
            help="Download the complete refactored project as a ZIP file"
        )
        
        st.success("✅ Download package ready!")
        
    except Exception as e:
        st.error(f"❌ Failed to create download package: {str(e)}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"Failed to start application: {str(e)}")
        st.exception(e)