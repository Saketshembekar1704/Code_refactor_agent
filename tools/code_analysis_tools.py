# tools/code_analysis_tools.py
import os
import ast
import json
from typing import Dict, List, Any
from pylint import epylint as lint
from radon.complexity import cc_visit
from radon.metrics import mi_visit
from crewai.tools import tool
from crewai.tools import BaseTool


@tool("Code Analysis Tool")
def analyze_code(file_path: str) -> str:
    """
    Analyzes Python code for quality issues, complexity, and maintainability.
    
    Args:
        file_path: Path to the Python file to analyze
        
    Returns:
        JSON string containing detailed analysis report
    """
    if not os.path.exists(file_path):
        return json.dumps({"error": f"File not found: {file_path}"})
    
    try:
        analysis_report = {
            "file_path": file_path,
            "pylint_issues": _get_pylint_issues(file_path),
            "complexity_metrics": _get_complexity_metrics(file_path),
            "maintainability_index": _get_maintainability_index(file_path),
            "undocumented_functions": _get_undocumented_functions(file_path),
            "code_smells": _detect_code_smells(file_path)
        }
        return json.dumps(analysis_report, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Analysis failed: {str(e)}"})

def _get_pylint_issues(file_path: str) -> List[Dict]:
    """Get pylint issues for the file"""
    try:
        (pylint_stdout, pylint_stderr) = lint.py_run(f'{file_path} --output-format=json', return_std=True)
        issues = json.loads(pylint_stdout.getvalue())
        
        formatted_issues = []
        for issue in issues:
            formatted_issues.append({
                "type": issue.get("type", "unknown"),
                "message": issue.get("message", ""),
                "line": issue.get("line", 0),
                "column": issue.get("column", 0),
                "symbol": issue.get("symbol", ""),
                "severity": _map_pylint_severity(issue.get("type", ""))
            })
        return formatted_issues
    except Exception:
        return []

def _get_complexity_metrics(file_path: str) -> List[Dict]:
    """Get cyclomatic complexity metrics"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        complexity_data = cc_visit(code)
        metrics = []
        
        for item in complexity_data:
            metrics.append({
                "name": item.name,
                "type": item.classname or "function",
                "complexity": item.complexity,
                "line": item.lineno,
                "complexity_grade": _get_complexity_grade(item.complexity)
            })
        return metrics
    except Exception:
        return []

def _get_maintainability_index(file_path: str) -> Dict:
    """Calculate maintainability index"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        mi_data = mi_visit(code, multi=True)
        return {
            "maintainability_index": round(mi_data, 2),
            "grade": _get_maintainability_grade(mi_data)
        }
    except Exception:
        return {"maintainability_index": 0, "grade": "Unknown"}

def _get_undocumented_functions(file_path: str) -> List[Dict]:
    """Find functions and classes without docstrings"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        tree = ast.parse(code)
        undocumented = []
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                if not ast.get_docstring(node):
                    undocumented.append({
                        "name": node.name,
                        "type": "class" if isinstance(node, ast.ClassDef) else "function",
                        "line": node.lineno,
                        "args": [arg.arg for arg in node.args.args] if hasattr(node, 'args') else []
                    })
        return undocumented
    except Exception:
        return []

def _detect_code_smells(file_path: str) -> List[Dict]:
    """Detect common code smells"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        smells = []
        
        for i, line in enumerate(lines, 1):
            # Long lines
            if len(line.strip()) > 100:
                smells.append({
                    "type": "long_line",
                    "line": i,
                    "description": f"Line too long ({len(line.strip())} characters)",
                    "severity": "minor"
                })
            
            # Magic numbers
            if any(char.isdigit() and not line.strip().startswith('#') for char in line):
                import re
                numbers = re.findall(r'\b\d+\b', line)
                for num in numbers:
                    if int(num) > 1 and int(num) not in [24, 60, 365]:  # Common acceptable numbers
                        smells.append({
                            "type": "magic_number",
                            "line": i,
                            "description": f"Magic number found: {num}",
                            "severity": "minor"
                        })
                        break
            
            # TODO comments
            if 'TODO' in line.upper() or 'FIXME' in line.upper():
                smells.append({
                    "type": "todo_comment",
                    "line": i,
                    "description": "TODO/FIXME comment found",
                    "severity": "info"
                })
        
        return smells
    except Exception:
        return []

def _map_pylint_severity(pylint_type: str) -> str:
    """Map pylint message types to severity levels"""
    mapping = {
        "error": "high",
        "warning": "medium", 
        "refactor": "low",
        "convention": "low",
        "info": "info"
    }
    return mapping.get(pylint_type, "unknown")

def _get_complexity_grade(complexity: int) -> str:
    """Get complexity grade based on cyclomatic complexity"""
    if complexity <= 5:
        return "A (Low)"
    elif complexity <= 10:
        return "B (Moderate)"
    elif complexity <= 20:
        return "C (High)"
    elif complexity <= 30:
        return "D (Very High)"
    else:
        return "F (Extremely High)"

def _get_maintainability_grade(mi: float) -> str:
    """Get maintainability grade based on maintainability index"""
    if mi >= 85:
        return "A (Excellent)"
    elif mi >= 70:
        return "B (Good)"
    elif mi >= 50:
        return "C (Fair)"
    elif mi >= 25:
        return "D (Poor)"
    else:
        return "F (Very Poor)"


@tool("File System Tool")
def read_file_system(path: str, operation: str = "read") -> str:
    """
    Reads and lists files in a directory structure.
    
    Args:
        path: File or directory path
        operation: Operation type - 'read', 'list', or 'exists'
        
    Returns:
        File content or directory listing as string
    """
    try:
        if operation == "read":
            if os.path.isfile(path):
                with open(path, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                return json.dumps({"error": f"File not found: {path}"})
        
        elif operation == "list":
            if os.path.isdir(path):
                files = []
                for root, dirs, filenames in os.walk(path):
                    for filename in filenames:
                        if filename.endswith('.py'):
                            files.append(os.path.join(root, filename))
                return json.dumps({"python_files": files})
            else:
                return json.dumps({"error": f"Directory not found: {path}"})
        
        elif operation == "exists":
            return json.dumps({"exists": os.path.exists(path)})
        
        else:
            return json.dumps({"error": f"Unknown operation: {operation}"})
            
    except Exception as e:
        return json.dumps({"error": f"File operation failed: {str(e)}"})
    name: str = "Code Analysis Tool"
    description: str = "Analyzes Python code for quality issues, complexity, and maintainability"

    def _run(self, file_path: str) -> str:
        """Analyze a Python file and return detailed analysis report"""
        if not os.path.exists(file_path):
            return json.dumps({"error": f"File not found: {file_path}"})
        
        try:
            analysis_report = {
                "file_path": file_path,
                "pylint_issues": self._get_pylint_issues(file_path),
                "complexity_metrics": self._get_complexity_metrics(file_path),
                "maintainability_index": self._get_maintainability_index(file_path),
                "undocumented_functions": self._get_undocumented_functions(file_path),
                "code_smells": self._detect_code_smells(file_path)
            }
            return json.dumps(analysis_report, indent=2)
        except Exception as e:
            return json.dumps({"error": f"Analysis failed: {str(e)}"})

    def _get_pylint_issues(self, file_path: str) -> List[Dict]:
        """Get pylint issues for the file"""
        try:
            (pylint_stdout, pylint_stderr) = lint.py_run(f'{file_path} --output-format=json', return_std=True)
            issues = json.loads(pylint_stdout.getvalue())
            
            formatted_issues = []
            for issue in issues:
                formatted_issues.append({
                    "type": issue.get("type", "unknown"),
                    "message": issue.get("message", ""),
                    "line": issue.get("line", 0),
                    "column": issue.get("column", 0),
                    "symbol": issue.get("symbol", ""),
                    "severity": self._map_pylint_severity(issue.get("type", ""))
                })
            return formatted_issues
        except Exception:
            return []

    def _get_complexity_metrics(self, file_path: str) -> List[Dict]:
        """Get cyclomatic complexity metrics"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            complexity_data = cc_visit(code)
            metrics = []
            
            for item in complexity_data:
                metrics.append({
                    "name": item.name,
                    "type": item.classname or "function",
                    "complexity": item.complexity,
                    "line": item.lineno,
                    "complexity_grade": self._get_complexity_grade(item.complexity)
                })
            return metrics
        except Exception:
            return []

    def _get_maintainability_index(self, file_path: str) -> Dict:
        """Calculate maintainability index"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            mi_data = mi_visit(code, multi=True)
            return {
                "maintainability_index": round(mi_data, 2),
                "grade": self._get_maintainability_grade(mi_data)
            }
        except Exception:
            return {"maintainability_index": 0, "grade": "Unknown"}

    def _get_undocumented_functions(self, file_path: str) -> List[Dict]:
        """Find functions and classes without docstrings"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            tree = ast.parse(code)
            undocumented = []
            
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    if not ast.get_docstring(node):
                        undocumented.append({
                            "name": node.name,
                            "type": "class" if isinstance(node, ast.ClassDef) else "function",
                            "line": node.lineno,
                            "args": [arg.arg for arg in node.args.args] if hasattr(node, 'args') else []
                        })
            return undocumented
        except Exception:
            return []

    def _detect_code_smells(self, file_path: str) -> List[Dict]:
        """Detect common code smells"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            smells = []
            
            for i, line in enumerate(lines, 1):
                # Long lines
                if len(line.strip()) > 100:
                    smells.append({
                        "type": "long_line",
                        "line": i,
                        "description": f"Line too long ({len(line.strip())} characters)",
                        "severity": "minor"
                    })
                
                # Magic numbers
                if any(char.isdigit() and not line.strip().startswith('#') for char in line):
                    import re
                    numbers = re.findall(r'\b\d+\b', line)
                    for num in numbers:
                        if int(num) > 1 and int(num) not in [24, 60, 365]:  # Common acceptable numbers
                            smells.append({
                                "type": "magic_number",
                                "line": i,
                                "description": f"Magic number found: {num}",
                                "severity": "minor"
                            })
                            break
                
                # TODO comments
                if 'TODO' in line.upper() or 'FIXME' in line.upper():
                    smells.append({
                        "type": "todo_comment",
                        "line": i,
                        "description": "TODO/FIXME comment found",
                        "severity": "info"
                    })
            
            return smells
        except Exception:
            return []

    def _map_pylint_severity(self, pylint_type: str) -> str:
        """Map pylint message types to severity levels"""
        mapping = {
            "error": "high",
            "warning": "medium", 
            "refactor": "low",
            "convention": "low",
            "info": "info"
        }
        return mapping.get(pylint_type, "unknown")

    def _get_complexity_grade(self, complexity: int) -> str:
        """Get complexity grade based on cyclomatic complexity"""
        if complexity <= 5:
            return "A (Low)"
        elif complexity <= 10:
            return "B (Moderate)"
        elif complexity <= 20:
            return "C (High)"
        elif complexity <= 30:
            return "D (Very High)"
        else:
            return "F (Extremely High)"

    def _get_maintainability_grade(self, mi: float) -> str:
        """Get maintainability grade based on maintainability index"""
        if mi >= 85:
            return "A (Excellent)"
        elif mi >= 70:
            return "B (Good)"
        elif mi >= 50:
            return "C (Fair)"
        elif mi >= 25:
            return "D (Poor)"
        else:
            return "F (Very Poor)"


class FileSystemTool(BaseTool):
    name: str = "File System Tool"
    description: str = "Reads and lists files in a directory structure"

    def _run(self, path: str, operation: str = "read") -> str:
        """Perform file system operations"""
        try:
            if operation == "read":
                if os.path.isfile(path):
                    with open(path, 'r', encoding='utf-8') as f:
                        return f.read()
                else:
                    return json.dumps({"error": f"File not found: {path}"})
            
            elif operation == "list":
                if os.path.isdir(path):
                    files = []
                    for root, dirs, filenames in os.walk(path):
                        for filename in filenames:
                            if filename.endswith('.py'):
                                files.append(os.path.join(root, filename))
                    return json.dumps({"python_files": files})
                else:
                    return json.dumps({"error": f"Directory not found: {path}"})
            
            elif operation == "exists":
                return json.dumps({"exists": os.path.exists(path)})
            
            else:
                return json.dumps({"error": f"Unknown operation: {operation}"})
                
        except Exception as e:
            return json.dumps({"error": f"File operation failed: {str(e)}"})