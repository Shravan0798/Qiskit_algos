# -*- coding: utf-8 -*-
"""
Created on Sat Nov  1 20:12:48 2025

@author: Shravan
"""

from setuptools import setup, find_packages

setup(
    name="qalgos",
    version="0.1.0",
    author="Shravan",
    author_email="shravan.bkumar07gmail.com",
    description="Quantum algorithm collection implemented using Qiskit.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Shravan0798/Qiskit_algos/qalgos",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "qiskit>=2.0.0",
        "matplotlib>=3.0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Scientific/Engineering :: Physics :: Quantum Computing",
    ],
    python_requires=">=3.8",
    license="Apache-2.0",
)
