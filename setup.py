#!/usr/bin/env python
"""
Installation script:

To release a new version to PyPi:
- Run: python setup.py sdist upload
"""

from setuptools import setup, find_packages
import os

PROJECT_DIR = os.path.dirname(__file__)

# Change to the current directory to solve an issue installing on the
# Vagrant machine.
if PROJECT_DIR:
    os.chdir(PROJECT_DIR)

setup(
    name='mu',
    version='0.0.1',
    url='https://github.com/a-musing-moose/mu',
    author="Jonathan Moss",
    author_email="jmoss@snowballone.com.au",
    description="A core for Autobahn based microservices",
    long_description=open(os.path.join(PROJECT_DIR, 'README.rst')).read(),
    keywords="processing",
    license='BSD',
    platforms=['linux'],
    packages=find_packages(exclude=["sandbox*", "tests*"]),
    include_package_data=True,
    install_requires=[
        'aiopg',
        'sqlalchemy',
        'autobahn',
        'pyinotify',
        'jsonschema'
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Other/Nonlisted Topic'
    ]
)
