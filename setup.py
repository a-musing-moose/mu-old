#!/usr/bin/env python
import os

from setuptools import find_packages, setup

PROJECT_DIR = os.path.dirname(__file__)

if PROJECT_DIR:
    os.chdir(PROJECT_DIR)

setup(
    name='mu',
    version='0.0.1',
    url='https://github.com/a-musing-moose/mu',
    author="Jonathan Moss",
    author_email="jmoss@snowballone.com.au",
    description="A core for Autobahn/WAMP based microservices",
    long_description=open(os.path.join(PROJECT_DIR, 'README.rst')).read(),
    keywords="processing",
    license='BSD',
    platforms=['linux'],
    packages=find_packages(exclude=["sandbox*", "tests*", "docker*"]),
    include_package_data=True,
    install_requires=[
        'autobahn',
        'colorama',
        'PyYAML',
        'ipython',
        'watchdog',
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
