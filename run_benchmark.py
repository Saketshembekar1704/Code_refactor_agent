"""
Benchmark script for RefactorCrew experimental evaluation.
Measures real before/after metrics using Radon and AST analysis.
"""
import os
import sys
import ast
import json
import time
import shutil
import re

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crew.refactor_crew import RefactorCrew


def count_loc(filepath):
    """Count non-blank, non-comment lines of code."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    count = 0
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith('#'):
            count += 1
    return count, len(lines)


def count_functions_classes(filepath):
    """Count functions and classes in a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        code = f.read()
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return 0, 0, 0, 0
    
    funcs = 0
    classes = 0
    funcs_with_doc = 0
    classes_with_doc = 0
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            funcs += 1
            if ast.get_docstring(node):
                funcs_with_doc += 1
        elif isinstance(node, ast.ClassDef):
            classes += 1
            if ast.get_docstring(node):
                classes_with_doc += 1
    
    return funcs, classes, funcs_with_doc, classes_with_doc


def calculate_cyclomatic_complexity(filepath):
    """Calculate cyclomatic complexity using AST."""
    with open(filepath, 'r', encoding='utf-8') as f:
        code = f.read()
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return [], 0
    
    complexities = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            cc = 1
            for child in ast.walk(node):
                if isinstance(child, (ast.If, ast.While, ast.For)):
                    cc += 1
                elif isinstance(child, ast.ExceptHandler):
                    cc += 1
                elif isinstance(child, ast.BoolOp):
                    cc += len(child.values) - 1
            complexities.append({"name": node.name, "complexity": cc})
    
    avg_cc = sum(c["complexity"] for c in complexities) / len(complexities) if complexities else 0
    return complexities, round(avg_cc, 2)


def calculate_maintainability_index(filepath):
    """Estimate maintainability index (simplified Halstead-based formula)."""
    with open(filepath, 'r', encoding='utf-8') as f:
        code = f.read()
    
    lines = code.split('\n')
    loc = len([l for l in lines if l.strip() and not l.strip().startswith('#')])
    
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return 0
    
    # Count operators and operands (simplified Halstead)
    operators = 0
    operands = 0
    for node in ast.walk(tree):
        if isinstance(node, (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow,
                            ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
                            ast.And, ast.Or, ast.Not, ast.Assign, ast.AugAssign)):
            operators += 1
        elif isinstance(node, (ast.Name, ast.Constant)):
            operands += 1
    
    # Calculate average CC
    _, avg_cc = calculate_cyclomatic_complexity(filepath)
    
    # Simplified MI formula: MI = 171 - 5.2*ln(V) - 0.23*CC - 16.2*ln(LOC)
    import math
    volume = (operators + operands) * math.log2(max(operators + operands, 1)) if (operators + operands) > 0 else 1
    mi = 171 - 5.2 * math.log(max(volume, 1)) - 0.23 * avg_cc - 16.2 * math.log(max(loc, 1))
    mi = max(0, min(100, mi))
    return round(mi, 2)


def detect_code_smells(filepath):
    """Detect code smells."""
    with open(filepath, 'r', encoding='utf-8') as f:
        code = f.read()
    
    smells = {
        "duplicate_functions": 0,
        "poor_naming": 0,
        "missing_docstrings": 0,
        "long_methods": 0,
        "total": 0
    }
    
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return smells
    
    # Check for duplicate function bodies
    func_bodies = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            body_str = ast.dump(ast.Module(body=node.body, type_ignores=[]))
            if body_str in func_bodies:
                smells["duplicate_functions"] += 1
            else:
                func_bodies[body_str] = node.name
            
            # Check poor naming
            if len(node.name) <= 2 or not re.match(r'^[a-z_][a-z0-9_]*$', node.name):
                if not node.name.startswith('__'):
                    smells["poor_naming"] += 1
            
            for arg in node.args.args:
                if len(arg.arg) == 1 and arg.arg not in ('_', 'x', 'y', 'n', 'i', 'j', 'k'):
                    smells["poor_naming"] += 1
            
            # Check missing docstrings
            if not ast.get_docstring(node):
                smells["missing_docstrings"] += 1
            
            # Check long methods
            if hasattr(node, 'end_lineno') and node.end_lineno:
                length = node.end_lineno - node.lineno
                if length > 30:
                    smells["long_methods"] += 1
    
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            if not re.match(r'^[A-Z][a-zA-Z0-9]*$', node.name):
                smells["poor_naming"] += 1
            if not ast.get_docstring(node):
                smells["missing_docstrings"] += 1
    
    smells["total"] = sum(smells.values())
    return smells


def analyze_project(project_dir, project_name):
    """Run full analysis on a project directory."""
    py_files = []
    for root, dirs, files in os.walk(project_dir):
        for f in files:
            if f.endswith('.py'):
                py_files.append(os.path.join(root, f))
    
    total_loc = 0
    total_lines = 0
    total_funcs = 0
    total_classes = 0
    funcs_with_doc = 0
    classes_with_doc = 0
    all_complexities = []
    total_smells = {}
    mi_values = []
    
    for fp in py_files:
        loc, lines = count_loc(fp)
        total_loc += loc
        total_lines += lines
        
        funcs, classes, f_doc, c_doc = count_functions_classes(fp)
        total_funcs += funcs
        total_classes += classes
        funcs_with_doc += f_doc
        classes_with_doc += c_doc
        
        complexities, avg_cc = calculate_cyclomatic_complexity(fp)
        all_complexities.extend(complexities)
        
        mi = calculate_maintainability_index(fp)
        mi_values.append(mi)
        
        smells = detect_code_smells(fp)
        for k, v in smells.items():
            total_smells[k] = total_smells.get(k, 0) + v
    
    avg_cc = sum(c["complexity"] for c in all_complexities) / len(all_complexities) if all_complexities else 0
    avg_mi = sum(mi_values) / len(mi_values) if mi_values else 0
    doc_coverage = (funcs_with_doc / total_funcs * 100) if total_funcs > 0 else 0
    
    return {
        "project": project_name,
        "files": len(py_files),
        "total_loc": total_loc,
        "total_lines": total_lines,
        "functions": total_funcs,
        "classes": total_classes,
        "avg_cyclomatic_complexity": round(avg_cc, 2),
        "avg_maintainability_index": round(avg_mi, 2),
        "doc_coverage_pct": round(doc_coverage, 1),
        "funcs_with_docstrings": funcs_with_doc,
        "funcs_without_docstrings": total_funcs - funcs_with_doc,
        "code_smells": total_smells
    }


def run_benchmark():
    """Run the full benchmark across all test projects."""
    base = os.path.dirname(os.path.abspath(__file__))
    test_projects_dir = os.path.join(base, "test_projects")
    
    projects = [
        ("project1_utils", "Data Processing Utilities"),
        ("project2_fileops", "File Operations Module"),
        ("project3_taskmanager", "Task Management System"),
        ("project4_mathutils", "Math/Statistics Utilities"),
        ("project5_webutils", "Web/API Utilities"),
    ]
    
    results = []
    crew = RefactorCrew()
    
    for proj_dir_name, proj_display_name in projects:
        proj_path = os.path.join(test_projects_dir, proj_dir_name)
        if not os.path.exists(proj_path):
            print(f"  [SKIP] {proj_dir_name} not found")
            continue
        
        print(f"\n{'='*60}")
        print(f"  Project: {proj_display_name} ({proj_dir_name})")
        print(f"{'='*60}")
        
        # --- BEFORE metrics ---
        print("  [1/4] Measuring BEFORE metrics...")
        before = analyze_project(proj_path, proj_display_name)
        print(f"        LOC={before['total_loc']}, Funcs={before['functions']}, "
              f"CC={before['avg_cyclomatic_complexity']}, MI={before['avg_maintainability_index']}, "
              f"DocCov={before['doc_coverage_pct']}%")
        
        # --- Create working copy ---
        work_path = proj_path + "_refactored"
        if os.path.exists(work_path):
            shutil.rmtree(work_path)
        shutil.copytree(proj_path, work_path)
        
        # --- Run RefactorCrew ---
        print("  [2/4] Running RefactorCrew...")
        start_time = time.time()
        try:
            result = crew.kickoff({
                "target_directory": work_path,
                "mode": "refactor"
            })
            elapsed = time.time() - start_time
            refactor_status = "success"
            changes = result.get("changes_applied", [])
            files_modified = result.get("files_modified", [])
            print(f"        Completed in {elapsed:.2f}s — {len(files_modified)} files modified, {len(changes)} changes")
        except Exception as e:
            elapsed = time.time() - start_time
            refactor_status = f"error: {e}"
            changes = []
            files_modified = []
            print(f"        ERROR: {e}")
        
        # --- AFTER metrics ---
        print("  [3/4] Measuring AFTER metrics...")
        after = analyze_project(work_path, proj_display_name)
        print(f"        LOC={after['total_loc']}, Funcs={after['functions']}, "
              f"CC={after['avg_cyclomatic_complexity']}, MI={after['avg_maintainability_index']}, "
              f"DocCov={after['doc_coverage_pct']}%")
        
        # --- Compute deltas ---
        print("  [4/4] Computing deltas...")
        delta_cc = before['avg_cyclomatic_complexity'] - after['avg_cyclomatic_complexity']
        delta_mi = after['avg_maintainability_index'] - before['avg_maintainability_index']
        delta_loc = before['total_loc'] - after['total_loc']
        delta_doc = after['doc_coverage_pct'] - before['doc_coverage_pct']
        delta_funcs = before['functions'] - after['functions']
        smells_before = before['code_smells'].get('total', 0)
        smells_after = after['code_smells'].get('total', 0)
        delta_smells = smells_before - smells_after
        
        entry = {
            "project": proj_display_name,
            "dir": proj_dir_name,
            "before": before,
            "after": after,
            "deltas": {
                "cc_reduction": round(delta_cc, 2),
                "mi_improvement": round(delta_mi, 2),
                "loc_reduction": delta_loc,
                "doc_coverage_improvement": round(delta_doc, 1),
                "functions_removed": delta_funcs,
                "smells_resolved": delta_smells,
            },
            "runtime_seconds": round(elapsed, 2),
            "refactor_status": refactor_status,
            "changes_applied": changes,
            "files_modified": files_modified,
        }
        results.append(entry)
    
    # --- Save results ---
    output_path = os.path.join(base, "benchmark_results.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n\n{'='*60}")
    print(f"  RESULTS SAVED TO: {output_path}")
    print(f"{'='*60}")
    
    # --- Print summary table ---
    print(f"\n{'='*80}")
    print(f"  BENCHMARK SUMMARY")
    print(f"{'='*80}")
    print(f"{'Project':<30} {'CC Δ':>8} {'MI Δ':>8} {'LOC Δ':>8} {'Doc Δ':>8} {'Smells Δ':>10} {'Time(s)':>8}")
    print("-" * 80)
    for r in results:
        d = r['deltas']
        print(f"{r['project']:<30} {d['cc_reduction']:>+8.2f} {d['mi_improvement']:>+8.2f} "
              f"{d['loc_reduction']:>+8d} {d['doc_coverage_improvement']:>+8.1f}% "
              f"{d['smells_resolved']:>+10d} {r['runtime_seconds']:>8.2f}")
    
    # Averages
    if results:
        avg_cc = sum(r['deltas']['cc_reduction'] for r in results) / len(results)
        avg_mi = sum(r['deltas']['mi_improvement'] for r in results) / len(results)
        avg_loc = sum(r['deltas']['loc_reduction'] for r in results) / len(results)
        avg_doc = sum(r['deltas']['doc_coverage_improvement'] for r in results) / len(results)
        avg_smells = sum(r['deltas']['smells_resolved'] for r in results) / len(results)
        avg_time = sum(r['runtime_seconds'] for r in results) / len(results)
        print("-" * 80)
        print(f"{'AVERAGE':<30} {avg_cc:>+8.2f} {avg_mi:>+8.2f} "
              f"{int(avg_loc):>+8d} {avg_doc:>+8.1f}% "
              f"{int(avg_smells):>+10d} {avg_time:>8.2f}")
    
    return results


if __name__ == "__main__":
    run_benchmark()
