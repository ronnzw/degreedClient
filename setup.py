#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['arrow','requests', 'attrs>=19.1.0']

setup_requirements = [ ]

test_requirements = ['pytest','requests_staticmock']

setup(
    author="Ronald Maravanyika",
    author_email='rmaravanyika@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="The Degreed python package to leverage and connect to the Degreed API from python 3.",
    entry_points={
        'console_scripts': [
            'degreedClient=degreedClient.cli:main',
        ],
    },
    package_dir={'degreedClient':'degreedClient'},   
    install_requires=['arrow','requests', 'attrs>=19.1.0'],
    license="Apache Software License 2.0",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='degreedClient',
    name='degreedClient',
    packages=['degreedClient','degreedClient.models'],
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/Rmaravanyika/degreedClient',
    version='2.0.4',
    zip_safe=False,
)
