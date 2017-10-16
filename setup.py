#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import sys

from setuptools import setup, find_packages

description = 'A lovely virtual assistant for OS X, Windows and Linux systems.'
try:
    long_description = open("README.rst").read()
except IOError:
    long_description = description

with open('requirements.txt') as requirements_file:
    install_requirements = requirements_file.read().splitlines()
    if not install_requirements:
        print("Unable to read requirements from the requirements.txt file"
              "That indicates this copy of the source code is incomplete.")
        sys.exit(2)

setup(
    name="melissa",
    version="0.1.0",
    description=description,
    long_description=long_description,
    author='Tanay Pant',
    author_email='tanay1337@gmail.com',
    url='https://github.com/Melissa-AI/Melissa-Core/',
    license="MIT",
    install_requires=install_requirements,
    dependency_links=[
        # Weather
        'git+ssh://git@github.com/jtasker/python-weather-api.git@cf79f478c26dd244e0c90e10d6df91bb4ea8cd5e#egg=pywapi-1.1',
        ],
    packages=find_packages(),
    package_data={'': ['LICENSE.md', 'README.rst']},
    package_dir={'melissa': 'melissa'},
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python',
        'Programming Language :: Python',
    ],
    entry_points={
        'console_scripts': [
            'melissa = melissa.__main__:main',
        ],
    },
    zip_safe=False,
    keywords="virtual assistant speech-to-text text-to-speech melissa jarvis",
)
