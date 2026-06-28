"""
Generate publication-quality benchmark result charts for the Blackbook.
Run: python generate_result_charts.py
Output: ./result_screenshots/ directory with all charts as PNG files.
"""

import json
import os
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import numpy as np

# ── Configuration ────────────────────────────────────────────────────────
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "result_screenshots")
BENCHMARK_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "benchmark_results.json")

# Color palette — LIGHT theme
BG_COLOR = "#FFFFFF"
CARD_BG = "#F8F9FA"
TEXT_COLOR = "#1F2937"
ACCENT_BLUE = "#2563EB"
ACCENT_GREEN = "#16A34A"
ACCENT_RED = "#DC2626"
ACCENT_ORANGE = "#D97706"
ACCENT_PURPLE = "#7C3AED"
ACCENT_CYAN = "#0891B2"
GRID_COLOR = "#E5E7EB"
BORDER_COLOR = "#D1D5DB"

# Before/After colors
BEFORE_COLOR = "#FEE2E2"    # Light red fill
AFTER_COLOR = "#DCFCE7"     # Light green fill
BEFORE_EDGE = "#DC2626"
AFTER_EDGE = "#16A34A"


def load_data():
    with open(BENCHMARK_FILE, 'r') as f:
        return json.load(f)


def setup_light_style():
    """Configure matplotlib for light theme."""
    plt.rcParams.update({
        'figure.facecolor': BG_COLOR,
        'axes.facecolor': BG_COLOR,
        'axes.edgecolor': BORDER_COLOR,
        'axes.labelcolor': TEXT_COLOR,
        'text.color': TEXT_COLOR,
        'xtick.color': TEXT_COLOR,
        'ytick.color': TEXT_COLOR,
        'grid.color': GRID_COLOR,
        'grid.alpha': 0.5,
        'font.family': 'sans-serif',
        'font.sans-serif': ['Segoe UI', 'Arial', 'Helvetica', 'DejaVu Sans'],
        'font.size': 11,
        'axes.titlesize': 14,
        'axes.labelsize': 12,
        'figure.titlesize': 18,
    })


def add_watermark(fig):
    """Add a subtle watermark/branding."""
    fig.text(0.99, 0.01, 'RefactorCrew Benchmark', fontsize=8,
             color=TEXT_COLOR, alpha=0.2, ha='right', va='bottom',
             fontstyle='italic')


# ═══════════════════════════════════════════════════════════════════════
# CHART 1: Before vs After — Key Metrics Comparison (Grouped Bar)
# ═══════════════════════════════════════════════════════════════════════
def chart_before_after_metrics(data):
    """Grouped bar chart comparing before/after for CC, MI, LOC, Functions."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Before vs After Refactoring \u2014 Key Metrics", fontsize=20, fontweight='bold', y=0.98)
    fig.subplots_adjust(hspace=0.4, wspace=0.3, top=0.90, bottom=0.08)

    projects = [d['project'].replace(' ', '\n') for d in data]
    x = np.arange(len(projects))
    width = 0.35

    # ── Cyclomatic Complexity ──
    ax = axes[0, 0]
    before_vals = [d['before']['avg_cyclomatic_complexity'] for d in data]
    after_vals = [d['after']['avg_cyclomatic_complexity'] for d in data]
    bars1 = ax.bar(x - width/2, before_vals, width, label='Before', color=BEFORE_COLOR,
                   edgecolor=BEFORE_EDGE, linewidth=1.5)
    bars2 = ax.bar(x + width/2, after_vals, width, label='After', color=AFTER_COLOR,
                   edgecolor=AFTER_EDGE, linewidth=1.5)
    ax.set_title("Cyclomatic Complexity (Lower = Better)", fontweight='bold', pad=10)
    ax.set_ylabel("Avg CC")
    ax.set_xticks(x)
    ax.set_xticklabels(projects, fontsize=8)
    ax.legend(framealpha=0.9, edgecolor=BORDER_COLOR)
    ax.grid(axis='y', alpha=0.3)
    for bar in bars1:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                f'{bar.get_height():.1f}', ha='center', va='bottom', fontsize=8, color=ACCENT_RED)
    for bar in bars2:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                f'{bar.get_height():.1f}', ha='center', va='bottom', fontsize=8, color=ACCENT_GREEN)

    # ── Maintainability Index ──
    ax = axes[0, 1]
    before_vals = [d['before']['avg_maintainability_index'] for d in data]
    after_vals = [d['after']['avg_maintainability_index'] for d in data]
    bars1 = ax.bar(x - width/2, before_vals, width, label='Before', color=BEFORE_COLOR,
                   edgecolor=BEFORE_EDGE, linewidth=1.5)
    bars2 = ax.bar(x + width/2, after_vals, width, label='After', color=AFTER_COLOR,
                   edgecolor=AFTER_EDGE, linewidth=1.5)
    ax.set_title("Maintainability Index", fontweight='bold', pad=10)
    ax.set_ylabel("Avg MI")
    ax.set_xticks(x)
    ax.set_xticklabels(projects, fontsize=8)
    ax.legend(framealpha=0.9, edgecolor=BORDER_COLOR)
    ax.grid(axis='y', alpha=0.3)
    for bar in bars1:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                f'{bar.get_height():.1f}', ha='center', va='bottom', fontsize=8, color=ACCENT_RED)
    for bar in bars2:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                f'{bar.get_height():.1f}', ha='center', va='bottom', fontsize=8, color=ACCENT_GREEN)

    # ── Documentation Coverage ──
    ax = axes[1, 0]
    before_vals = [d['before']['doc_coverage_pct'] for d in data]
    after_vals = [d['after']['doc_coverage_pct'] for d in data]
    bars1 = ax.bar(x - width/2, before_vals, width, label='Before', color=BEFORE_COLOR,
                   edgecolor=BEFORE_EDGE, linewidth=1.5)
    bars2 = ax.bar(x + width/2, after_vals, width, label='After', color=AFTER_COLOR,
                   edgecolor=AFTER_EDGE, linewidth=1.5)
    ax.set_title("Documentation Coverage % (Higher = Better)", fontweight='bold', pad=10)
    ax.set_ylabel("Coverage %")
    ax.set_xticks(x)
    ax.set_xticklabels(projects, fontsize=8)
    ax.set_ylim(0, 115)
    ax.legend(framealpha=0.9, edgecolor=BORDER_COLOR)
    ax.grid(axis='y', alpha=0.3)
    for bar in bars1:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f'{bar.get_height():.0f}%', ha='center', va='bottom', fontsize=8, color=ACCENT_RED)
    for bar in bars2:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f'{bar.get_height():.0f}%', ha='center', va='bottom', fontsize=8, color=ACCENT_GREEN)

    # ── Code Smells ──
    ax = axes[1, 1]
    before_vals = [d['before']['code_smells']['total'] for d in data]
    after_vals = [d['after']['code_smells']['total'] for d in data]
    bars1 = ax.bar(x - width/2, before_vals, width, label='Before', color=BEFORE_COLOR,
                   edgecolor=BEFORE_EDGE, linewidth=1.5)
    bars2 = ax.bar(x + width/2, after_vals, width, label='After', color=AFTER_COLOR,
                   edgecolor=AFTER_EDGE, linewidth=1.5)
    ax.set_title("Code Smells Count (Lower = Better)", fontweight='bold', pad=10)
    ax.set_ylabel("Total Smells")
    ax.set_xticks(x)
    ax.set_xticklabels(projects, fontsize=8)
    ax.legend(framealpha=0.9, edgecolor=BORDER_COLOR)
    ax.grid(axis='y', alpha=0.3)
    for bar in bars1:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                f'{int(bar.get_height())}', ha='center', va='bottom', fontsize=8, color=ACCENT_RED)
    for bar in bars2:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                f'{int(bar.get_height())}', ha='center', va='bottom', fontsize=8, color=ACCENT_GREEN)

    add_watermark(fig)
    path = os.path.join(OUTPUT_DIR, "fig1_before_after_metrics.png")
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor=BG_COLOR)
    plt.close(fig)
    print(f"  [OK] Saved: {path}")


# ═══════════════════════════════════════════════════════════════════════
# CHART 2: Code Smells Breakdown — Stacked Bar
# ═══════════════════════════════════════════════════════════════════════
def chart_code_smells_breakdown(data):
    """Stacked bar chart showing code smell categories before and after."""
    fig, ax = plt.subplots(figsize=(14, 7))
    fig.suptitle("Code Smells Breakdown \u2014 Before vs After Refactoring", fontsize=18, fontweight='bold', y=0.97)
    fig.subplots_adjust(top=0.88, bottom=0.15)

    categories = ['duplicate_functions', 'poor_naming', 'missing_docstrings', 'long_methods']
    cat_labels = ['Duplicate\nFunctions', 'Poor\nNaming', 'Missing\nDocstrings', 'Long\nMethods']
    colors_before = ['#FECACA', '#FDE68A', '#DDD6FE', '#BFDBFE']
    colors_after = ['#BBF7D0', '#A7F3D0', '#BAE6FD', '#C7D2FE']
    edge_before = [ACCENT_RED, ACCENT_ORANGE, ACCENT_PURPLE, ACCENT_BLUE]
    edge_after = [ACCENT_GREEN, ACCENT_CYAN, '#3B82F6', '#6366F1']

    projects = [d['project'] for d in data]
    n = len(projects)
    x = np.arange(n)
    width = 0.35

    # Before bars (stacked)
    bottom_before = np.zeros(n)
    for i, cat in enumerate(categories):
        vals = [d['before']['code_smells'].get(cat, 0) for d in data]
        ax.bar(x - width/2, vals, width, bottom=bottom_before, label=f'Before: {cat_labels[i].replace(chr(10), " ")}',
               color=colors_before[i], edgecolor=edge_before[i], linewidth=1)
        bottom_before += np.array(vals)

    # After bars (stacked)
    bottom_after = np.zeros(n)
    for i, cat in enumerate(categories):
        vals = [d['after']['code_smells'].get(cat, 0) for d in data]
        ax.bar(x + width/2, vals, width, bottom=bottom_after, label=f'After: {cat_labels[i].replace(chr(10), " ")}',
               color=colors_after[i], edgecolor=edge_after[i], linewidth=1)
        bottom_after += np.array(vals)

    # Add total labels on top
    for i in range(n):
        total_b = sum(d['before']['code_smells'].get(c, 0) for c in categories for d in [data[i]])
        total_a = sum(d['after']['code_smells'].get(c, 0) for c in categories for d in [data[i]])
        reduction = total_b - total_a
        pct = (reduction / total_b * 100) if total_b > 0 else 0
        ax.text(x[i] - width/2, bottom_before[i] + 0.5, f'{int(bottom_before[i])}',
                ha='center', va='bottom', fontsize=9, fontweight='bold', color=ACCENT_RED)
        ax.text(x[i] + width/2, bottom_after[i] + 0.5, f'{int(bottom_after[i])}',
                ha='center', va='bottom', fontsize=9, fontweight='bold', color=ACCENT_GREEN)
        # Reduction annotation
        ax.annotate(f'\u2193{pct:.0f}%', xy=(x[i], max(bottom_before[i], bottom_after[i]) + 3),
                    ha='center', fontsize=10, fontweight='bold', color=ACCENT_BLUE)

    ax.set_xticks(x)
    ax.set_xticklabels(projects, fontsize=9)
    ax.set_ylabel("Number of Code Smells")
    ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=8,
              framealpha=0.9, edgecolor=BORDER_COLOR, ncol=1)
    ax.grid(axis='y', alpha=0.3)

    add_watermark(fig)
    path = os.path.join(OUTPUT_DIR, "fig2_code_smells_breakdown.png")
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor=BG_COLOR)
    plt.close(fig)
    print(f"  [OK] Saved: {path}")


# ═══════════════════════════════════════════════════════════════════════
# CHART 3: Documentation Coverage — Before vs After with 100% highlight
# ═══════════════════════════════════════════════════════════════════════
def chart_documentation_coverage(data):
    """Horizontal bar chart emphasizing 0% to 100% documentation improvement."""
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.suptitle("Documentation Coverage \u2014 0% to 100% Across All Projects", fontsize=18, fontweight='bold', y=0.97)
    fig.subplots_adjust(top=0.88, bottom=0.1, left=0.25)

    projects = [d['project'] for d in data]
    n = len(projects)
    y = np.arange(n)
    height = 0.35

    before_vals = [d['before']['doc_coverage_pct'] for d in data]
    after_vals = [d['after']['doc_coverage_pct'] for d in data]

    # Before bars
    ax.barh(y + height/2, before_vals, height, label='Before (0%)',
            color=BEFORE_COLOR, edgecolor=BEFORE_EDGE, linewidth=1.5)
    # After bars
    ax.barh(y - height/2, after_vals, height, label='After (100%)',
            color=AFTER_COLOR, edgecolor=AFTER_EDGE, linewidth=1.5)

    # Add labels
    for i in range(n):
        ax.text(after_vals[i] + 1, y[i] - height/2, f'{after_vals[i]:.0f}%',
                va='center', fontsize=10, fontweight='bold', color=ACCENT_GREEN)
        ax.text(max(before_vals[i], 2), y[i] + height/2, f'{before_vals[i]:.0f}%',
                va='center', fontsize=10, fontweight='bold', color=ACCENT_RED)

        # Functions documented count
        funcs_before = data[i]['before']['funcs_with_docstrings']
        funcs_after = data[i]['after']['funcs_with_docstrings']
        total_funcs = data[i]['after']['functions']
        ax.text(108, y[i], f'{funcs_before}\u2192{funcs_after}/{total_funcs} funcs',
                va='center', fontsize=8, color=ACCENT_BLUE)

    ax.set_yticks(y)
    ax.set_yticklabels(projects, fontsize=10)
    ax.set_xlabel("Documentation Coverage %")
    ax.set_xlim(0, 130)
    ax.legend(framealpha=0.9, edgecolor=BORDER_COLOR, loc='lower right')
    ax.grid(axis='x', alpha=0.3)

    # Add a "100% target" line
    ax.axvline(x=100, color=ACCENT_GREEN, linestyle='--', alpha=0.4, linewidth=1)
    ax.text(100, n - 0.2, '100% Target', ha='center', va='bottom', fontsize=8,
            color=ACCENT_GREEN, alpha=0.6)

    add_watermark(fig)
    path = os.path.join(OUTPUT_DIR, "fig3_documentation_coverage.png")
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor=BG_COLOR)
    plt.close(fig)
    print(f"  [OK] Saved: {path}")


# ═══════════════════════════════════════════════════════════════════════
# CHART 4: Summary Dashboard — Aggregate Metrics
# ═══════════════════════════════════════════════════════════════════════
def chart_summary_dashboard(data):
    """Dashboard-style figure with key aggregate stats."""
    fig = plt.figure(figsize=(14, 8))
    fig.suptitle("RefactorCrew \u2014 Benchmark Summary Dashboard", fontsize=20, fontweight='bold', y=0.97)

    gs = GridSpec(2, 4, figure=fig, hspace=0.5, wspace=0.4, top=0.88, bottom=0.08, left=0.06, right=0.94)

    # Calculate aggregate metrics
    total_smells_before = sum(d['before']['code_smells']['total'] for d in data)
    total_smells_after = sum(d['after']['code_smells']['total'] for d in data)
    total_smells_resolved = total_smells_before - total_smells_after

    total_changes = sum(len(d.get('changes_applied', [])) for d in data)
    total_files = sum(len(d.get('files_modified', [])) for d in data)
    avg_runtime = np.mean([d['runtime_seconds'] for d in data])

    # ── KPI Cards (Top Row) ──
    kpis = [
        ("Code Smells\nResolved", f"{total_smells_resolved}", f"of {total_smells_before}", ACCENT_GREEN),
        ("Doc Coverage\nImprovement", "0% \u2192 100%", "All 5 projects", ACCENT_BLUE),
        ("Total Changes\nApplied", f"{total_changes}", f"across {total_files} files", ACCENT_PURPLE),
        ("Avg Runtime\nPer Project", f"{avg_runtime:.2f}s", "near real-time", ACCENT_CYAN),
    ]

    for i, (title, value, subtitle, color) in enumerate(kpis):
        ax = fig.add_subplot(gs[0, i])
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')

        # Card background
        card = mpatches.FancyBboxPatch((0.02, 0.02), 0.96, 0.96,
                                        boxstyle="round,pad=0.05",
                                        facecolor=CARD_BG, edgecolor=color,
                                        linewidth=2)
        ax.add_patch(card)

        ax.text(0.5, 0.78, title, ha='center', va='center', fontsize=10,
                fontweight='bold', color=TEXT_COLOR, alpha=0.7)
        ax.text(0.5, 0.45, value, ha='center', va='center', fontsize=22,
                fontweight='bold', color=color)
        ax.text(0.5, 0.18, subtitle, ha='center', va='center', fontsize=9,
                color=TEXT_COLOR, alpha=0.45)

    # ── Bottom Left: Smell Reduction Donut ──
    ax = fig.add_subplot(gs[1, 0:2])
    categories = ['Duplicate Functions', 'Poor Naming', 'Missing Docstrings', 'Long Methods']
    cat_keys = ['duplicate_functions', 'poor_naming', 'missing_docstrings', 'long_methods']
    resolved_by_cat = []
    for key in cat_keys:
        before = sum(d['before']['code_smells'].get(key, 0) for d in data)
        after = sum(d['after']['code_smells'].get(key, 0) for d in data)
        resolved_by_cat.append(before - after)

    colors = [ACCENT_RED, ACCENT_ORANGE, ACCENT_PURPLE, ACCENT_BLUE]
    wedges, texts, autotexts = ax.pie(
        resolved_by_cat, labels=categories, autopct='%1.0f%%',
        colors=colors, startangle=90, pctdistance=0.75,
        wedgeprops=dict(width=0.35, edgecolor='white', linewidth=2),
        textprops=dict(color=TEXT_COLOR, fontsize=9)
    )
    for t in autotexts:
        t.set_color('white')
        t.set_fontsize(9)
        t.set_fontweight('bold')
    ax.set_title(f"Code Smells Resolved by Category\n(Total: {total_smells_resolved})",
                 fontweight='bold', fontsize=12, pad=10)

    # ── Bottom Right: Per-Project Changes Bar ──
    ax = fig.add_subplot(gs[1, 2:4])
    projects = [d['project'] for d in data]
    changes_per_proj = [len(d.get('changes_applied', [])) for d in data]
    bar_colors = [ACCENT_BLUE, ACCENT_GREEN, ACCENT_PURPLE, ACCENT_ORANGE, ACCENT_CYAN]
    bars = ax.barh(projects, changes_per_proj, color=bar_colors,
                   edgecolor=BORDER_COLOR, linewidth=0.5)
    for bar, val in zip(bars, changes_per_proj):
        ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
                f'{val}', va='center', fontsize=10, fontweight='bold', color=TEXT_COLOR)
    ax.set_xlabel("Number of Changes Applied")
    ax.set_title("Refactoring Changes Per Project", fontweight='bold', fontsize=12, pad=10)
    ax.grid(axis='x', alpha=0.3)
    ax.invert_yaxis()

    add_watermark(fig)
    path = os.path.join(OUTPUT_DIR, "fig4_summary_dashboard.png")
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor=BG_COLOR)
    plt.close(fig)
    print(f"  [OK] Saved: {path}")


# ═══════════════════════════════════════════════════════════════════════
# CHART 5: Benchmark Results Table (publication-style) — FIXED WIDTH
# ═══════════════════════════════════════════════════════════════════════
def chart_results_table(data):
    """Render a styled table of benchmark results as an image."""
    fig, ax = plt.subplots(figsize=(20, 7))
    fig.suptitle("Experimental Results \u2014 Before vs After Refactoring (5 Test Projects)",
                 fontsize=18, fontweight='bold', y=0.96)
    fig.subplots_adjust(top=0.85, bottom=0.05, left=0.02, right=0.98)
    ax.axis('off')

    columns = ['Project', 'Files', 'LOC\n(Before)', 'LOC\n(After)',
               'CC\n(Before)', 'CC\n(After)',
               'MI\n(Before)', 'MI\n(After)',
               'Doc %\n(Before)', 'Doc %\n(After)',
               'Smells\n(Before)', 'Smells\n(After)',
               'Smells\nResolved']

    cell_data = []
    for d in data:
        row = [
            d['project'],
            str(d['before']['files']),
            str(d['before']['total_loc']),
            str(d['after']['total_loc']),
            f"{d['before']['avg_cyclomatic_complexity']:.2f}",
            f"{d['after']['avg_cyclomatic_complexity']:.2f}",
            f"{d['before']['avg_maintainability_index']:.1f}",
            f"{d['after']['avg_maintainability_index']:.1f}",
            f"{d['before']['doc_coverage_pct']:.0f}%",
            f"{d['after']['doc_coverage_pct']:.0f}%",
            str(d['before']['code_smells']['total']),
            str(d['after']['code_smells']['total']),
            str(d['deltas']['smells_resolved']),
        ]
        cell_data.append(row)

    # Average row
    avg_row = [
        'AVERAGE',
        '-',
        f"{np.mean([d['before']['total_loc'] for d in data]):.0f}",
        f"{np.mean([d['after']['total_loc'] for d in data]):.0f}",
        f"{np.mean([d['before']['avg_cyclomatic_complexity'] for d in data]):.2f}",
        f"{np.mean([d['after']['avg_cyclomatic_complexity'] for d in data]):.2f}",
        f"{np.mean([d['before']['avg_maintainability_index'] for d in data]):.1f}",
        f"{np.mean([d['after']['avg_maintainability_index'] for d in data]):.1f}",
        f"{np.mean([d['before']['doc_coverage_pct'] for d in data]):.0f}%",
        f"{np.mean([d['after']['doc_coverage_pct'] for d in data]):.0f}%",
        f"{np.mean([d['before']['code_smells']['total'] for d in data]):.0f}",
        f"{np.mean([d['after']['code_smells']['total'] for d in data]):.0f}",
        f"{np.mean([d['deltas']['smells_resolved'] for d in data]):.0f}",
    ]
    cell_data.append(avg_row)

    table = ax.table(cellText=cell_data, colLabels=columns,
                     cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2.0)

    # Set column widths — wider for Project column
    col_widths = [0.15, 0.05, 0.065, 0.065, 0.065, 0.065, 0.065, 0.065, 0.065, 0.065, 0.065, 0.065, 0.07]
    for (row, col), cell in table.get_celld().items():
        if col < len(col_widths):
            cell.set_width(col_widths[col])

    # Style the table
    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor(BORDER_COLOR)
        cell.set_linewidth(0.8)
        if row == 0:
            # Header
            cell.set_facecolor(ACCENT_BLUE)
            cell.set_text_props(color='white', fontweight='bold', fontsize=9)
        elif row == len(cell_data):
            # Average row
            cell.set_facecolor('#EEF2FF')
            cell.set_text_props(color=ACCENT_BLUE, fontweight='bold', fontsize=10)
        else:
            # Alternate row colors
            if row % 2 == 0:
                cell.set_facecolor('#F9FAFB')
            else:
                cell.set_facecolor('#FFFFFF')
            cell.set_text_props(color=TEXT_COLOR, fontsize=10)

            # Color-code improvements
            if col == 9:  # Doc After
                cell.set_text_props(color=ACCENT_GREEN, fontweight='bold', fontsize=10)
            elif col == 8:  # Doc Before
                cell.set_text_props(color=ACCENT_RED, fontweight='bold', fontsize=10)
            elif col == 12:  # Smells Resolved
                cell.set_text_props(color=ACCENT_GREEN, fontweight='bold', fontsize=10)

    add_watermark(fig)
    path = os.path.join(OUTPUT_DIR, "fig5_results_table.png")
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor=BG_COLOR)
    plt.close(fig)
    print(f"  [OK] Saved: {path}")


# ═══════════════════════════════════════════════════════════════════════
# CHART 6: Improvement Radar Chart
# ═══════════════════════════════════════════════════════════════════════
def chart_improvement_radar(data):
    """Radar/spider chart showing improvement dimensions per project."""
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
    fig.suptitle("Multi-Dimensional Improvement Radar \u2014 Per Project",
                 fontsize=18, fontweight='bold', y=0.98)
    fig.subplots_adjust(top=0.88)

    categories = [
        'CC\nReduction',
        'Doc Coverage\nImprovement',
        'Smells\nResolved %',
        'Duplicates\nRemoved %',
        'Functions\nOptimized'
    ]
    N = len(categories)

    colors = [ACCENT_BLUE, ACCENT_GREEN, ACCENT_PURPLE, ACCENT_ORANGE, ACCENT_CYAN]
    fill_colors = ['#DBEAFE', '#DCFCE7', '#EDE9FE', '#FEF3C7', '#CFFAFE']

    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]

    ax.set_facecolor('#FAFAFA')
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=9)
    ax.tick_params(axis='x', pad=15)

    for i, d in enumerate(data):
        before_smells = d['before']['code_smells']['total']
        after_smells = d['after']['code_smells']['total']
        smell_pct = ((before_smells - after_smells) / before_smells * 100) if before_smells > 0 else 0

        before_dup = d['before']['code_smells'].get('duplicate_functions', 0)
        after_dup = d['after']['code_smells'].get('duplicate_functions', 0)
        dup_pct = ((before_dup - after_dup) / before_dup * 100) if before_dup > 0 else 0

        values = [
            max(0, d['deltas']['cc_reduction'] * 30),
            d['deltas']['doc_coverage_improvement'],
            smell_pct,
            dup_pct,
            d['deltas']['functions_removed'] * 25,
        ]
        values = [min(v, 100) for v in values]
        values += values[:1]

        ax.plot(angles, values, 'o-', linewidth=2, color=colors[i], label=d['project'], alpha=0.9)
        ax.fill(angles, values, color=fill_colors[i], alpha=0.3)

    ax.set_ylim(0, 110)
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(['20', '40', '60', '80', '100'], fontsize=7, color=TEXT_COLOR, alpha=0.5)
    ax.yaxis.grid(True, color=GRID_COLOR, alpha=0.5)
    ax.xaxis.grid(True, color=GRID_COLOR, alpha=0.5)
    ax.spines['polar'].set_color(BORDER_COLOR)

    ax.legend(loc='lower right', bbox_to_anchor=(1.3, -0.05), fontsize=9,
              framealpha=0.9, edgecolor=BORDER_COLOR)

    add_watermark(fig)
    path = os.path.join(OUTPUT_DIR, "fig6_improvement_radar.png")
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor=BG_COLOR)
    plt.close(fig)
    print(f"  [OK] Saved: {path}")


# ═══════════════════════════════════════════════════════════════════════
# CHART 7: Changes Applied Breakdown — FIXED LAYOUT
# ═══════════════════════════════════════════════════════════════════════
def chart_changes_breakdown(data):
    """Categorize and show types of changes applied."""
    fig, ax = plt.subplots(figsize=(14, 7))
    fig.suptitle("Types of Refactoring Changes Applied", fontsize=18, fontweight='bold', y=0.97)
    fig.subplots_adjust(top=0.88, bottom=0.12, left=0.22)

    # Categorize changes
    change_types = {
        'Added Docstrings': 0,
        'Removed Duplicates': 0,
        'Improved Variable Names': 0,
        'Refactored Class Names': 0,
    }
    per_project = {p['project']: dict(change_types) for p in data}

    for d in data:
        for change in d.get('changes_applied', []):
            change_lower = change.lower()
            proj = d['project']
            if 'added docstring' in change_lower:
                change_types['Added Docstrings'] += 1
                per_project[proj]['Added Docstrings'] += 1
            elif 'removed' in change_lower and 'duplicate' in change_lower:
                change_types['Removed Duplicates'] += 1
                per_project[proj]['Removed Duplicates'] += 1
            elif 'variable names' in change_lower or 'improved variable' in change_lower:
                change_types['Improved Variable Names'] += 1
                per_project[proj]['Improved Variable Names'] += 1
            elif 'refactored class' in change_lower or 'class name' in change_lower:
                change_types['Refactored Class Names'] += 1
                per_project[proj]['Refactored Class Names'] += 1

    projects = [d['project'] for d in data]
    categories_list = list(change_types.keys())
    bar_colors = ['#C4B5FD', '#FCA5A5', '#FDE68A', '#99F6E4']
    edge_colors = [ACCENT_PURPLE, ACCENT_RED, ACCENT_ORANGE, ACCENT_CYAN]

    y = np.arange(len(projects))
    left = np.zeros(len(projects))

    for i, cat in enumerate(categories_list):
        vals = [per_project[p][cat] for p in projects]
        bars = ax.barh(y, vals, left=left, label=cat, color=bar_colors[i],
                       edgecolor=edge_colors[i], linewidth=1, height=0.6)
        # Add count labels on bars
        for j, (bar, val) in enumerate(zip(bars, vals)):
            if val > 0:
                ax.text(left[j] + val/2, bar.get_y() + bar.get_height()/2,
                        str(val), ha='center', va='center', fontsize=9,
                        fontweight='bold', color=TEXT_COLOR)
        left += np.array(vals)

    # Total labels
    for i, total in enumerate(left):
        ax.text(total + 0.3, y[i], f'Total: {int(total)}', va='center',
                fontsize=10, fontweight='bold', color=ACCENT_GREEN)

    ax.set_yticks(y)
    ax.set_yticklabels(projects, fontsize=10)
    ax.set_xlabel("Number of Changes")
    ax.grid(axis='x', alpha=0.3)
    ax.invert_yaxis()

    # Legend at top-right, NOT overlapping with data
    ax.legend(loc='upper right', framealpha=0.9, edgecolor=BORDER_COLOR, fontsize=10,
              bbox_to_anchor=(1.0, 1.0))

    # Grand total annotation at top-left, away from legend
    grand_total = int(sum(left))
    ax.text(0.02, 0.02, f'Grand Total: {grand_total} changes across {len(data)} projects',
            transform=ax.transAxes, ha='left', va='bottom', fontsize=11,
            fontweight='bold', color=ACCENT_BLUE, alpha=0.8,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#EFF6FF', edgecolor=ACCENT_BLUE, alpha=0.7))

    add_watermark(fig)
    path = os.path.join(OUTPUT_DIR, "fig7_changes_breakdown.png")
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor=BG_COLOR)
    plt.close(fig)
    print(f"  [OK] Saved: {path}")


# ═══════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════
def main():
    print("=" * 60)
    print("  RefactorCrew -- Generating Blackbook Result Charts")
    print("=" * 60)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    setup_light_style()
    data = load_data()

    print(f"\n  Loaded {len(data)} project results from benchmark_results.json\n")

    print("  Generating charts...")
    chart_before_after_metrics(data)
    chart_code_smells_breakdown(data)
    chart_documentation_coverage(data)
    chart_summary_dashboard(data)
    chart_results_table(data)
    chart_improvement_radar(data)
    chart_changes_breakdown(data)

    print(f"\n{'=' * 60}")
    print(f"  All charts saved to: {OUTPUT_DIR}")
    print(f"  Total: 7 publication-quality figures (LIGHT MODE)")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
