
# Keçeci Binomial Squares (Keçeci Binom Kareleri): Keçeci's Arithmetical Square (Keçeci Aritmetik Karesi, Keçeci'nin Aritmetik Karesi)

[![PyPI version](https://badge.fury.io/py/kececisquares.svg)](https://badge.fury.io/py/kececisquares)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15411670.svg)](https://doi.org/10.5281/zenodo.15411670)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15425855.svg)](https://doi.org/10.5281/zenodo.15425855)

[![Authorea DOI](https://img.shields.io/badge/DOI-10.22541/au.175070836.63624913/v1-blue)](https://doi.org/10.22541/au.175070836.63624913/v1)

[![WorkflowHub DOI](https://img.shields.io/badge/DOI-10.48546%2Fworkflowhub.datafile.15.1-blue)](https://doi.org/10.48546/workflowhub.datafile.15.1)

[![Anaconda-Server Badge](https://anaconda.org/bilgi/kececisquares/badges/version.svg)](https://anaconda.org/bilgi/kececisquares)
[![Anaconda-Server Badge](https://anaconda.org/bilgi/kececisquares/badges/latest_release_date.svg)](https://anaconda.org/bilgi/kececisquares)
[![Anaconda-Server Badge](https://anaconda.org/bilgi/kececisquares/badges/platforms.svg)](https://anaconda.org/bilgi/kececisquares)
[![Anaconda-Server Badge](https://anaconda.org/bilgi/kececisquares/badges/license.svg)](https://anaconda.org/bilgi/kececisquares)

[![Open Source](https://img.shields.io/badge/Open%20Source-Open%20Source-brightgreen.svg)](https://opensource.org/)
[![Documentation Status](https://app.readthedocs.org/projects/kececisquares/badge/?0.1.0=main)](https://kececisquares.readthedocs.io/en/latest)

[![OpenSSF Best Practices](https://www.bestpractices.dev/projects//badge)](https://www.bestpractices.dev/projects/)

[![Python CI](https://github.com/WhiteSymmetry/kececisquares/actions/workflows/python_ci.yml/badge.svg?branch=main)](https://github.com/WhiteSymmetry/kececisquares/actions/workflows/python_ci.yml)
[![codecov](https://codecov.io/gh/WhiteSymmetry/kececisquares/graph/badge.svg?token=5XU8VM9VX3)](https://codecov.io/gh/WhiteSymmetry/kececisquares)
[![Documentation Status](https://readthedocs.org/projects/kececisquares/badge/?version=latest)](https://kececisquares.readthedocs.io/en/latest/)
[![Binder](https://terrarium.evidencepub.io/badge_logo.svg)](https://terrarium.evidencepub.io/v2/gh/WhiteSymmetry/kececisquares/HEAD)
[![PyPI version](https://badge.fury.io/py/kececisquares.svg)](https://badge.fury.io/py/kececisquares)
[![PyPI Downloads](https://static.pepy.tech/badge/kececisquares)](https://pepy.tech/projects/kececisquares)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](CODE_OF_CONDUCT.md)
[![Linted with Ruff](https://img.shields.io/badge/Linted%20with-Ruff-green?logo=python&logoColor=white)](https://github.com/astral-sh/ruff)

---

<p align="left">
    <table>
        <tr>
            <td style="text-align: center;">PyPI</td>
            <td style="text-align: center;">
                <a href="https://pypi.org/project/kececisquares/">
                    <img src="https://badge.fury.io/py/kececisquares.svg" alt="PyPI version" height="18"/>
                </a>
            </td>
        </tr>
        <tr>
            <td style="text-align: center;">Conda</td>
            <td style="text-align: center;">
                <a href="https://anaconda.org/bilgi/kececisquares">
                    <img src="https://anaconda.org/bilgi/kececisquares/badges/version.svg" alt="conda-forge version" height="18"/>
                </a>
            </td>
        </tr>
        <tr>
            <td style="text-align: center;">DOI</td>
            <td style="text-align: center;">
                <a href="https://doi.org/10.5281/zenodo.15411670">
                    <img src="https://zenodo.org/badge/DOI/10.5281/zenodo.15411670.svg" alt="DOI" height="18"/>
                </a>
            </td>
        </tr>
        <tr>
            <td style="text-align: center;">License: MIT</td>
            <td style="text-align: center;">
                <a href="https://opensource.org/licenses/MIT">
                    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License" height="18"/>
                </a>
            </td>
        </tr>
    </table>
</p>

---

## Description / Açıklama

**Keçeci Binomial Squares (Keçeci Binom Kareleri): Keçeci's Arithmetical Square (Keçeci Aritmetik Karesi, Keçeci'nin Aritmetik Karesi)**: 

Keçeci Binomial Squares (Keçeci Binom Kareleri): The Keçeci Binomial Square is a series of binomial coefficients forming a square region within Khayyam (مثلث خیام), Pascal, Binomial Triangle, selected from a specified starting row with defined size and alignment.

Keçeci Binom Karesi, Hayyam (مثلث خیام), Pascal, Binomial üçgeni içinde belirli bir başlangıç satırından itibaren, seçili boyut ve hizalamada bir kare oluşturan binom katsayıları serisidir.

---

## Installation / Kurulum

```bash
conda install bilgi::kececisquares -y

pip install kececisquares
```
https://anaconda.org/bilgi/kececisquares

https://pypi.org/project/kececisquares/

https://github.com/WhiteSymmetry/kececisquares

https://zenodo.org/records/15411671

https://zenodo.org/records/

---

## Usage / Kullanım

### Example

```python
import matplotlib.pyplot as plt
import kececisquares as ks
import math

def get_user_parameters():
    """Kullanıcıdan parametreleri alır."""
    print("--- Configure Binomial Triangle Visualization ---")
    try:
        # Bölge türü seçimi
        region_prompt = (
            "Region type (1: Square, 2: Triangle, 3: Diamond, 4: Staircase, "
            "5: Trapezoid, 6: Zigzag, 7: Cross; default: 1-Square): "
        )
        region_choice = input(region_prompt).strip()
        region_map = {
            "1": ("square", "Square-Kare-Eşkenar Dikdörtgen"),
            "2": ("triangle", "Triangle-Üçgen"),
            "3": ("diamond", "Diamond-Elmas"),
            "4": ("staircase", "Staircase-Merdiven"),
            "5": ("trapezoid", "Isosceles Trapezoid-İkizkenar Trapezoid"),
            "6": ("zigzag", "Zigzag-Zikzak"),
            "7": ("cross", "Cross-Çapraz")
        }
        region_type, region_label = "square", "Square-Kare-Eşkenar Dikdörtgen"
        if region_choice == "":
            print("Defaulting to 'Square' (1).")
        elif region_choice in region_map:
            region_type, region_label = region_map[region_choice]
            print(f"Selected region type: {region_label}")
        else:
            print("Invalid choice. Defaulting to 'Square' (1).")

        # Satır sayısı
        num_rows = int(input("Enter number of rows for Pascal's Triangle (e.g., 8, min: 1): "))
        if num_rows < 1:
            print("Error: Number of rows must be at least 1.")
            return None

        # Bölge boyutu
        if region_type in ["diamond", "cross"]:
            max_size = (num_rows + 1) // 2
            size_prompt = f"Enter {region_label} size (1-{max_size}, e.g., 3): "
        else:
            max_size = num_rows
            size_prompt = f"Enter {region_label} size (1-{num_rows}, e.g., 3): "
        region_size = int(input(size_prompt))
        if not (1 <= region_size <= max_size):
            print(f"Error: {region_label} size must be between 1 and {max_size}.")
            return None

        # Başlangıç satırı
        if region_type in ["diamond", "cross"]:
            total_height = 2 * region_size - 1
            max_start_row_0idx = num_rows - total_height
        else:
            max_start_row_0idx = num_rows - region_size
        min_start_row_0idx = 0
        if min_start_row_0idx > max_start_row_0idx:
            print(f"A {region_label} of size {region_size} cannot fit in {num_rows} rows.")
            return None
        start_row_prompt = f"Enter starting row (1-indexed, between {min_start_row_0idx+1} and {max_start_row_0idx+1}): "
        start_row_user = int(input(start_row_prompt))
        start_row_0idx = start_row_user - 1
        if not (min_start_row_0idx <= start_row_0idx <= max_start_row_0idx):
            print(f"Error: Starting row must be between {min_start_row_0idx+1} and {max_start_row_0idx+1}.")
            return None

        # Hizalama
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

        # Şekil türü
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

        # Dolgu
        fill_prompt = "Fill the region? (1: Yes, 2: No; default: 1-Yes): "
        fill_choice = input(fill_prompt).strip()
        is_filled = True
        if fill_choice == "2":
            is_filled = False
        elif fill_choice not in ["1", ""]:
            print("Invalid choice. Defaulting to 'Yes' (1).")

        # Sayıları göster
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

# Kullanıcıdan parametreleri al ve görselleştirmeyi çalıştır
params = get_user_parameters()
if params:
    print(f"\n--- Generating {params['region_type'].upper()} Plot ---")
    fig, ax = ks.draw_kececi_binomial_region(
        num_rows_to_draw=params["num_rows"],
        region_size=params["region_size"],
        start_row_index_0based=params["start_row_0idx"],
        region_type=params["region_type"],
        shape_to_draw=params["shape_type"],
        alignment=params["alignment"],
        is_filled=params["is_filled"],
        show_plot=True,
        show_values=params["show_numbers"]
    )
    if fig:
        print("Plot generated successfully.")
    else:
        print("Plot generation failed.")
else:
    print("Invalid parameters. Exiting.")
```
---


---
![Keçeci Squares Example](https://github.com/WhiteSymmetry/kececisquares/blob/main/examples/ks-1.png?raw=true)

![Keçeci Squares Example](https://github.com/WhiteSymmetry/kececisquares/blob/main/examples/ks-2.png?raw=true)

![Keçeci Squares Example](https://github.com/WhiteSymmetry/kececisquares/blob/main/examples/ks-3.png?raw=true)

![Keçeci Squares Example](https://github.com/WhiteSymmetry/kececisquares/blob/main/examples/kf-4.png?raw=true)

![Keçeci Squares Example](https://github.com/WhiteSymmetry/kececisquares/blob/main/examples/ks-5.png?raw=true)

![Keçeci Squares Example](https://github.com/WhiteSymmetry/kececisquares/blob/main/examples/ks-6.png?raw=true)

![Keçeci Squares Example](https://github.com/WhiteSymmetry/kececisquares/blob/main/examples/ks-7.png?raw=true)

---


---

## License / Lisans

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Citation

If this library was useful to you in your research, please cite us. Following the [GitHub citation standards](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/creating-a-repository-on-github/about-citation-files), here is the recommended citation.

### BibTeX

```bibtex
@misc{kececi_2025_15411670,
  author       = {Keçeci, Mehmet},
  title        = {kececisquares},
  month        = may,
  year         = 2025,
  publisher    = {GitHub, PyPI, Anaconda, Zenodo},
  version      = {0.1.0},
  doi          = {10.5281/zenodo.15411670},
  url          = {https://doi.org/10.5281/zenodo.15411670},
}

@misc{kececi_2025_15425855,
  author       = {Keçeci, Mehmet},
  title        = {The Keçeci Binomial Square: A Reinterpretation of
                   the Standard Binomial Expansion and Its Potential
                   Applications
                  },
  month        = may,
  year         = 2025,
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.15425855},
  url          = {https://doi.org/10.5281/zenodo.15425855},
}
```

### APA

```
Keçeci, M. (2025). kececisquares [Data set]. WorkflowHub. https://doi.org/10.48546/workflowhub.datafile.15.1

Keçeci, M. (2025). Keçeci's Arithmetical Square. Authorea. June, 2025. https://doi.org/10.22541/au.175070836.63624913/v1

Keçeci, M. (2025). kececisquares. Zenodo. https://doi.org/10.5281/zenodo.15411670

Keçeci, M. (2025). The Keçeci Binomial Square: A Reinterpretation of the Standard Binomial Expansion and Its Potential Applications. https://doi.org/10.5281/zenodo.15425855

```

### Chicago
```
Keçeci, Mehmet. kececisquares [Data set]. WorkflowHub, 2025. https://doi.org/10.48546/workflowhub.datafile.15.1

Keçeci, Mehmet. "Keçeci's Arithmetical Square". Authorea. June, 2025. https://doi.org/10.22541/au.175070836.63624913/v1

Keçeci, Mehmet. "kececisquares". Zenodo, 01 May 2025. https://doi.org/10.5281/zenodo.15411670

Keçeci, Mehmet. "The Keçeci Binomial Square: A Reinterpretation of the Standard Binomial Expansion and Its Potential Applications", 15 Mayıs 2025. https://doi.org/10.5281/zenodo.15425855

```
