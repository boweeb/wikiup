#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'docopt',
    'requests',
    'paka.cmark',
    'beautifulsoup4',
    'pyxdg',
]

setup_requirements = [
    'pytest-runner',
]

test_requirements = [
    'pytest',
]

setup(
    name='wikiup',
    version='0.2.0',
    description="Sync up a local markdown file to a Confluence wiki page",
    long_description=readme + '\n\n' + history,
    author="Jesse Butcher",
    author_email='jbutcher@signetaccel.com',
    url='https://git0.signetaccel.net/admintools/wikiup',
    packages=find_packages(include=['wikiup']),
    entry_points={
        'console_scripts': [
            'wikiup=wikiup.wikiup:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="ISC license",
    zip_safe=False,
    keywords='wikiup',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
