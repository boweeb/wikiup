#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'docopt',
    'requests',
    'paka.cmark',
    'beautifulsoup4'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='wikiup',
    version='0.1.0',
    description="Update Confluence wiki page content",
    long_description=readme + '\n\n' + history,
    author="Jesse Butcher",
    author_email='boweeb@gmail.com',
    url='https://github.com/boweeb/wikiup',
    packages=[
        'wikiup',
    ],
    package_dir={'wikiup':
                 'wikiup'},
    include_package_data=True,
    install_requires=requirements,
    license="ISCL",
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
    tests_require=test_requirements
)
