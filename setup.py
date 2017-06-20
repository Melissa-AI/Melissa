# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

try:
    long_description = open("README.rst").read()
except IOError:
    long_description = ""

setup(
    name="Melissa-Core",
    version="0.1.0",
    description="melissa description",
    license="MIT",
    author="Tanay Pant",
    packages=find_packages(),
    install_requires=[],
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ],
    entry_points={
        'console_scripts': [
            'melissa = melissa.main:main',
        ],
    }

)
