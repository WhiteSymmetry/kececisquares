# kececisquares.py

import datetime
import math
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon, Rectangle, Circle, Polygon
import numpy as np
import platform

# Sürüm ve tarih bilgisi
PYTHON_VERSION_INFO = platform.python_version()
CURRENT_DATE_INFO = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ========================================================
# 1. Temel Üçgen Üretici
# ========================================================
def generate_binomial_triangle(num_rows):
    if num_rows < 1:
        raise ValueError("Number of rows must be at least 1.")
    triangle = []
    for row_index in range(num_rows):
        row = [1]
        if row_index > 0:
            prev_row = triangle[row_index - 1]
            for j in range(1, row_index):
                row.append(prev_row[j - 1] + prev_row[j])
            row.append(1)
        triangle.append(row)
    return triangle

# ========================================================
# 2. Bölge Seçici Fonksiyonlar
# ========================================================

def kececi_binomial_square(binomial_triangle_data, square_size, start_row_index, alignment_type):
    if square_size < 1:
        raise ValueError("Square size must be at least 1.")
    if start_row_index < 0:
        raise ValueError("Start row index must be >= 0.")
    if start_row_index + square_size > len(binomial_triangle_data):
        raise ValueError(f"Square of size {square_size} starting at row {start_row_index} exceeds available rows.")
    
    series_data = []
    selected_indices_info = []
    
    for i in range(square_size):
        current_row_idx = start_row_index + i
        current_row = binomial_triangle_data[current_row_idx]
        row_length = len(current_row)
        
        if square_size > row_length:
            raise ValueError(f"Cannot fit square of size {square_size} in row {current_row_idx + 1}.")
        
        if alignment_type == "left":
            start_col = 0
        elif alignment_type == "right":
            start_col = row_length - square_size
        elif alignment_type == "center":
            start_col = (row_length - square_size) // 2
        else:
            raise ValueError("Invalid alignment. Use 'left', 'right', or 'center'.")
        
        if start_col < 0:
            raise ValueError(f"Invalid start column {start_col} for row {current_row_idx + 1}.")
        
        end_col = start_col + square_size
        segment = current_row[start_col:end_col]
        series_data.extend(segment)
        selected_indices_info.append({
            "row_index": current_row_idx,
            "slice_start_col": start_col,
            "slice_end_col": end_col
        })
    
    total_value = sum(series_data)
    return series_data, total_value, selected_indices_info


def kececi_binomial_triangle(binomial_triangle_data, triangle_size, start_row_index, alignment_type):
    if triangle_size < 1:
        raise ValueError("Triangle size must be at least 1.")
    if start_row_index < 0:
        raise ValueError("Start row index must be >= 0.")
    if start_row_index + triangle_size > len(binomial_triangle_data):
        raise ValueError(f"Triangle of size {triangle_size} starting at row {start_row_index} exceeds available rows.")
    
    series_data = []
    selected_indices_info = []
    
    for i in range(triangle_size):
        current_row_idx = start_row_index + i
        current_row = binomial_triangle_data[current_row_idx]
        row_length = len(current_row)
        elements_to_select = i + 1
        
        if elements_to_select > row_length:
            raise ValueError(f"Cannot select {elements_to_select} elements in row {current_row_idx + 1}.")
        
        if alignment_type == "left":
            start_col = 0
        elif alignment_type == "right":
            start_col = row_length - elements_to_select
        elif alignment_type == "center":
            start_col = (row_length - elements_to_select) // 2
        else:
            raise ValueError("Invalid alignment.")
        
        if start_col < 0:
            raise ValueError(f"Invalid start column {start_col} for row {current_row_idx + 1}.")
        
        end_col = start_col + elements_to_select
        segment = current_row[start_col:end_col]
        series_data.extend(segment)
        selected_indices_info.append({
            "row_index": current_row_idx,
            "slice_start_col": start_col,
            "slice_end_col": end_col
        })
    
    total_value = sum(series_data)
    return series_data, total_value, selected_indices_info


def kececi_binomial_diamond(binomial_triangle_data, diamond_size, start_row_index, alignment_type):
    """
    Gerçek simetrik elmas.
    Sadece center alignment.
    Her satırda merkeze göre simetrik genişler/daralır.
    """
    if diamond_size < 1:
        raise ValueError("Diamond size must be at least 1.")
    if start_row_index < 0:
        raise ValueError("Start row index must be >= 0.")
    
    total_height = 2 * diamond_size - 1
    if start_row_index + total_height > len(binomial_triangle_data):
        raise ValueError(f"Diamond of size {diamond_size} (height {total_height}) starting at row {start_row_index} exceeds available rows.")

    if alignment_type != "center":
        raise ValueError("Diamond only supports 'center' alignment for symmetric shape.")

    series_data = []
    selected_indices_info = []
    
    # Yukarıdan ortaya
    for i in range(diamond_size):
        current_row_idx = start_row_index + i
        current_row = binomial_triangle_data[current_row_idx]
        row_length = len(current_row)
        elements_to_select = i + 1

        if row_length < elements_to_select:
            raise ValueError(f"Row {current_row_idx + 1} too short for diamond segment of size {elements_to_select}.")

        # Merkeze göre simetrik seç
        center = row_length // 2
        half = elements_to_select // 2
        start_col = center - half
        end_col = start_col + elements_to_select

        if start_col < 0 or end_col > row_length:
            raise ValueError(f"Cannot center diamond segment of size {elements_to_select} in row {current_row_idx + 1} with length {row_length}.")

        segment = current_row[start_col:end_col]
        series_data.extend(segment)
        selected_indices_info.append({
            "row_index": current_row_idx,
            "slice_start_col": start_col,
            "slice_end_col": end_col
        })

    # Ortadan aşağıya (orta satır hariç)
    for i in range(1, diamond_size):
        current_row_idx = start_row_index + diamond_size - 1 + i
        current_row = binomial_triangle_data[current_row_idx]
        row_length = len(current_row)
        elements_to_select = diamond_size - i

        if row_length < elements_to_select:
            raise ValueError(f"Row {current_row_idx + 1} too short for diamond segment of size {elements_to_select}.")

        center = row_length // 2
        half = elements_to_select // 2
        start_col = center - half
        end_col = start_col + elements_to_select

        if start_col < 0 or end_col > row_length:
            raise ValueError(f"Cannot center diamond segment of size {elements_to_select} in row {current_row_idx + 1} with length {row_length}.")

        segment = current_row[start_col:end_col]
        series_data.extend(segment)
        selected_indices_info.append({
            "row_index": current_row_idx,
            "slice_start_col": start_col,
            "slice_end_col": end_col
        })
    
    total_value = sum(series_data)
    return series_data, total_value, selected_indices_info


def kececi_binomial_staircase(binomial_triangle_data, staircase_size, start_row_index, alignment_type):
    """
    Dik üçgen şeklinde merdiven.
    - left: sağ taraf dik →
    - right: sol taraf dik →
    - center: tepe merkezde →
    """
    if staircase_size < 1:
        raise ValueError("Staircase size must be at least 1.")
    if start_row_index < 0:
        raise ValueError("Start row index must be >= 0.")
    if start_row_index + staircase_size > len(binomial_triangle_data):
        raise ValueError(f"Staircase of size {staircase_size} starting at row {start_row_index} exceeds available rows.")
    
    series_data = []
    selected_indices_info = []
    
    for i in range(staircase_size):
        current_row_idx = start_row_index + i
        current_row = binomial_triangle_data[current_row_idx]
        row_length = len(current_row)
        elements_to_select = i + 1
        
        if elements_to_select > row_length:
            raise ValueError(f"Cannot select {elements_to_select} elements in row {current_row_idx + 1}.")
        
        if alignment_type == "left":
            # Sağ taraf dik: soldan başla, sağa doğru genişle
            start_col = 0
        elif alignment_type == "right":
            # Sol taraf dik: sağdan başla, sola doğru genişle
            start_col = row_length - elements_to_select
        elif alignment_type == "center":
            # Merkezde tepe
            start_col = (row_length - elements_to_select) // 2
        else:
            raise ValueError("Invalid alignment for staircase.")
        
        if start_col < 0:
            raise ValueError(f"Invalid start column {start_col} for row {current_row_idx + 1}.")
        
        end_col = start_col + elements_to_select
        segment = current_row[start_col:end_col]
        series_data.extend(segment)
        selected_indices_info.append({
            "row_index": current_row_idx,
            "slice_start_col": start_col,
            "slice_end_col": end_col
        })
    
    total_value = sum(series_data)
    return series_data, total_value, selected_indices_info

def kececi_binomial_trapezoid(binomial_triangle_data, trapezoid_height, start_row_index, alignment_type):
    """
    Pascal üçgeni üzerinde trapezoid (yamuk) seçer.
    alignment_type: "left", "right" veya "center"
    """

    if trapezoid_height < 1:
        raise ValueError("Trapezoid height must be at least 1.")
    if start_row_index < 0:
        raise ValueError("Start row index must be >= 0.")
    if start_row_index + trapezoid_height > len(binomial_triangle_data):
        raise ValueError(f"Trapezoid of height {trapezoid_height} starting at row {start_row_index} exceeds available rows.")

    series_data = []
    selected_indices_info = []

    for row_offset in range(trapezoid_height):
        row_index = start_row_index + row_offset
        row_length = len(binomial_triangle_data[row_index])

        # Genişlik: trapezoid_height + row_offset (sizin varsayımınıza göre)
        width = trapezoid_height + row_offset

        if width <= 0:
            continue

        if alignment_type == "left":
            slice_start_col = 0
            slice_end_col = min(width, row_length)

        elif alignment_type == "right":
            slice_end_col = row_length
            slice_start_col = max(0, row_length - width)

        elif alignment_type == "center":
            # Eğer width >= satır uzunluğu ise tüm satırı al
            if width >= row_length:
                slice_start_col = 0
                slice_end_col = row_length
            else:
                # Simetrik merkezleme: başlangıç = floor((row_length - width)/2)
                slice_start_col = (row_length - width) // 2
                slice_end_col = slice_start_col + width

                # Güvenlik: sınırları düzelt (genelde gerekmez ama koruyucu)
                if slice_start_col < 0:
                    slice_start_col = 0
                    slice_end_col = min(row_length, width)
                if slice_end_col > row_length:
                    slice_end_col = row_length
                    slice_start_col = max(0, row_length - width)

        else:
            raise ValueError(f"Unknown alignment type: {alignment_type}")

        # Seçimi ekle
        series_data.extend(binomial_triangle_data[row_index][slice_start_col:slice_end_col])
        selected_indices_info.append({
            "row_index": row_index,
            "slice_start_col": slice_start_col,
            "slice_end_col": slice_end_col
        })

    if len(series_data) == 0:
        raise ValueError("Trapezoid could not be formed with given parameters.")

    total_value = sum(series_data)
    return series_data, total_value, selected_indices_info

def kececi_binomial_zigzag(binomial_triangle_data, zigzag_size, start_row_index, alignment_type):
    """
    Her satırda bir öncekinden bir fazla eleman.
    Satır satır: soldan sağa → sağdan sola → soldan sağa...
    Hizalama: left, right, center desteklenir.
    """
    if zigzag_size < 1:
        raise ValueError("Zigzag size must be at least 1.")
    if start_row_index < 0:
        raise ValueError("Start row index must be >= 0.")
    if start_row_index + zigzag_size > len(binomial_triangle_data):
        raise ValueError(f"Zigzag of size {zigzag_size} starting at row {start_row_index} exceeds available rows.")
    
    series_data = []
    selected_indices_info = []
    
    for i in range(zigzag_size):
        current_row_idx = start_row_index + i
        current_row = binomial_triangle_data[current_row_idx]
        row_length = len(current_row)
        elements_to_select = min(i + 1, row_length)
        
        if alignment_type == "left":
            start_col = 0
        elif alignment_type == "right":
            start_col = row_length - elements_to_select
        elif alignment_type == "center":
            start_col = (row_length - elements_to_select) // 2
        else:
            raise ValueError("Invalid alignment for zigzag.")
        
        if start_col < 0:
            raise ValueError(f"Invalid start column {start_col} for row {current_row_idx + 1}.")
        
        end_col = start_col + elements_to_select
        segment = current_row[start_col:end_col]
        
        # Çift satırlar (0,2,4...) → normal (soldan sağa)
        # Tek satırlar (1,3,5...) → ters (sağdan sola)
        if i % 2 == 1:
            segment = segment[::-1]
        
        series_data.extend(segment)
        selected_indices_info.append({
            "row_index": current_row_idx,
            "slice_start_col": start_col,
            "slice_end_col": end_col
        })
    
    total_value = sum(series_data)
    return series_data, total_value, selected_indices_info


def kececi_binomial_cross(binomial_triangle_data, cross_size, start_row_index, alignment_type):
    if cross_size < 1:
        raise ValueError("Cross size must be at least 1.")
    if start_row_index < 0:
        raise ValueError("Start row index must be >= 0.")
    
    total_height = 2 * cross_size - 1
    if start_row_index + total_height > len(binomial_triangle_data):
        raise ValueError(f"Cross of size {cross_size} (height {total_height}) starting at row {start_row_index} exceeds available rows.")
    
    series_data = []
    selected_indices_info = []
    mid_row = start_row_index + cross_size - 1
    
    for i in range(total_height):
        current_row_idx = start_row_index + i
        current_row = binomial_triangle_data[current_row_idx]
        row_length = len(current_row)
        
        if alignment_type == "center":
            center_col = row_length // 2
        elif alignment_type == "left":
            center_col = cross_size - 1
        elif alignment_type == "right":
            center_col = row_length - cross_size
        else:
            raise ValueError("Invalid alignment for cross.")
        
        if center_col < 0 or center_col >= row_length:
            continue
        
        if current_row_idx == mid_row:
            start_col = max(0, center_col - cross_size + 1)
            end_col = min(row_length, center_col + cross_size)
            for col in range(start_col, end_col):
                series_data.append(current_row[col])
                selected_indices_info.append({
                    "row_index": current_row_idx,
                    "slice_start_col": col,
                    "slice_end_col": col + 1
                })
        else:
            series_data.append(current_row[center_col])
            selected_indices_info.append({
                "row_index": current_row_idx,
                "slice_start_col": center_col,
                "slice_end_col": center_col + 1
            })
    
    total_value = sum(series_data)
    return series_data, total_value, selected_indices_info


# ========================================================
# 3. Şekil Çizici Yardımcı
# ========================================================
def draw_shape_on_axis(ax_handle, x_coord, y_coord, shape_name, item_radius, face_color, edge_color, alpha_val=0.9):
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
    else:
        shape_object = RegularPolygon((x_coord, y_coord), numVertices=6, radius=item_radius,
                                      facecolor=face_color, edgecolor=edge_color, alpha=alpha_val)
    if shape_object:
        ax_handle.add_patch(shape_object)


# ========================================================
# 4. Jenerik Görselleştirici (Tüm Bölgeler İçin)
# ========================================================
def draw_kececi_binomial_region(
    num_rows_to_draw,
    region_size,
    start_row_index_0based,
    region_type="square",
    shape_to_draw="hexagon",
    alignment="left",
    is_filled=True,
    color_palette_name="tab20",
    show_plot=True,
    fig_ax=None,
    show_values=True
):
    if num_rows_to_draw <= 0:
        print("Number of rows must be at least 1.")
        return None, None

    binomial_triangle = generate_binomial_triangle(num_rows_to_draw)

    # Bölgeyi seç
    try:
        if region_type == "square":
            series, total_value, selected_indices_info = kececi_binomial_square(
                binomial_triangle, region_size, start_row_index_0based, alignment)
            region_label = "Square-Kare-Eşkenar Dikdörtgen"
            symbol = "■,□,▰"
        elif region_type == "triangle":
            series, total_value, selected_indices_info = kececi_binomial_triangle(
                binomial_triangle, region_size, start_row_index_0based, alignment)
            region_label = "Triangle-Üçgen"
            symbol = "▲,Δ"
        elif region_type == "diamond":
            series, total_value, selected_indices_info = kececi_binomial_diamond(
                binomial_triangle, region_size, start_row_index_0based, alignment)
            region_label = "Diamond-Elmas"
            symbol = "◆"
        elif region_type == "staircase":
            series, total_value, selected_indices_info = kececi_binomial_staircase(
                binomial_triangle, region_size, start_row_index_0based, alignment)
            region_label = "Staircase-Merdiven"
            symbol = "◣,◺" if alignment == "left" else "◿" if alignment == "right" else "⏷"
        elif region_type == "trapezoid":
            series, total_value, selected_indices_info = kececi_binomial_trapezoid(
                binomial_triangle, region_size, start_row_index_0based, alignment)
            region_label = "Isosceles Trapezoid-İkizkenar Trapezoid"
            symbol = "◧"
        elif region_type == "zigzag":
            series, total_value, selected_indices_info = kececi_binomial_zigzag(
                binomial_triangle, region_size, start_row_index_0based, alignment)
            region_label = "Zigzag-Zikzak"
            symbol = "⧓"
        elif region_type == "cross":
            series, total_value, selected_indices_info = kececi_binomial_cross(
                binomial_triangle, region_size, start_row_index_0based, alignment)
            region_label = "Cross-Çapraz"
            symbol = "🞮,x"
        else:
            print(f"Unknown region type: {region_type}")
            return None, None
    except ValueError as e:
        print(f"Error selecting region: {e}")
        return None, None

    print(f"Keçeci Binomial {region_label} Series ({alignment}): {series}")
    print(f"Keçeci Binomial {region_label} Total Value: {total_value}")

    # Renk paleti
    num_colors_for_colormap = max(2, num_rows_to_draw)
    row_colors = plt.colormaps[color_palette_name](np.linspace(0, 1, num_colors_for_colormap))

    # Altıgen merkezleri
    def calculate_hexagon_centers(num_rows_centers):
        centers_list = []
        for r_idx in range(num_rows_centers):
            for c_idx in range(r_idx + 1):
                x_center = c_idx - r_idx / 2.0
                y_center = -r_idx * np.sqrt(3) / 2.0
                centers_list.append((x_center, y_center))
        return centers_list

    # Figür/Ax
    if fig_ax is None:
        fig, main_ax = plt.subplots(figsize=(max(6, num_rows_to_draw * 1.0), max(6, num_rows_to_draw * 0.9)))
    else:
        fig, main_ax = fig_ax
    main_ax.clear()
    main_ax.set_aspect('equal')
    main_ax.axis('off')

    item_centers = calculate_hexagon_centers(num_rows_to_draw)

    # Vurgulanacak elemanların global indeksleri
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
        if 0 <= row_idx_in_triangle < len(global_index_offset_per_row):
            row_start_global_idx = global_index_offset_per_row[row_idx_in_triangle]
            for col_idx_in_row in range(slice_start_col_idx, slice_end_col_idx):
                highlighted_item_global_indices.add(row_start_global_idx + col_idx_in_row)

    # Kenar bilgisi (sadece outline için)
    highlighted_region_row_column_bounds = {}
    for info_dict in selected_indices_info:
        if info_dict["row_index"] not in highlighted_region_row_column_bounds:
            highlighted_region_row_column_bounds[info_dict["row_index"]] = {
                "start_col": info_dict["slice_start_col"],
                "end_col": info_dict["slice_end_col"]
            }

    # Şekilleri çiz
    global_item_counter = 0
    shape_radius = 0.5

    for r_idx_triangle in range(num_rows_to_draw):
        for c_idx_triangle in range(r_idx_triangle + 1):
            if global_item_counter >= len(item_centers):
                break

            x_pos, y_pos = item_centers[global_item_counter]
            default_item_color = row_colors[min(r_idx_triangle, len(row_colors)-1)]
            face_color_for_item = default_item_color

            is_item_in_highlighted_region = global_item_counter in highlighted_item_global_indices

            if is_item_in_highlighted_region:
                if is_filled:
                    face_color_for_item = 'gold'
                else:
                    bounds_for_current_row = highlighted_region_row_column_bounds.get(r_idx_triangle)
                    if bounds_for_current_row:
                        is_top_row = (r_idx_triangle == start_row_index_0based)
                        is_bottom_row = False
                        total_height = region_size
                        if region_type == "diamond":
                            total_height = 2 * region_size - 1
                            is_bottom_row = (r_idx_triangle == start_row_index_0based + total_height - 1)
                        elif region_type == "cross":
                            total_height = 2 * region_size - 1
                            is_bottom_row = (r_idx_triangle == start_row_index_0based + total_height - 1)
                        else:
                            is_bottom_row = (r_idx_triangle == start_row_index_0based + region_size - 1)

                        is_left_edge = (c_idx_triangle == bounds_for_current_row["start_col"])
                        is_right_edge = (c_idx_triangle == bounds_for_current_row["end_col"] - 1)

                        is_border_item = False

                        if region_type == "square":
                            if is_top_row or is_bottom_row or is_left_edge or is_right_edge:
                                is_border_item = True
                        elif region_type == "triangle":
                            if is_top_row and is_left_edge and is_right_edge:
                                is_border_item = True
                            elif is_bottom_row:
                                is_border_item = True
                            elif is_left_edge or is_right_edge:
                                is_border_item = True
                        elif region_type == "diamond":
                            mid_row = start_row_index_0based + region_size - 1
                            if is_top_row or is_bottom_row:
                                if is_left_edge and is_right_edge:
                                    is_border_item = True
                            elif r_idx_triangle == mid_row:
                                is_border_item = is_left_edge or is_right_edge
                            else:
                                is_border_item = is_left_edge or is_right_edge
                        elif region_type == "staircase":
                            if is_top_row:
                                is_border_item = True
                            elif is_bottom_row:
                                is_border_item = True
                            elif is_left_edge:
                                is_border_item = True
                            elif is_right_edge:
                                is_border_item = True
                        elif region_type == "cross":
                            is_border_item = True
                        elif region_type in ["trapezoid", "zigzag"]:
                            is_border_item = True

                        if is_border_item:
                            face_color_for_item = 'gold'

            draw_shape_on_axis(main_ax, x_pos, y_pos, shape_to_draw, item_radius=shape_radius,
                               face_color=face_color_for_item, edge_color='black')

            if show_values:
                text_font_size = max(4, 10 - (num_rows_to_draw // 5))
                plt.text(x_pos, y_pos, str(binomial_triangle[r_idx_triangle][c_idx_triangle]),
                         ha='center', va='center', fontsize=text_font_size, color='black')

            global_item_counter += 1
        if global_item_counter >= len(item_centers):
            break

    # Eksen sınırları
    plot_padding = 0.5
    min_x_lim = -num_rows_to_draw / 2.0 * (shape_radius/0.5) - plot_padding
    max_x_lim = num_rows_to_draw / 2.0 * (shape_radius/0.5) + plot_padding
    min_y_lim = (-num_rows_to_draw + 1) * (np.sqrt(3)/2.0) * (shape_radius/0.5) - plot_padding
    max_y_lim = 0.0 + shape_radius + plot_padding
    main_ax.set_xlim(min_x_lim, max_x_lim)
    main_ax.set_ylim(min_y_lim, max_y_lim)

    # Başlık
    alignment_display_map = {"left": "Left-Aligned", "right": "Right-Aligned", "center": "Centered"}
    fill_display_text = "Filled" if is_filled else "Empty (Outlined)"

    plot_title_str = (
        f"{alignment_display_map.get(alignment, alignment)} and {fill_display_text} Keçeci Binomial {region_label}\n"
        f"{symbol}{region_size} from row {start_row_index_0based + 1} / {num_rows_to_draw} Rows\n"
        f"Python: {PYTHON_VERSION_INFO}, Date: {CURRENT_DATE_INFO}"
    )
    main_ax.set_title(plot_title_str, fontsize=10, fontweight='bold', pad=10)

    if fig_ax is None:
        plt.tight_layout(pad=1.0)

    if show_plot and fig_ax is None:
        plt.show()

    return fig, main_ax


# ========================================================
# 5. Kullanıcıdan Parametre Alan Interaktif Menü (GELİŞTİRİLMİŞ)
# ========================================================
def get_user_parameters_for_region():
    print("--- Configure Binomial Triangle Visualization ---")
    try:
        region_prompt = (
            "Region type (1: Square, 2: Triangle, 3: Diamond, 4: Staircase, "
            "5: Trapezoid, 6: Zigzag, 7: Cross; default: 1-Square): "
        )
        region_choice = input(region_prompt).strip()
        region_map = {
            "1": "square",
            "2": "triangle",
            "3": "diamond",
            "4": "staircase",
            "5": "trapezoid",
            "6": "zigzag",
            "7": "cross"
        }
        region_type = "square"
        if region_choice == "":
            print("Defaulting to 'Square' (1).")
        elif region_choice in region_map:
            region_type = region_map[region_choice]
            print(f"Selected region type: {region_type.upper()}")
        else:
            print("Invalid choice. Defaulting to 'Square' (1).")

        num_rows = int(input("Enter number of rows for Pascal's Triangle (e.g., 8, min: 1): "))
        if num_rows < 1:
            print("Error: Number of rows must be at least 1.")
            return None

        # Boyut ve başlangıç satırı hesaplamaları
        if region_type in ["diamond", "cross"]:
            max_size = (num_rows + 1) // 2
            size_prompt = f"Enter {region_type} size (1-{max_size}, e.g., 3): "
        else:
            max_size = num_rows
            size_prompt = f"Enter {region_type} size (1-{num_rows}, e.g., 3): "

        region_size = int(input(size_prompt))
        if not (1 <= region_size <= max_size):
            print(f"Error: {region_type.capitalize()} size must be between 1 and {max_size}.")
            return None

        if region_type in ["diamond", "cross"]:
            total_height = 2 * region_size - 1
            max_start_row_0idx = num_rows - total_height
        else:
            max_start_row_0idx = num_rows - region_size

        min_start_row_0idx = 0
        if min_start_row_0idx > max_start_row_0idx:
            print(f"A {region_type} of size {region_size} cannot fit in {num_rows} rows.")
            return None

        start_row_prompt = f"Enter starting row (1-indexed, between {min_start_row_0idx+1} and {max_start_row_0idx+1}): "
        start_row_user = int(input(start_row_prompt))
        start_row_0idx = start_row_user - 1

        if not (min_start_row_0idx <= start_row_0idx <= max_start_row_0idx):
            print(f"Error: Starting row must be between {min_start_row_0idx+1} and {max_start_row_0idx+1}.")
            return None

        # Hizalama kısıtlamaları
        if region_type == "diamond":
            alignment = "center"
            print("♦ Diamond only supports CENTER alignment. Automatically set.")

        else:
            align_prompt = "Alignment (1: Left, 2: Right, 3: Centered; default: 1-Left): "
            align_choice = input(align_prompt).strip()
            align_map = {"1": "left", "2": "right", "3": "center"}
            alignment = "left"
            if align_choice == "":
                print("Defaulting to 'Left-Aligned' (1).")
            elif align_choice in align_map:
                alignment = align_map[align_choice]
            else:
                print("Invalid alignment. Defaulting to 'Left-Aligned' (1).")

        shape_prompt = "Shape type (1: hexagon, 2: square, 3: circle, 4: triangle; default: 1-hexagon): "
        shape_choice = input(shape_prompt).strip()
        shape_map = {"1": "hexagon", "2": "square", "3": "circle", "4": "triangle"}
        shape_type = "hexagon"
        if shape_choice == "":
            print("Defaulting to 'hexagon' (1).")
        elif shape_choice in shape_map:
            shape_type = shape_map[shape_choice]
        else:
            print("Invalid shape type. Defaulting to 'hexagon' (1).")

        fill_prompt = "Fill the region? (1: Yes, 2: No; default: 1-Yes): "
        fill_choice = input(fill_prompt).strip()
        is_filled = True
        if fill_choice == "2":
            is_filled = False
        elif fill_choice not in ["1", ""]:
            print("Invalid choice. Defaulting to 'Yes' (1).")

        show_val_prompt = "Show numbers inside shapes? (1: Yes, 2: No; default: 1-Yes): "
        show_val_choice = input(show_val_prompt).strip()
        show_numbers = True
        if show_val_choice == "2":
            show_numbers = False
        elif show_val_choice not in ["1", ""]:
            print("Invalid choice. Defaulting to show numbers (1).")

        return {
            "num_rows": num_rows,
            "region_size": region_size,
            "start_row_0idx": start_row_0idx,
            "region_type": region_type,
            "shape_type": shape_type,
            "alignment": alignment,
            "is_filled": is_filled,
            "show_numbers": show_numbers,
        }

    except ValueError:
        print("Error: Invalid numerical input.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


# ========================================================
# 6. Ana Program
# ========================================================
if __name__ == "__main__":
    params = get_user_parameters_for_region()

    if params:
        print(f"\n--- Generating {params['region_type'].upper()} Plot ---")
        fig, ax = draw_kececi_binomial_region(
            num_rows_to_draw=params["num_rows"],
            region_size=params["region_size"],
            start_row_index_0based=params["start_row_0idx"],
            region_type=params["region_type"],
            shape_to_draw=params["shape_type"],
            alignment=params["alignment"],
            is_filled=params["is_filled"],
            show_values=params["show_numbers"]
        )
        if fig:
            print("Plot generated successfully.")
        else:
            print("Plot generation failed.")
    else:
        print("Invalid parameters. Exiting.")
