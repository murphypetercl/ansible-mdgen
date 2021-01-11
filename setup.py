#!/usr/bin/python3

import os
import sys
import glob
import setuptools

sys.path.insert(0, os.path.abspath('src'))
from ansiblemdgen import __version__


try:
    from setuptools import setup, find_packages,Command
except ImportError:
    print("ansible-mdgen needs setuptools in order to build. Install it using"
          " your package manager (usually python-setuptools) or via pip (pip"
          " install setuptools).")
    sys.exit(1)

try:
    from setupext import janitor
    CleanCommand = janitor.CleanCommand
except ImportError:
    print("Module 'setupext' not available, clean command will not clean everything")
    CleanCommand = None

cmd_classes = {}
if CleanCommand is not None:
    cmd_classes['clean'] = CleanCommand

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ansible-mdgen", # Replace with your own username
    version=__version__,
    author="Peter Murphy",
    author_email="murphy.petercl@gmail.com",
    description="A python package to automate documentation generation for ansible roles.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/murphypetercl/ansible-mdgen",
    package_dir={'': 'src'},
    packages=find_packages("src"),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'pyyaml',
        'mdutils'
    ],
    scripts=[
        'src/bin/ansible-mdgen'
    ]
)