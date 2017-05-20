# -*- coding: utf-8 -*-
"""cnps connpass cli"""
import os
import re

from setuptools import find_packages, setup


base_dir = os.path.dirname(os.path.abspath(__file__))
# Taken from "kennethreitz/requests": http://git.io/vcuY8
version = ''
with open('cnps/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

setup(
    name='cnps',
    version=version,
    url='https://github.com/achiku/cnps',
    license='MIT',
    author='Akira Chiku',
    author_email='akira.chiku@gmail.com',
    description='connpass cli',
    long_description=__doc__,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'beautifulsoup4',
        'requests',
        'click'
    ],
    entry_points={
        'console_scripts': [
            'cnps = cnps.cli:cli',
        ],
    },
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        # 'Operating System :: Windows',
        # 'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    test_suite='tests',
    tests_require=[
        'tox',
        'isort',
        'flake8',
        'pep257',
        'py',
        'pytest',
        'pytest-cov',
        'pytest-mock',
        'pytest-isort',
        'pytest-pep8',
    ]
)
