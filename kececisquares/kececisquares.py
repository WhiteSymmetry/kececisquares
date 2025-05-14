# kececisquares.py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon, Rectangle, Circle, Polygon
import datetime
import platform
import math # For math.ceil

# Python version and date information (can be used by the main script if needed)
PYTHON_VERSION_INFO = platform.python_version()
CURRENT_DATE_INFO = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def generate_binomial_triangle(num_rows):
    """Generates Pascal's (Binomial) Triangle."""
    binomial_triangle_data = []
    for i in range(num_rows):
        row_data = [1]
        if i > 0:
            if binomial_triangle_data[i-1]: # Ensure previous row exists and is not empty
                for j in range(1, i):
                    row_data.append(binomial_triangle_data[i-1][j-1] + binomial_triangle_data[i-1][j])
            row_data.append(1)
        elif i == 0 and num_rows == 1: # Special case for single row triangle
            pass # row_data is already [1]
        binomial_triangle_data.append(row_data)
    return binomial_triangle_data

def kececi_binomial_square(binomial_triangle_data, square_size, start_row_index, alignment_type):
    """
    Selects the 'Keçeci Binomial Square' series, calculates its sum, and returns indices of selected elements.
    (Note: "Keçeci" is a proper name, kept as is for consistency with the original concept.)
    """
    series_data = []
    selected_indices_info = [] # Stores dicts: {"row_index": ..., "slice_start_col": ..., "slice_end_col": ...}

    # Validate that the square can actually be formed with the given parameters
    # This basic validation should be enhanced if this function is called directly without pre-validation
    if start_row_index + square_size > len(binomial_triangle_data):
        raise ValueError(
            f"Square (size {square_size} starting at row {start_row_index+1}) "
            f"exceeds the triangle's {len(binomial_triangle_data)} rows."
        )

    for i in range(square_size):
        current_row_idx = start_row_index + i
        current_row_elements = binomial_triangle_data[current_row_idx]
        num_elements_in_current_row = len(current_row_elements)

        if square_size > num_elements_in_current_row :
             raise ValueError(
                f"Square (size {square_size}) cannot fit in row {current_row_idx+1} "
                f"which has only {num_elements_in_current_row} elements."
            )

        actual_start_col_in_row = 0
        if alignment_type == "left":
            actual_start_col_in_row = 0
        elif alignment_type == "right":
            actual_start_col_in_row = num_elements_in_current_row - square_size
        elif alignment_type == "center":
            actual_start_col_in_row = (num_elements_in_current_row - square_size) // 2
        else:
            raise ValueError(f"Invalid alignment_type: {alignment_type}. Must be 'left', 'right', or 'center'.")
        
        if actual_start_col_in_row < 0: # Should not happen with prior validation but good to have
            raise ValueError(
                f"Calculated start column {actual_start_col_in_row} is invalid for row {current_row_idx+1} "
                f"with {num_elements_in_current_row} elements and square size {square_size}."
            )

        row_series_segment = current_row_elements[actual_start_col_in_row : actual_start_col_in_row + square_size]
        series_data.extend(row_series_segment)
        selected_indices_info.append({
            "row_index": current_row_idx,
            "slice_start_col": actual_start_col_in_row,
            "slice_end_col": actual_start_col_in_row + square_size
        })

    total_value = sum(series_data)
    return series_data, total_value, selected_indices_info

def draw_shape_on_axis(ax_handle, x_coord, y_coord, shape_name, item_radius, face_color, edge_color, alpha_val=0.9):
    """A general function to draw different shapes."""
    shape_object = None
    if shape_name == "hexagon":
        shape_object = RegularPolygon((x_coord, y_coord), numVertices=6, radius=item_radius,
                                      facecolor=face_color, edgecolor=edge_color, alpha=alpha_val)
    elif shape_name == "square":
        side_length = item_radius * np.sqrt(2)
        shape_object = Rectangle((x_coord - side_length / 2, y_coord - side_length / 2),
                                 width=side_length, height=side_length,
                                 facecolor=face_color, edgecolor=edge_color, alpha=alpha_val)
    elif shape_name == "circle":
        circle_radius_val = item_radius
        shape_object = Circle((x_coord, y_coord), radius=circle_radius_val,
                              facecolor=face_color, edgecolor=edge_color, alpha=alpha_val)
    elif shape_name == "triangle":
        p1 = [x_coord, y_coord + item_radius]
        p2 = [x_coord - item_radius * np.sqrt(3)/2, y_coord - item_radius/2]
        p3 = [x_coord + item_radius * np.sqrt(3)/2, y_coord - item_radius/2]
        shape_object = Polygon([p1, p2, p3], closed=True,
                               facecolor=face_color, edgecolor=edge_color, alpha=alpha_val)
    else: # Default to hexagon if unknown type
        shape_object = RegularPolygon((x_coord, y_coord), numVertices=6, radius=item_radius,
                                      facecolor=face_color, edgecolor=edge_color, alpha=alpha_val)
    if shape_object:
        ax_handle.add_patch(shape_object)

def draw_kececi_binomial_square(
        num_rows_to_draw, square_region_size, start_row_index_for_square_0based,
        shape_to_draw="hexagon", square_alignment="left",
        is_square_filled=True, color_palette_name="tab20",
        show_plot=True, fig_ax=None, show_values=True): # Added show_plot and fig_ax

    if num_rows_to_draw <= 0: # Changed from == 0 to <= 0
        print("Number of rows to draw must be positive. Minimum is 1.")
        return None, None # Return None if plot cannot be made

    binomial_triangle = generate_binomial_triangle(num_rows_to_draw)
    
    try:
        series, total_value, selected_indices_info = \
            kececi_binomial_square(binomial_triangle, square_region_size, start_row_index_for_square_0based, square_alignment)
    except ValueError as e:
        print(f"Error selecting square region: {e}")
        return None, None


    print(f"Keçeci Binomial Square Series ({square_alignment}): {series}")
    print(f"Keçeci Binomial Square Total Value: {total_value}")
    
    num_colors_for_colormap = max(2, num_rows_to_draw)
    row_colors = plt.colormaps[color_palette_name](np.linspace(0, 1, num_colors_for_colormap))
    
    def calculate_hexagon_centers(num_rows_centers):
        centers_list = []
        for r_idx in range(num_rows_centers):
            for c_idx in range(r_idx + 1):
                x_center = c_idx - r_idx / 2.0
                y_center = -r_idx * np.sqrt(3) / 2.0
                centers_list.append((x_center, y_center))
        return centers_list
    
    if fig_ax is None:
        fig, main_ax = plt.subplots(figsize=(max(6, num_rows_to_draw * 1.0), max(6, num_rows_to_draw * 0.9)))
    else:
        fig, main_ax = fig_ax # Use provided figure and axis
    main_ax.clear() # Clear axis if reused
    main_ax.set_aspect('equal')
    main_ax.axis('off')

    
    item_centers = calculate_hexagon_centers(num_rows_to_draw)
    
    highlighted_item_global_indices = set()
    global_index_offset_per_row = [0] * num_rows_to_draw
    current_global_offset = 0
    for r_idx_offset in range(num_rows_to_draw):
        global_index_offset_per_row[r_idx_offset] = current_global_offset
        current_global_offset += (r_idx_offset + 1)

    for info_dict in selected_indices_info:
        row_idx_in_triangle = info_dict["row_index"]
        slice_start_col_idx = info_dict["slice_start_col"]
        slice_end_col_idx = info_dict["slice_end_col"]
        # Ensure row_idx_in_triangle is within bounds of global_index_offset_per_row
        if 0 <= row_idx_in_triangle < len(global_index_offset_per_row):
            row_start_global_idx = global_index_offset_per_row[row_idx_in_triangle]
            for col_idx_in_row in range(slice_start_col_idx, slice_end_col_idx):
                highlighted_item_global_indices.add(row_start_global_idx + col_idx_in_row)

    highlighted_square_row_column_bounds = {}
    for info_dict in selected_indices_info:
        highlighted_square_row_column_bounds[info_dict["row_index"]] = {
            "start_col": info_dict["slice_start_col"],
            "end_col": info_dict["slice_end_col"]
        }
            
    global_item_counter = 0
    shape_radius = 0.5
    
    for r_idx_triangle in range(num_rows_to_draw):
        for c_idx_triangle in range(r_idx_triangle + 1):
            if global_item_counter >= len(item_centers): # Safety break
                print(f"Warning: global_item_counter ({global_item_counter}) exceeded item_centers length ({len(item_centers)}).")
                break
            x_pos, y_pos = item_centers[global_item_counter]
            default_item_color = row_colors[min(r_idx_triangle, len(row_colors)-1)]
            face_color_for_item = default_item_color
            
            is_item_in_highlighted_square = global_item_counter in highlighted_item_global_indices

            if is_item_in_highlighted_square:
                if is_square_filled:
                    face_color_for_item = 'gold'
                else: # Outline mode
                    is_border_item = False
                    bounds_for_current_row = highlighted_square_row_column_bounds.get(r_idx_triangle)
                    
                    if bounds_for_current_row:
                        is_top_row_of_square = (r_idx_triangle == start_row_index_for_square_0based)
                        is_bottom_row_of_square = (r_idx_triangle == start_row_index_for_square_0based + square_region_size - 1)
                        is_left_edge_item = (c_idx_triangle == bounds_for_current_row["start_col"])
                        is_right_edge_item = (c_idx_triangle == bounds_for_current_row["end_col"] - 1)

                        if is_top_row_of_square or is_bottom_row_of_square or \
                           is_left_edge_item or is_right_edge_item:
                            is_border_item = True
                        
                        if is_border_item:
                            face_color_for_item = 'gold'
            
            draw_shape_on_axis(main_ax, x_pos, y_pos, shape_to_draw, item_radius=shape_radius,
                               face_color=face_color_for_item, edge_color='black')
            
            text_font_size = 10
            if num_rows_to_draw > 7: text_font_size = 8
            if num_rows_to_draw > 12: text_font_size = 6
            if num_rows_to_draw > 18: text_font_size = 5
            if shape_to_draw == "triangle" and num_rows_to_draw > 10: text_font_size = max(4, text_font_size-1)

            plt.text(x_pos, y_pos, str(binomial_triangle[r_idx_triangle][c_idx_triangle]),
                     ha='center', va='center', fontsize=text_font_size, color='black')
            global_item_counter += 1
        if global_item_counter >= len(item_centers): # Safety break for outer loop
            break

    plot_padding = 0.5 # Adjusted for better fit
    min_x_lim = -num_rows_to_draw / 2.0 * (shape_radius/0.5) - plot_padding
    max_x_lim = num_rows_to_draw / 2.0 * (shape_radius/0.5) + plot_padding
    min_y_lim = (-num_rows_to_draw +1) * (np.sqrt(3)/2.0) * (shape_radius/0.5) - plot_padding # Adjusted for bottom row
    max_y_lim = 0.0 + shape_radius + plot_padding # Adjusted for top item
    main_ax.set_xlim(min_x_lim, max_x_lim)
    main_ax.set_ylim(min_y_lim, max_y_lim)

    alignment_symbol_map = {"left": "-", "right": "+", "center": ""}
    alignment_symbol = alignment_symbol_map.get(square_alignment, "")
    
    alignment_display_map = {"left": "Left-Aligned", "right": "Right-Aligned", "center": "Centered"}
    fill_display_text = "Filled" if is_square_filled else "Empty (Outlined)"
    
    # Using global version/date info from the module
    plot_title_str = (
        f"{alignment_display_map.get(square_alignment, square_alignment)} and {fill_display_text} Keçeci Binomial Square\n"
        f"{alignment_symbol}{square_region_size}x{square_region_size}$_{{{start_row_index_for_square_0based + 1}}}$ / {num_rows_to_draw} Rows\n"
        f"Python: {PYTHON_VERSION_INFO}, Date: {CURRENT_DATE_INFO}"
    )
    main_ax.set_title(plot_title_str, fontsize=10, fontweight='bold', pad=10)
    
    if fig_ax is None: # Only apply tight_layout if we created the fig/ax here
        plt.tight_layout(pad=1.0)
    
    if show_plot and fig_ax is None : # Only call plt.show() if we created the fig/ax and are asked to show
        plt.show()
    
    return fig, main_ax # Return fig and ax for potential reuse or further manipulation
