# -*- coding: utf-8 -*-
# ruff: noqa: N806, N815

"""
kececisquares.py
Keçeci Binomial Squares (Keçeci Binom Kareleri)
Keçeci-Narayana Shapes (Keçeci-Narayana Şekilleri)

The Keçeci Binomial Square is a series of binomial coefficients 
forming a square or other geometric shapes region within Khayyam (مثلث خیام), 
Pascal, Binomial Triangle, selected from a specified starting row with defined 
size and alignment.

Narayana üçgeni içinde belirli alt alanların seçilmesiyle elde edilen 
geometrik bölgeler Keçeci-Narayana Şekilleri (Keçeci-Narayana Shapes) 
olarak adlandırılmıştır.

Keçeci Binomial & Keçeci-Narayana Visualizer

Provides tools for generating Pascal/Khayyam and Narayana triangles,
selecting geometric regions, visualizing on hexagonal grids, and
exporting statistical reports.
"""

from __future__ import annotations

import datetime
import json
import csv
import platform
import warnings
from collections import Counter
from math import comb
from statistics import mean, median, stdev, variance
from typing import List, Dict, Optional, Tuple, Any

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Polygon, Rectangle, RegularPolygon

# =============================================================================
# METADATA
# =============================================================================
PYTHON_VERSION = platform.python_version()
TIMESTAMP = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# =============================================================================
# 1. TRIANGLE GENERATORS
# =============================================================================
def generate_binomial_triangle(num_rows: int) -> List[List[int]]:
    """
    Generate Pascal/Khayyam triangle up to `num_rows`.
    Pascal/Binom üçgeni oluşturur.
    """
    if num_rows < 1:
        raise ValueError("Number of rows must be at least 1.")
    triangle = []
    for r in range(num_rows):
        row = [1]
        if r > 0:
            prev = triangle[-1]
            row.extend(prev[j] + prev[j + 1] for j in range(r - 1))
            row.append(1)
        triangle.append(row)
    return triangle


def generate_narayana_triangle(num_rows: int) -> List[List[int]]:
    """Generate Narayana triangle: N(n,k) = C(n,k)*C(n,k-1)/n."""
    if num_rows < 1:
        raise ValueError("Number of rows must be at least 1.")
    triangle = []
    for n in range(1, num_rows + 1):
        row = [comb(n, k) * comb(n, k - 1) // n for k in range(1, n + 1)]
        triangle.append(row)
    return triangle


# =============================================================================
# 2. HELPER: SLICE CALCULATOR
# =============================================================================
def _get_slice_indices(row_length: int, elements: int, alignment: str) -> Tuple[int, int]:
    """Calculate start/end column indices for a given alignment."""
    if alignment == "left":
        return 0, elements
    if alignment == "right":
        return row_length - elements, row_length
    # center
    start = (row_length - elements) // 2
    return start, start + elements


# =============================================================================
# 3. REGION SELECTORS (BINOMIAL) - STANDARDIZED PARAMETER NAMES
# =============================================================================
def kececi_binomial_square(triangle: List[List[int]], size: int, start_row: int, alignment: str) -> Tuple[List[int], int, List[Dict]]:
    """Select a square region from binomial triangle."""
    if size < 1 or start_row < 0 or start_row + size > len(triangle):
        raise ValueError("Invalid square parameters.")
    
    series, info = [], []
    for i in range(size):
        row_idx = start_row + i
        row = triangle[row_idx]
        if size > len(row):
            raise ValueError(f"Row {row_idx + 1} too short for square.")
        s, e = _get_slice_indices(len(row), size, alignment)
        series.extend(row[s:e])
        info.append({"row_index": row_idx, "slice_start_col": s, "slice_end_col": e})
    return series, sum(series), info


def kececi_binomial_triangle(triangle: List[List[int]], size: int, start_row: int, alignment: str) -> Tuple[List[int], int, List[Dict]]:
    """Select a triangular region from binomial triangle."""
    if size < 1 or start_row < 0 or start_row + size > len(triangle):
        raise ValueError("Invalid triangle parameters.")
    
    series, info = [], []
    for i in range(size):
        row_idx = start_row + i
        row = triangle[row_idx]
        elements = i + 1
        if elements > len(row):
            raise ValueError(f"Row {row_idx + 1} too short.")
        s, e = _get_slice_indices(len(row), elements, alignment)
        series.extend(row[s:e])
        info.append({"row_index": row_idx, "slice_start_col": s, "slice_end_col": e})
    return series, sum(series), info


def kececi_binomial_diamond(triangle: List[List[int]], size: int, start_row: int, alignment: str) -> Tuple[List[int], int, List[Dict]]:
    """Select a diamond-shaped region (center alignment only)."""
    if alignment != "center":
        raise ValueError("Diamond only supports 'center' alignment.")
    if size < 1 or start_row < 0:
        raise ValueError("Invalid diamond parameters.")
    
    height = 2 * size - 1
    if start_row + height > len(triangle):
        raise ValueError("Diamond exceeds triangle bounds.")
    
    series, info = [], []
    # Upper half including middle
    for i in range(size):
        r = start_row + i
        row = triangle[r]
        s, e = _get_slice_indices(len(row), i + 1, "center")
        series.extend(row[s:e])
        info.append({"row_index": r, "slice_start_col": s, "slice_end_col": e})
    # Lower half
    for i in range(1, size):
        r = start_row + size - 1 + i
        row = triangle[r]
        s, e = _get_slice_indices(len(row), size - i, "center")
        series.extend(row[s:e])
        info.append({"row_index": r, "slice_start_col": s, "slice_end_col": e})
    return series, sum(series), info


def kececi_binomial_staircase(triangle: List[List[int]], size: int, start_row: int, alignment: str) -> Tuple[List[int], int, List[Dict]]:
    """Select a staircase (right triangle) region."""
    return kececi_binomial_triangle(triangle, size, start_row, alignment)


def kececi_binomial_trapezoid(triangle: List[List[int]], size: int, start_row: int, alignment: str) -> Tuple[List[int], int, List[Dict]]:
    """Select a trapezoid region."""
    if size < 1 or start_row < 0 or start_row + size > len(triangle):
        raise ValueError("Invalid trapezoid parameters.")
    
    series, info = [], []
    for offset in range(size):
        r = start_row + offset
        row = triangle[r]
        width = size + offset
        s, e = _get_slice_indices(len(row), min(width, len(row)), alignment)
        series.extend(row[s:e])
        info.append({"row_index": r, "slice_start_col": s, "slice_end_col": e})
    if not series:
        raise ValueError("Trapezoid could not be formed.")
    return series, sum(series), info


def kececi_binomial_zigzag(triangle: List[List[int]], size: int, start_row: int, alignment: str) -> Tuple[List[int], int, List[Dict]]:
    """Select a zigzag region (alternating direction per row)."""
    if size < 1 or start_row < 0 or start_row + size > len(triangle):
        raise ValueError("Invalid zigzag parameters.")
    
    series, info = [], []
    for i in range(size):
        r = start_row + i
        row = triangle[r]
        elements = min(i + 1, len(row))
        s, e = _get_slice_indices(len(row), elements, alignment)
        segment = row[s:e]
        if i % 2 == 1:
            segment = segment[::-1]
        series.extend(segment)
        info.append({"row_index": r, "slice_start_col": s, "slice_end_col": e})
    return series, sum(series), info


def kececi_binomial_cross(triangle: List[List[int]], size: int, start_row: int, alignment: str) -> Tuple[List[int], int, List[Dict]]:
    """Select a cross-shaped region."""
    height = 2 * size - 1
    if size < 1 or start_row < 0 or start_row + height > len(triangle):
        raise ValueError("Invalid cross parameters.")
    
    series, info = [], []
    mid = start_row + size - 1
    
    for i in range(height):
        r = start_row + i
        row = triangle[r]
        if alignment == "center":
            center = len(row) // 2
        elif alignment == "left":
            center = size - 1
        else:  # right
            center = len(row) - size
        
        if not (0 <= center < len(row)):
            continue
        
        if r == mid:
            s, e = max(0, center - size + 1), min(len(row), center + size)
            series.extend(row[s:e])
            for c in range(s, e):
                info.append({"row_index": r, "slice_start_col": c, "slice_end_col": c + 1})
        else:
            series.append(row[center])
            info.append({"row_index": r, "slice_start_col": center, "slice_end_col": center + 1})
    return series, sum(series), info


def kececi_nested_square(triangle: List[List[int]], outer_size: int, inner_size: int, start_row: int, alignment: str) -> Tuple:
    """
    Select nested squares: outer square containing a smaller inner square.
    Ana karenin içinde daha küçük bir kare oluşturur.
    """
    if inner_size > outer_size:
        raise ValueError("Inner square must be <= outer square.")
    
    # ✅ İç çağrılarda da 'size' parametresi kullanıldığından emin olun
    outer_series, outer_total, outer_info = kececi_binomial_square(triangle, outer_size, start_row, alignment)
    
    inner_start = start_row + (outer_size - inner_size) // 2
    
    inner_series, inner_total, inner_info = kececi_binomial_square(triangle, inner_size, inner_start, alignment)
    
    return outer_series, outer_total, outer_info, inner_series, inner_total, inner_info


# =============================================================================
# 4. NARAYANA REGION SELECTOR
# =============================================================================
def kececi_narayana_shape(triangle: List[List[int]], shape_type: str, size: int, start_row: int, alignment: str, width: Optional[int] = None) -> Tuple[List[int], int, List[Dict]]:
    """
    Select geometric regions from Narayana triangle.
    Narayana üçgeni için şekil seçici.
    Binomial fonksiyonlarıyla aynı dönüş formatını kullanır.
    """
    shape_type = shape_type.lower().strip()
    valid = {"triangle", "square", "rectangle", "diamond", "polygon"}
    if shape_type not in valid:
        raise ValueError(f"shape_type must be one of: {', '.join(valid)}")
    if size < 1 or start_row < 0:
        raise ValueError("Invalid parameters.")
    
    series, info = [], []
    
    def _slice(row: List[int], count: int, align: str) -> Tuple[int, int]:
        return _get_slice_indices(len(row), min(count, len(row)), align)
    
    if shape_type == "triangle":
        if start_row + size > len(triangle):
            raise ValueError("Triangle exceeds bounds.")
        for i in range(size):
            r = start_row + i
            s, e = _slice(triangle[r], i + 1, alignment)
            series.extend(triangle[r][s:e])
            info.append({"row_index": r, "slice_start_col": s, "slice_end_col": e})
    
    elif shape_type == "square":
        if start_row + size > len(triangle):
            raise ValueError("Square exceeds bounds.")
        for i in range(size):
            r = start_row + i
            s, e = _slice(triangle[r], size, alignment)
            series.extend(triangle[r][s:e])
            info.append({"row_index": r, "slice_start_col": s, "slice_end_col": e})
    
    elif shape_type == "rectangle":
        w = width or size
        if w < 1 or start_row + size > len(triangle):
            raise ValueError("Invalid rectangle parameters.")
        for i in range(size):
            r = start_row + i
            s, e = _slice(triangle[r], w, alignment)
            series.extend(triangle[r][s:e])
            info.append({"row_index": r, "slice_start_col": s, "slice_end_col": e})
    
    elif shape_type == "diamond":
        if alignment != "center":
            raise ValueError("Diamond requires 'center' alignment.")
        height = 2 * size - 1
        if start_row + height > len(triangle):
            raise ValueError("Diamond exceeds bounds.")
        for i in range(size):
            r = start_row + i
            s, e = _slice(triangle[r], i + 1, "center")
            series.extend(triangle[r][s:e])
            info.append({"row_index": r, "slice_start_col": s, "slice_end_col": e})
        for i in range(1, size):
            r = start_row + size - 1 + i
            s, e = _slice(triangle[r], size - i, "center")
            series.extend(triangle[r][s:e])
            info.append({"row_index": r, "slice_start_col": s, "slice_end_col": e})
    
    elif shape_type == "polygon":
        w = width or size
        if w < 3 or start_row + size > len(triangle):
            raise ValueError("Invalid polygon parameters.")
        for i in range(size):
            r = start_row + i
            s, e = _slice(triangle[r], w, "center")
            series.extend(triangle[r][s:e])
            info.append({"row_index": r, "slice_start_col": s, "slice_end_col": e})
    
    return series, sum(series), info


# =============================================================================
# 5. VISUALIZATION HELPERS
# =============================================================================
def draw_shape_on_axis(ax, x: float, y: float, shape: str, radius: float, face_color: str, edge_color: str, alpha: float = 0.9):
    """Draw a geometric shape at given coordinates."""
    if shape == "hexagon":
        # ✅ radius= keyword argument olarak geçmeli
        ax.add_patch(RegularPolygon((x, y), numVertices=6, radius=radius, facecolor=face_color, edgecolor=edge_color, alpha=alpha))
    elif shape == "square":
        side = radius * np.sqrt(2)
        ax.add_patch(Rectangle((x - side/2, y - side/2), side, side, facecolor=face_color, edgecolor=edge_color, alpha=alpha))
    elif shape == "circle":
        ax.add_patch(Circle((x, y), radius=radius, facecolor=face_color, edgecolor=edge_color, alpha=alpha))
    elif shape == "triangle":
        pts = [(x, y + radius), (x - radius*np.sqrt(3)/2, y - radius/2), (x + radius*np.sqrt(3)/2, y - radius/2)]
        ax.add_patch(Polygon(pts, closed=True, facecolor=face_color, edgecolor=edge_color, alpha=alpha))
    else:
        ax.add_patch(RegularPolygon((x, y), numVertices=6, radius=radius, facecolor=face_color, edgecolor=edge_color, alpha=alpha))


# =============================================================================
# 6. MAIN VISUALIZATION ENGINE
# =============================================================================
def draw_kececi_region(triangle_data: List[List[int]], num_rows: int, region_size: int, 
                       start_row_0based: int, region_type: str = "square", 
                       shape_to_draw: str = "hexagon", alignment: str = "left",
                       is_filled: bool = True, show_values: bool = True,
                       triangle_source: str = "binomial", narayana_shape_type: Optional[str] = None,
                       narayana_width: Optional[int] = None, show_plot: bool = True,
                       fig_ax: Optional[Tuple[plt.Figure, plt.Axes]] = None) -> Tuple[Optional[plt.Figure], Optional[plt.Axes], List[int], List[Dict], int]:
    """
    Unified visualization engine for Binomial and Narayana triangles.
    
    Returns:
        tuple: (fig, ax, series_data, selected_indices_info, total_value)

    Birleştirilmiş görselleştirici: Hem Binomial hem Narayana üçgenlerini
    aynı grafiksel yeteneklerle (altıgen/kare/daire/üçgen, renklendirme, 
    kenarlık vurgulama) çizer.
    """
    if num_rows < 1:
        raise ValueError("Number of rows must be at least 1.")
    
    # Select region
    try:
        if triangle_source == "narayana":
            series_data, total_value, selected_indices_info = kececi_narayana_shape(
                triangle_data, narayana_shape_type or region_type, region_size, 
                start_row_0based, alignment, narayana_width)
            region_label = f"Narayana-{narayana_shape_type or region_type}".title()
            symbol = "◆"
        else:
            selectors = {
                "square": kececi_binomial_square, "triangle": kececi_binomial_triangle,
                "diamond": kececi_binomial_diamond, "staircase": kececi_binomial_staircase,
                "trapezoid": kececi_binomial_trapezoid, "zigzag": kececi_binomial_zigzag,
                "cross": kececi_binomial_cross
            }
            if region_type == "nested":
                outer, _, outer_info, inner, _, inner_info = kececi_nested_square(
                    triangle_data, region_size, region_size//2, start_row_0based, alignment)
                series_data = outer + inner
                selected_indices_info = outer_info + inner_info
                total_value = sum(series_data)
                region_label = "Nested-İç İçe"
                symbol = "◫"
            elif region_type in selectors:
                series_data, total_value, selected_indices_info = selectors[region_type](
                    triangle_data, region_size, start_row_0based, alignment)
                region_label = region_type.capitalize()
                symbol = {"square": "■", "triangle": "▲", "diamond": "◆", "cross": "✚"}.get(region_type, "●")
            else:
                raise ValueError(f"Unsupported region type: {region_type}")
    except ValueError as e:
        print(f"❌ Selection error: {e}")
        return None, None, [], [], 0
    
    print(f"📊 Keçeci {triangle_source.title()} {region_label} ({alignment}): Total = {total_value:,} | Elements = {len(series_data)}")
    
    # Grid coordinates for hexagonal layout
    centers = [(c - r/2, -r * np.sqrt(3)/2) for r in range(num_rows) for c in range(r+1)]
    row_offsets = [sum(range(r+1)) for r in range(num_rows)]
    
    # Track highlighted cells
    highlighted = set()
    for info in selected_indices_info:
        r, s, e = info["row_index"], info["slice_start_col"], info["slice_end_col"]
        if 0 <= r < num_rows:
            base = row_offsets[r]
            highlighted.update(base + c for c in range(s, e))
    
    # Setup figure
    if fig_ax is None:
        fig, ax = plt.subplots(figsize=(max(6, num_rows), max(6, num_rows * 0.8)))
    else:
        fig, ax = fig_ax
    ax.clear()
    ax.set_aspect("equal")
    ax.axis("off")
    
    cmap = plt.colormaps["tab20"]
    colors = cmap(np.linspace(0, 1, max(2, num_rows)))
    radius = 0.5
    
    # Draw all cells
    global_idx = 0
    for r in range(num_rows):
        for c in range(r + 1):
            if global_idx >= len(centers):
                break
            x, y = centers[global_idx]
            is_selected = global_idx in highlighted
            color = "gold" if is_selected and is_filled else colors[min(r, len(colors)-1)]
            
            draw_shape_on_axis(ax, x, y, shape_to_draw, radius, color, "black")
            
            if show_values and r < len(triangle_data) and c < len(triangle_data[r]):
                ax.text(x, y, str(triangle_data[r][c]), ha="center", va="center", 
                       fontsize=max(4, 9 - num_rows//6), color="black")
            global_idx += 1
    
    # Axis limits
    pad = 0.6
    ax.set_xlim(-num_rows/2 - pad, num_rows/2 + pad)
    ax.set_ylim(-num_rows * np.sqrt(3)/2 - pad, pad)
    
    # Title
    align_map = {"left": "Left", "right": "Right", "center": "Centered"}
    fill_text = "Filled" if is_filled else "Outlined"
    src = "Narayana" if triangle_source == "narayana" else "Binomial"
    ax.set_title(f"{align_map.get(alignment, alignment)} {fill_text} Keçeci {src} {region_label}\n"
                f"{symbol}{region_size} from row {start_row_0based+1} / {num_rows} Rows\n"
                f"Python {PYTHON_VERSION} | {TIMESTAMP}", fontsize=10, fontweight="bold")
    
    if fig_ax is None:
        plt.tight_layout()
    
    # Console reports (only for small triangles)
    if series_data and num_rows <= 25:
        print_console_reports(triangle_data, series_data, selected_indices_info, 
                              triangle_source, region_label, num_rows)
    
    if show_plot and fig_ax is None:
        plt.show()
    
    return fig, ax, series_data, selected_indices_info, total_value


def print_console_reports(triangle: List[List[int]], series: List[int], indices: List[Dict], 
                          source: str, label: str, num_rows: int):
    """Print triangle matrix and statistics to console."""
    # Matrix with highlights
    highlight_set = {(info["row_index"], c) for info in indices for c in range(info["slice_start_col"], info["slice_end_col"])}
    print_triangle_matrix(triangle, highlight_set, f"{source.title()} Triangle ({num_rows} rows)")
    
    # Statistics
    stats = calculate_region_statistics(series, label)
    print_detailed_report(series, indices, source, label, stats)
    
    # Patterns
    patterns = detect_patterns(series)
    if patterns:
        print("🔍 Pattern Detection:")
        for p in patterns:
            print(f"   {p}")
        print()


# =============================================================================
# 7. CONSOLE OUTPUT UTILITIES
# =============================================================================
def print_triangle_matrix(triangle: List[List[int]], highlight: Optional[set] = None, title: str = "Matrix"):
    """
    Print triangle as formatted ASCII matrix with optional highlighting.
    Üçgen verisini terminalde formatlı matris olarak yazdırır.
    highlight_indices: vurgulanacak (row, col) tuple'ları set'i
    """
    print(f"\n{'='*60}\n  {title}\n{'='*60}")
    if not triangle:
        print("  (empty)")
        return
    max_w = len(str(max(max(row) for row in triangle))) + 2
    for r, row in enumerate(triangle):
        indent = " " * ((len(triangle) - r) * (max_w // 2))
        print(indent, end="")
        for c, val in enumerate(row):
            hl = highlight and (r, c) in highlight
            if hl:
                print(f"\033[1;33m[{val:>{max_w-2}}]\033[0m", end="")
            else:
                print(f" {val:>{max_w-2}} ", end="")
        print()
    print(f"{'='*60}\n")


def calculate_region_statistics(series: List[int], label: str = "Region") -> Dict[str, Any]:
    """Calculate comprehensive statistics for a data series."""
    if not series:
        return {}
    s = {
        "count": len(series), "sum": sum(series), "min": min(series), "max": max(series),
        "mean": mean(series), "median": median(series),
        "variance": variance(series) if len(series) > 1 else 0,
        "std_dev": stdev(series) if len(series) > 1 else 0,
        "unique": len(set(series)), "most_common": Counter(series).most_common(3)
    }
    s["range"] = s["max"] - s["min"]
    s["cv"] = (s["std_dev"] / s["mean"] * 100) if s["mean"] != 0 else 0
    s["even"] = sum(1 for x in series if x % 2 == 0)
    s["odd"] = s["count"] - s["even"]
    return s


def print_detailed_report(series: List[int], indices: List[Dict], source: str, label: str, stats: Dict):
    """Print detailed analysis report to console."""
    print(f"\n📊 DETAILED ANALYSIS REPORT\n{'─'*60}")
    print(f"\n🔹 Region: {label.upper()} | Source: {source.title()}")
    print(f"   Elements: {stats['count']} | Sum: {stats['sum']:,}")
    
    print(f"\n🔹 Descriptive Statistics:")
    print(f"   {'Metric':<15} {'Value':>15}\n   {'─'*30}")
    for k, v in [("Min", stats["min"]), ("Max", stats["max"]), ("Mean", f"{stats['mean']:.4f}"),
                 ("Median", f"{stats['median']:.4f}"), ("Std Dev", f"{stats['std_dev']:.4f}"),
                 ("Variance", f"{stats['variance']:.4f}"), ("CV (%)", f"{stats['cv']:.2f}"),
                 ("Range", stats["range"]), ("Unique", stats["unique"])]:
        print(f"   {k:<15} {v:>15}")
    
    print(f"\n🔹 Parity: Even {stats['even']} ({stats['even']/len(series)*100:.1f}%) | Odd {stats['odd']}")
    
    if stats["most_common"]:
        print(f"\n🔹 Most Common:")
        for val, freq in stats["most_common"]:
            print(f"   {val:,} ×{freq}")
    
    print(f"\n🔹 Selected Cells (first 20):")
    print(f"   {'Row':>4} {'Col':>4} {'Value':>10}\n   {'─'*20}")
    for i, info in enumerate(indices[:20]):
        r = info["row_index"] + 1
        for c in range(info["slice_start_col"]+1, info["slice_end_col"]+1):
            val = series[i] if i < len(series) else ""
            print(f"   {r:>4} {c:>4} {val:>10,}")
    if len(indices) > 20:
        print(f"   ... +{len(indices)-20} more")
    
    print(f"\n🔹 Series Preview: {series[:30]}{'...' if len(series)>30 else ''}")
    print(f"{'─'*60}\n")


def detect_patterns(series: List[int]) -> List[str]:
    """Detect mathematical patterns in the series."""
    patterns = []
    if not series:
        return patterns
    if series == series[::-1]:
        patterns.append("✓ Palindromic sequence")
    if len(series) >= 2:
        if all(series[i] <= series[i+1] for i in range(len(series)-1)):
            patterns.append("✓ Non-decreasing")
        elif all(series[i] >= series[i+1] for i in range(len(series)-1)):
            patterns.append("✓ Non-increasing")
    primes = [x for x in series if x > 1 and all(x % d for d in range(2, int(x**0.5)+1))]
    if primes:
        patterns.append(f"✓ Contains {len(primes)} prime(s): {primes[:4]}{'...' if len(primes)>4 else ''}")
    return patterns


# =============================================================================
# 8. EXPORT FUNCTIONS
# =============================================================================
def export_to_csv(series: List[int], indices: List[Dict], filepath: str = "kececi_output.csv") -> bool:
    """
    Export selected data to CSV file.
    Seçili bölge verisini CSV dosyasına aktarır.
    Args:
        series_data: Seçilen hücrelerin değer listesi
        selected_indices: Her hücre için {row_index, slice_start_col, slice_end_col} bilgisi
        filepath: Çıktı dosya yolu
    """
    try:
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f)
            w.writerow(["index", "row_1based", "col_1based", "value"])
            idx = 0
            for info in indices:
                r = info["row_index"] + 1
                for c in range(info["slice_start_col"]+1, info["slice_end_col"]+1):
                    w.writerow([idx, r, c, series[idx]])
                    idx += 1
        print(f"✅ CSV exported: {filepath} ({len(series)} records)")
        return True
    except Exception as e:
        print(f"❌ CSV export failed: {e}")
        return False


def export_to_json(data: Dict, filepath: str = "kececi_output.json") -> bool:
    """Export analysis results to JSON file.
    Tüm analiz sonuçlarını JSON formatında kaydeder.
    
    Args:
        export_data: Dışa aktarılacak tüm verileri içeren dictionary
        filepath: Çıktı dosya yolu
    """
    try:
        def clean(obj):
            if isinstance(obj, (np.integer, np.floating)):
                return float(obj)
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            if isinstance(obj, dict):
                return {k: clean(v) for k, v in obj.items()}
            if isinstance(obj, (list, tuple)):
                return [clean(i) for i in obj]
            return obj
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(clean(data), f, indent=2, ensure_ascii=False)
        print(f"✅ JSON exported: {filepath}")
        return True
    except Exception as e:
        print(f"❌ JSON export failed: {e}")
        return False

# ========================================================
# HIGH-LEVEL REPORT GENERATOR (PUBLIC API)
# ========================================================

def generate_full_report(params: Dict[str, Any]) -> Dict[str, Optional[str]]:
    """
    Generate complete analysis: plot + CSV + JSON + console output.
    
    Args:
        params: Dictionary with keys:
            - triangle_source: "binomial" or "narayana"
            - num_rows: int
            - region_size: int
            - start_row_0idx: int (0-based)
            - region_type: str (square, triangle, diamond, etc.)
            - shape_type: str (hexagon, square, circle, triangle)
            - alignment: str (left, right, center)
            - is_filled: bool
            - show_numbers: bool
            - save_path: Optional[str] for PNG
            - csv_path: Optional[str] for CSV export
            - json_path: Optional[str] for JSON export
    
    Returns:
        Dictionary with generated file paths:
        {
            "plot": "path/to/file.png" or None,
            "csv": "path/to/file.csv" or None,
            "json": "path/to/file.json" or None,
            "series": List[int],  # The selected values
            "statistics": Dict,   # From calculate_region_statistics
        }
    """
    results = {"plot": None, "csv": None, "json": None, "series": None, "statistics": None}
    
    try:
        # 1. Generate triangle
        if params["triangle_source"] == "narayana":
            triangle = generate_narayana_triangle(params["num_rows"])
        else:
            triangle = generate_binomial_triangle(params["num_rows"])
        
        # 2. Select region & visualize
        result = draw_kececi_region(
            triangle_data=triangle,
            num_rows=params["num_rows"],
            region_size=params["region_size"],
            start_row_0based=params["start_row_0idx"],
            region_type=params["region_type"],
            shape_to_draw=params.get("shape_type", "hexagon"),
            alignment=params.get("alignment", "left"),
            is_filled=params.get("is_filled", True),
            show_values=params.get("show_numbers", True),
            triangle_source=params["triangle_source"],
            narayana_shape_type=params.get("narayana_shape_type"),
            narayana_width=params.get("narayana_width"),
            show_plot=False  # Don't auto-show; user controls display
        )
        
        if result[0] is None:
            raise RuntimeError("Visualization failed")
        
        fig, ax, series_data, indices, total = result
        results["series"] = series_data
        results["statistics"] = calculate_region_statistics(series_data, params.get("region_label", "Region"))
        
        # 3. Save plot if requested
        if params.get("save_path"):
            fig.savefig(params["save_path"], dpi=200, bbox_inches="tight")
            results["plot"] = params["save_path"]
            print(f"✅ Plot saved: {params['save_path']}")
        
        # 4. Export CSV if requested
        if params.get("csv_path"):
            if export_to_csv(series_data, indices, params["csv_path"]):
                results["csv"] = params["csv_path"]
        
        # 5. Export JSON if requested
        if params.get("json_path"):
            payload = {
                "metadata": {
                    "version": __version__, "timestamp": TIMESTAMP, "python": PYTHON_VERSION,
                    "source": params["triangle_source"], "region": params.get("region_label"),
                    "size": params["region_size"], "start_row": params["start_row_0idx"] + 1,
                    "alignment": params.get("alignment")
                },
                "data": {"values": series_data, "sum": total, "count": len(series_data), "cells": indices},
                "statistics": results["statistics"],
                "config": {k: v for k, v in params.items() if k not in ("save_path", "csv_path", "json_path")}
            }
            if export_to_json(payload, params["json_path"]):
                results["json"] = params["json_path"]
        
        # 6. Optional: show plot
        if params.get("show_plot", True):
            plt.show()
        
        return results
        
    except Exception as e:
        print(f"❌ Report generation failed: {e}")
        return results


# =============================================================================
# 9. INTERACTIVE PARAMETER COLLECTION
# =============================================================================
def get_user_parameters() -> Optional[Dict]:
    """
    Collect visualization parameters via interactive CLI.
    Tek bir fonksiyon altında hem Keçeci Binomial Shapes 
    hem de Keçeci-Narayana Shapes için parametre toplar.
    Tüm çıktı anahtarları tutarlıdır: triangle_source, num_rows, region_type, vb.
    """
    print("="*60 + "\n   KEÇECI BINOMIAL & NARAYANA SHAPES VISUALIZER\n" + "="*60)
    
    try:
        # System selection
        sys_choice = input("\n1: Binomial (Pascal)  2: Narayana (default:1): ").strip() or "1"
        source = "narayana" if sys_choice == "2" else "binomial"
        print(f"✓ Selected: {'Narayana' if source=='narayana' else 'Binomial/Pascal'} Triangle")
        
        # Rows
        num_rows = int(input("Number of rows (min:1): ").strip())
        if num_rows < 1:
            raise ValueError("Rows must be >= 1")
        
        # Region type
        if source == "binomial":
            choices = input("Shape: 1:Square 2:Triangle 3:Diamond 4:Staircase 5:Trapezoid 6:Zigzag 7:Cross 8:Nested (1): ").strip() or "1"
            r_map = {"1":"square","2":"triangle","3":"diamond","4":"staircase","5":"trapezoid","6":"zigzag","7":"cross","8":"nested"}
            r_type = r_map.get(choices, "square")
            r_label = {"square":"Square-Kare","triangle":"Triangle-Üçgen","diamond":"Diamond-Elmas",
                      "staircase":"Staircase-Merdiven","trapezoid":"Trapezoid-Yamuk","zigzag":"Zigzag-Zikzak",
                      "cross":"Cross-Çapraz","nested":"Nested-İç İçe"}.get(r_type, "Square-Kare")
            n_shape, n_width = None, None
        else:
            choices = input("Shape: 1:Triangle 2:Square 3:Rectangle 4:Diamond 5:Polygon (1): ").strip() or "1"
            r_map = {"1":"triangle","2":"square","3":"rectangle","4":"diamond","5":"polygon"}
            r_type = r_map.get(choices, "triangle")
            r_label = {"triangle":"Triangle-Üçgen","square":"Square-Kare","rectangle":"Rectangle-Dikdörtgen",
                      "diamond":"Diamond-Elmas","polygon":"Polygon-Çokgen"}.get(r_type, "Triangle-Üçgen")
            n_shape = r_type
            n_width = int(input(f"Width for {r_label}: ").strip()) if r_type in ("rectangle","polygon") else None
        
        # Size validation
        max_sz = (num_rows+1)//2 if r_type in ("diamond","cross") else num_rows
        size = int(input(f"Size (1-{max_sz}): ").strip())
        if not (1 <= size <= max_sz):
            raise ValueError(f"Size must be 1-{max_sz}")
        
        # Start row
        height = 2*size-1 if r_type in ("diamond","cross") else size
        max_start = num_rows - height
        start = int(input(f"Start row (1-{max_start+1}): ").strip()) - 1
        if not (0 <= start <= max_start):
            raise ValueError(f"Start must be 1-{max_start+1}")
        
        # Alignment
        align = "center" if r_type == "diamond" else {"1":"left","2":"right","3":"center"}.get(input("Align 1:L 2:R 3:C (1): ").strip() or "1", "left")
        
        # Visual options
        vis = {"1":"hexagon","2":"square","3":"circle","4":"triangle"}.get(input("Visual 1:Hex 2:Sq 3:Cir 4:Tri (1): ").strip() or "1", "hexagon")
        fill = input("Fill? 1:Y 2:N (1): ").strip() != "2"
        show_vals = input("Show numbers? 1:Y 2:N (1): ").strip() != "2"
        
        # Save options
        save_plot = input("Save PNG? 1:Y 2:N (2): ").strip() == "1"
        save_path = f"kececi_{source}_{r_type}_{size}.png" if save_plot else None
        
        export_choice = input("Export: 1:CSV 2:JSON 3:Both 4:None (4): ").strip() or "4"
        base = f"kececi_{source}_{r_type}_{size}"
        
        return {
            "triangle_source": source, "num_rows": num_rows, "region_size": size,
            "start_row_0idx": start, "region_type": r_type, "region_label": r_label,
            "narayana_shape_type": n_shape, "narayana_width": n_width,
            "shape_type": vis, "alignment": align, "is_filled": fill,
            "show_numbers": show_vals, "save_plot": save_plot, "save_path": save_path,
            "export_csv": export_choice in ("1","3"), "export_json": export_choice in ("2","3"),
            "csv_path": f"{base}.csv" if export_choice in ("1","3") else None,
            "json_path": f"{base}.json" if export_choice in ("2","3") else None,
        }
        
    except (ValueError, KeyboardInterrupt) as e:
        print(f"\n❌ {'Cancelled' if isinstance(e, KeyboardInterrupt) else 'Invalid input'}")
        return None
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None


# =============================================================================
# 10. MAIN EXECUTION
# =============================================================================
if __name__ == "__main__":
    print(f"\n🔷 Keçeci Visualizer v{__version__} | Python {PYTHON_VERSION} | {TIMESTAMP}\n")
    
    params = get_user_parameters()
    if not params:
        print("⛔ Exiting.")
        exit(1)
    
    # Generate triangle
    triangle = generate_narayana_triangle(params["num_rows"]) if params["triangle_source"]=="narayana" else generate_binomial_triangle(params["num_rows"])
    
    print(f"\n🔄 Generating {params['region_type'].upper()}...")
    
    # Visualize (returns 5 values)
    result = draw_kececi_region(
        triangle_data=triangle, num_rows=params["num_rows"], region_size=params["region_size"],
        start_row_0based=params["start_row_0idx"], region_type=params["region_type"],
        shape_to_draw=params["shape_type"], alignment=params["alignment"],
        is_filled=params["is_filled"], show_values=params["show_numbers"],
        triangle_source=params["triangle_source"], narayana_shape_type=params.get("narayana_shape_type"),
        narayana_width=params.get("narayana_width"), show_plot=False
    )
    
    if result[0] is None:
        print("❌ Visualization failed.")
        exit(1)
    
    fig, ax, series_data, indices, total = result
    
    # Export if requested
    if params.get("export_csv") or params.get("export_json"):
        print("\n📦 Exporting...")
        stats = calculate_region_statistics(series_data, params["region_label"])
        patterns = detect_patterns(series_data)
        
        if params.get("export_csv") and params.get("csv_path"):
            export_to_csv(series_data, indices, params["csv_path"])
        
        if params.get("export_json") and params.get("json_path"):
            payload = {
                "metadata": {"version": __version__, "timestamp": TIMESTAMP, "python": PYTHON_VERSION,
                           "source": params["triangle_source"], "region": params["region_label"],
                           "size": params["region_size"], "start_row": params["start_row_0idx"]+1,
                           "alignment": params["alignment"]},
                "data": {"values": series_data, "sum": total, "count": len(series_data), "cells": indices},
                "statistics": stats, "patterns": patterns,
                "config": {"shape": params["shape_type"], "filled": params["is_filled"], "show_values": params["show_numbers"]}
            }
            export_to_json(payload, params["json_path"])
    
    # Show plot
    if fig:
        if params.get("save_plot") and params.get("save_path"):
            plt.savefig(params["save_path"], dpi=200, bbox_inches="tight")
            print(f"✅ Saved: {params['save_path']}")
        plt.show()
        print("✅ Done.")
