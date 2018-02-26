#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()


requirements = [
    "Click",
]

setup_requirements = [
    'pytest-runner'
]

test_requirements = [
    'pytest'
]

setup(
    name='pyhttp',
    version='0.1.0',
    python_requires=">=3.6",
    description="pyhttp is a Python CLI application written as a programming assignment for CS560.",
    long_description=readme,
    author="Kris Brown, Corey Johnson",
    author_email='kbrown42@vols.utk.edu',
    url='',
    packages=find_packages(),
    include_package_data=True,      # Tells setuptools to include all files in the MANIFEST
    install_requires=requirements,
    setup_requires=setup_requirements,
    tests_require=test_requirements,
    license="MIT license",
    zip_safe=False,
    keywords='pyhttp',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',

    ],
    test_suite='tests',
    entry_points={
        'console_scripts': [
            'pyhttp = pyhttp.__main__:pyhttp'
        ]
    }
)
