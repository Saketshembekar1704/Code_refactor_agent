# tools/file_operations.py
import os
import shutil
import json
import re
from typing import Dict, List
from crewai.tools import tool

@tool("File Modification Tool")
def modify_file(operation: str, file_path: str, **kwargs) -> str:
    """
    Performs precise file modifications including renaming variables, extracting functions, and adding docstrings.
    
    Args:
        operation: Type of operation (rename_variable, extract_function, add_docstring, replace_line, add_import, backup_file)
        file_path: Path to the file to modify
        **kwargs: Additional parameters specific to each operation
        
    Returns:
        JSON string with operation result
    """
    try:
        if not os.path.exists(file_path):
            return json.dumps({"error": f"File not found: {file_path}", "success": False})

        if operation == "rename_variable":
            return _rename_variable(file_path, kwargs.get("old_name"), kwargs.get("new_name"))
        
        elif operation == "extract_function":
            return _extract_function(file_path, kwargs.get("start_line"), kwargs.get("end_line"), kwargs.get("function_name"))
        
        elif operation == "add_docstring":
            return _add_docstring(file_path, kwargs.get("function_name"), kwargs.get("docstring"))
        
        elif operation == "replace_line":
            return _replace_line(file_path, kwargs.get("line_number"), kwargs.get("new_content"))
        
        elif operation == "add_import":
            return _add_import(file_path, kwargs.get("import_statement"))
        
        elif operation == "backup_file":
            return _backup_file(file_path)
        
        else:
            return json.dumps({"error": f"Unknown operation: {operation}", "success": False})

    except Exception as e:
        return json.dumps({"error": f"File modification failed: {str(e)}", "success": False})

def _rename_variable(file_path: str, old_name: str, new_name: str) -> str:
    """Rename a variable throughout the file"""
    if not old_name or not new_name:
        return json.dumps({"error": "Both old_name and new_name are required", "success": False})

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Use word boundaries to avoid partial matches
    pattern = r'\b' + re.escape(old_name) + r'\b'
    new_content = re.sub(pattern, new_name, content)
    
    changes_made = content != new_content
    
    if changes_made:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

    return json.dumps({
        "success": True,
        "changes_made": changes_made,
        "operation": f"Renamed '{old_name}' to '{new_name}'"
    })

def _extract_function(file_path: str, start_line: int, end_line: int, function_name: str) -> str:
    """Extract code block into a new function"""
    if not all([start_line, end_line, function_name]):
        return json.dumps({"error": "start_line, end_line, and function_name are required", "success": False})

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    if start_line < 1 or end_line > len(lines) or start_line > end_line:
        return json.dumps({"error": "Invalid line range", "success": False})

    # Extract the code block
    extracted_lines = lines[start_line-1:end_line]
    extracted_code = ''.join(extracted_lines)
    
    # Determine indentation
    base_indent = len(extracted_lines[0]) - len(extracted_lines[0].lstrip())
    
    # Create function definition
    function_def = f"def {function_name}():\n"
    function_body = ""
    for line in extracted_lines:
        if line.strip():  # Skip empty lines
            # Adjust indentation
            current_indent = len(line) - len(line.lstrip())
            new_indent = current_indent - base_indent + 4
            function_body += " " * new_indent + line.lstrip()
        else:
            function_body += line

    # Add return statement if needed
    if not any(line.strip().startswith('return') for line in extracted_lines):
        function_body += "    pass\n"

    new_function = function_def + function_body + "\n"
    
    # Replace extracted code with function call
    function_call = " " * base_indent + f"{function_name}()\n"
    
    # Reconstruct file
    new_lines = (lines[:start_line-1] + 
                [function_call] + 
                lines[end_line:] + 
                ["\n", new_function])

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    return json.dumps({
        "success": True,
        "operation": f"Extracted function '{function_name}' from lines {start_line}-{end_line}"
    })

def _add_docstring(file_path: str, function_name: str, docstring: str) -> str:
    """Add docstring to a function"""
    if not function_name or not docstring:
        return json.dumps({"error": "Both function_name and docstring are required", "success": False})

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    function_found = False
    insert_line = -1
    
    for i, line in enumerate(lines):
        # Look for function definition
        if line.strip().startswith(f"def {function_name}(") or line.strip().startswith(f"async def {function_name}("):
            function_found = True
            # Find the line after the function definition (after the colon)
            j = i
            while j < len(lines) and ':' not in lines[j]:
                j += 1
            insert_line = j + 1
            break

    if not function_found:
        return json.dumps({"error": f"Function '{function_name}' not found", "success": False})

    # Check if docstring already exists
    if insert_line < len(lines):
        next_line = lines[insert_line].strip()
        if next_line.startswith('"""') or next_line.startswith("'''"):
            return json.dumps({"error": f"Function '{function_name}' already has a docstring", "success": False})

    # Determine indentation
    func_line = lines[insert_line - 1] if insert_line > 0 else lines[0]
    base_indent = len(func_line) - len(func_line.lstrip()) + 4

    # Format docstring
    docstring_lines = []
    docstring_lines.append(" " * base_indent + '"""' + docstring + '"""\n')

    # Insert docstring
    lines.insert(insert_line, docstring_lines[0])

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    return json.dumps({
        "success": True,
        "operation": f"Added docstring to function '{function_name}'"
    })

def _replace_line(file_path: str, line_number: int, new_content: str) -> str:
    """Replace a specific line in the file"""
    if not line_number or new_content is None:
        return json.dumps({"error": "line_number and new_content are required", "success": False})

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    if line_number < 1 or line_number > len(lines):
        return json.dumps({"error": f"Line number {line_number} is out of range", "success": False})

    old_content = lines[line_number - 1].rstrip()
    lines[line_number - 1] = new_content + '\n'

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    return json.dumps({
        "success": True,
        "operation": f"Replaced line {line_number}",
        "old_content": old_content,
        "new_content": new_content
    })

def _add_import(file_path: str, import_statement: str) -> str:
    """Add an import statement to the file"""
    if not import_statement:
        return json.dumps({"error": "import_statement is required", "success": False})

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Check if import already exists
    if any(import_statement.strip() in line for line in lines):
        return json.dumps({"success": True, "operation": "Import already exists", "changes_made": False})

    # Find the right place to insert the import
    insert_line = 0
    
    # Skip shebang and encoding declarations
    for i, line in enumerate(lines):
        if line.startswith('#') and ('coding' in line or 'encoding' in line or line.startswith('#!')):
            insert_line = i + 1
        elif line.strip() == '':
            continue
        elif line.startswith('import ') or line.startswith('from '):
            # Insert after existing imports
            insert_line = i + 1
        else:
            break

    # Insert the import
    lines.insert(insert_line, import_statement + '\n')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    return json.dumps({
        "success": True,
        "operation": f"Added import: {import_statement}",
        "changes_made": True
    })

def _backup_file(file_path: str) -> str:
    """Create a backup of the file"""
    backup_path = file_path + '.backup'
    try:
        shutil.copy2(file_path, backup_path)
        return json.dumps({
            "success": True,
            "backup_path": backup_path,
            "operation": "File backed up successfully"
        })
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"Backup failed: {str(e)}"
        })
    name: str = "File Modification Tool"
    description: str = "Performs precise file modifications including renaming variables, extracting functions, and adding docstrings"

    def _run(self, operation: str, file_path: str, **kwargs) -> str:
        """Perform file modification operations"""
        try:
            if not os.path.exists(file_path):
                return json.dumps({"error": f"File not found: {file_path}", "success": False})

            if operation == "rename_variable":
                return self._rename_variable(file_path, kwargs.get("old_name"), kwargs.get("new_name"))
            
            elif operation == "extract_function":
                return self._extract_function(file_path, kwargs.get("start_line"), kwargs.get("end_line"), kwargs.get("function_name"))
            
            elif operation == "add_docstring":
                return self._add_docstring(file_path, kwargs.get("function_name"), kwargs.get("docstring"))
            
            elif operation == "replace_line":
                return self._replace_line(file_path, kwargs.get("line_number"), kwargs.get("new_content"))
            
            elif operation == "add_import":
                return self._add_import(file_path, kwargs.get("import_statement"))
            
            elif operation == "backup_file":
                return self._backup_file(file_path)
            
            else:
                return json.dumps({"error": f"Unknown operation: {operation}", "success": False})

        except Exception as e:
            return json.dumps({"error": f"File modification failed: {str(e)}", "success": False})

    def _rename_variable(self, file_path: str, old_name: str, new_name: str) -> str:
        """Rename a variable throughout the file"""
        if not old_name or not new_name:
            return json.dumps({"error": "Both old_name and new_name are required", "success": False})

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Use word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(old_name) + r'\b'
        new_content = re.sub(pattern, new_name, content)
        
        changes_made = content != new_content
        
        if changes_made:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

        return json.dumps({
            "success": True,
            "changes_made": changes_made,
            "operation": f"Renamed '{old_name}' to '{new_name}'"
        })

    def _extract_function(self, file_path: str, start_line: int, end_line: int, function_name: str) -> str:
        """Extract code block into a new function"""
        if not all([start_line, end_line, function_name]):
            return json.dumps({"error": "start_line, end_line, and function_name are required", "success": False})

        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        if start_line < 1 or end_line > len(lines) or start_line > end_line:
            return json.dumps({"error": "Invalid line range", "success": False})

        # Extract the code block
        extracted_lines = lines[start_line-1:end_line]
        extracted_code = ''.join(extracted_lines)
        
        # Determine indentation
        base_indent = len(extracted_lines[0]) - len(extracted_lines[0].lstrip())
        
        # Create function definition
        function_def = f"def {function_name}():\n"
        function_body = ""
        for line in extracted_lines:
            if line.strip():  # Skip empty lines
                # Adjust indentation
                current_indent = len(line) - len(line.lstrip())
                new_indent = current_indent - base_indent + 4
                function_body += " " * new_indent + line.lstrip()
            else:
                function_body += line

        # Add return statement if needed
        if not any(line.strip().startswith('return') for line in extracted_lines):
            function_body += "    pass\n"

        new_function = function_def + function_body + "\n"
        
        # Replace extracted code with function call
        function_call = " " * base_indent + f"{function_name}()\n"
        
        # Reconstruct file
        new_lines = (lines[:start_line-1] + 
                    [function_call] + 
                    lines[end_line:] + 
                    ["\n", new_function])

        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

        return json.dumps({
            "success": True,
            "operation": f"Extracted function '{function_name}' from lines {start_line}-{end_line}"
        })

    def _add_docstring(self, file_path: str, function_name: str, docstring: str) -> str:
        """Add docstring to a function"""
        if not function_name or not docstring:
            return json.dumps({"error": "Both function_name and docstring are required", "success": False})

        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        function_found = False
        insert_line = -1
        
        for i, line in enumerate(lines):
            # Look for function definition
            if line.strip().startswith(f"def {function_name}(") or line.strip().startswith(f"async def {function_name}("):
                function_found = True
                # Find the line after the function definition (after the colon)
                j = i
                while j < len(lines) and ':' not in lines[j]:
                    j += 1
                insert_line = j + 1
                break

        if not function_found:
            return json.dumps({"error": f"Function '{function_name}' not found", "success": False})

        # Check if docstring already exists
        if insert_line < len(lines):
            next_line = lines[insert_line].strip()
            if next_line.startswith('"""') or next_line.startswith("'''"):
                return json.dumps({"error": f"Function '{function_name}' already has a docstring", "success": False})

        # Determine indentation
        func_line = lines[insert_line - 1] if insert_line > 0 else lines[0]
        base_indent = len(func_line) - len(func_line.lstrip()) + 4

        # Format docstring
        docstring_lines = []
        docstring_lines.append(" " * base_indent + '"""' + docstring + '"""\n')

        # Insert docstring
        lines.insert(insert_line, docstring_lines[0])

        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)

        return json.dumps({
            "success": True,
            "operation": f"Added docstring to function '{function_name}'"
        })

    def _replace_line(self, file_path: str, line_number: int, new_content: str) -> str:
        """Replace a specific line in the file"""
        if not line_number or new_content is None:
            return json.dumps({"error": "line_number and new_content are required", "success": False})

        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        if line_number < 1 or line_number > len(lines):
            return json.dumps({"error": f"Line number {line_number} is out of range", "success": False})

        old_content = lines[line_number - 1].rstrip()
        lines[line_number - 1] = new_content + '\n'

        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)

        return json.dumps({
            "success": True,
            "operation": f"Replaced line {line_number}",
            "old_content": old_content,
            "new_content": new_content
        })

    def _add_import(self, file_path: str, import_statement: str) -> str:
        """Add an import statement to the file"""
        if not import_statement:
            return json.dumps({"error": "import_statement is required", "success": False})

        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Check if import already exists
        if any(import_statement.strip() in line for line in lines):
            return json.dumps({"success": True, "operation": "Import already exists", "changes_made": False})

        # Find the right place to insert the import
        insert_line = 0
        
        # Skip shebang and encoding declarations
        for i, line in enumerate(lines):
            if line.startswith('#') and ('coding' in line or 'encoding' in line or line.startswith('#!')):
                insert_line = i + 1
            elif line.strip() == '':
                continue
            elif line.startswith('import ') or line.startswith('from '):
                # Insert after existing imports
                insert_line = i + 1
            else:
                break

        # Insert the import
        lines.insert(insert_line, import_statement + '\n')

        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)

        return json.dumps({
            "success": True,
            "operation": f"Added import: {import_statement}",
            "changes_made": True
        })

    def _backup_file(self, file_path: str) -> str:
        """Create a backup of the file"""
        backup_path = file_path + '.backup'
        try:
            shutil.copy2(file_path, backup_path)
            return json.dumps({
                "success": True,
                "backup_path": backup_path,
                "operation": "File backed up successfully"
            })
        except Exception as e:
            return json.dumps({
                "success": False,
                "error": f"Backup failed: {str(e)}"
            })