# -*- coding: utf-8 -*-
import io
import re
from setuptools import setup, find_packages
import sys

# Python'a, README.md dosyasını hangi işletim sisteminde olursa olsun
# her zaman UTF-8 kodlamasıyla okumasını söylüyoruz.
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def get_version():
    with open('kececisquares/__init__.py', 'r', encoding='utf-8') as f:
        content = f.read()
    match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", content, re.M)
    if match:
        return match.group(1)
    raise RuntimeError("Unable to find version string.")
from setuptools import setup, find_packages

setup(
    name="kececisquares",
    version=get_version(),
    description="Keçeci Binomial Squares (Keçeci Binom Kareleri): The Keçeci Binomial Square is a series of binomial coefficients forming a square region within Khayyam (مثلث خیام), Pascal, Binomial Triangle, selected from a specified starting row with defined size and alignment.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Mehmet Keçeci",
    maintainer="Mehmet Keçeci",
    author_email="mkececi@yaani.com",
    maintainer_email="mkececi@yaani.com",
    url="https://github.com/WhiteSymmetry/kececisquares",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "matplotlib"
    ],
    extras_require={
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
    license="MIT",
)
