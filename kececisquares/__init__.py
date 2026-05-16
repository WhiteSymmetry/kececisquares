### `__init__.py`
# -*- coding: utf-8 -*-
"""
Keçeci Binomial & Keçeci-Narayana Visualizer Package

Provides a unified toolkit for:
- Generating Pascal/Khayyam and Narayana triangles
- Selecting geometric regions (square, triangle, diamond, staircase, etc.)
- Visualizing regions on a hexagonal grid
- Exporting statistical reports (CSV, JSON)
- Interactive CLI parameter collection

"""
from __future__ import annotations

__version__ = "0.1.8"


from .kececisquares import (
    # Triangle generators
    generate_binomial_triangle,
    generate_narayana_triangle,
    
    # Region selectors (Binomial)
    kececi_binomial_square,
    kececi_binomial_triangle,
    kececi_binomial_diamond,
    kececi_binomial_staircase,
    kececi_binomial_trapezoid,
    kececi_binomial_zigzag,
    kececi_binomial_cross,
    kececi_nested_square,
    
    # Region selector (Narayana)
    kececi_narayana_shape,
    
    # Visualization
    draw_kececi_region,
    draw_shape_on_axis,
    
    # Statistics & Reporting
    calculate_region_statistics,
    detect_patterns,
    print_triangle_matrix,        
    print_detailed_report,
    print_console_reports,       
    
    # Export
    export_to_csv,
    export_to_json,
    
    # High-level API
    generate_full_report,         # Public
    get_user_parameters,
)

__all__ = [
    "generate_binomial_triangle",
    "generate_narayana_triangle",
    "kececi_binomial_square",
    "kececi_binomial_triangle", 
    "kececi_binomial_diamond",
    "kececi_binomial_staircase",
    "kececi_binomial_trapezoid",
    "kececi_binomial_zigzag",
    "kececi_binomial_cross",
    "kececi_nested_square",
    "kececi_narayana_shape",
    "draw_kececi_region",
    "draw_shape_on_axis",
    "calculate_region_statistics",
    "detect_patterns",
    "print_triangle_matrix",
    "print_detailed_report",
    "print_console_reports",
    "export_to_csv",
    "export_to_json",
    "generate_full_report",
    "get_user_parameters",
]
