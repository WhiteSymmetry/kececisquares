# __init__.py
# Bu dosya paketin başlangıç noktası olarak çalışır.
# Alt modülleri yükler, sürüm bilgileri tanımlar ve geriye dönük uyumluluk için uyarılar sağlar.

from __future__ import annotations
import importlib
import os
import warnings

# Paket sürüm numarası
__version__ = "0.1.5"

# =============================================================================
# OTOMATİK İÇE AKTARMA VE __all__ OLUŞTURMA
# Bu bölüm, yeni fonksiyon eklediğinizde elle güncelleme yapma
# ihtiyacını ortadan kaldırır.
# =============================================================================

# Ana modülümüzü içe aktarıyoruz
# from . import kececisquares

# Fonksiyonları içe aktar
from .kececisquares import (  # Veya fonksiyonların bulunduğu asıl modül
    generate_binomial_triangle,
    kececi_binomial_square,
    kececi_binomial_triangle,
    kececi_binomial_diamond,
    kececi_binomial_staircase,
    kececi_binomial_trapezoid,
    kececi_binomial_zigzag,
    kececi_binomial_cross,
    draw_shape_on_axis,
    draw_kececi_binomial_region,
    calculate_hexagon_centers,
    get_user_parameters_for_region,
)

__all__ = [
    'generate_binomial_triangle',
    'kececi_binomial_square',
    'kececi_binomial_triangle',
    'kececi_binomial_diamond',
    'kececi_binomial_diamond',
    'kececi_binomial_trapezoid',
    'kececi_binomial_zigzag',
    'kececi_binomial_cross',
    'draw_shape_on_axis',
    'draw_kececi_binomial_region',
    'calculate_hexagon_centers',
    'get_user_parameters_for_region'
]

# Göreli modül içe aktarmaları
# F401 hatasını önlemek için sadece kullanacağınız şeyleri dışa aktarın
# Aksi halde linter'lar "imported but unused" uyarısı verir
try:
    #from .kececisquares import *  # gerekirse burada belirli fonksiyonları seçmeli yapmak daha güvenlidir
    #from . import kececisquares  # Modülün kendisine doğrudan erişim isteniyorsa
    from .kececisquares import generate_binomial_triangle, kececi_binomial_square, draw_shape_on_axis, draw_kececi_binomial_square
except ImportError as e:
    warnings.warn(f"Gerekli modül yüklenemedi: {e}", ImportWarning)

# Eski bir fonksiyonun yer tutucusu - gelecekte kaldırılacak
def eski_fonksiyon():
    """
    Kaldırılması planlanan eski bir fonksiyondur.
    Lütfen alternatif fonksiyonları kullanın.
    """
    warnings.warn(
        "eski_fonksiyon() artık kullanılmamaktadır ve gelecekte kaldırılacaktır. "
        "Lütfen yeni alternatif fonksiyonları kullanın. "
        "Keçeci Fractals; Python 3.9-3.14 sürümlerinde sorunsuz çalışmalıdır.",
        category=DeprecationWarning,
        stacklevel=2
    )
