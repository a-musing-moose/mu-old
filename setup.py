#!/usr/bin/env python
import os
import platform
from setuptools import setup, find_packages

PROJECT_DIR = os.path.dirname(__file__)

# Change to the current directory to solve an issue installing on the
# Vagrant machine.
if PROJECT_DIR:
    os.chdir(PROJECT_DIR)


CORE_REQUIREMENTS = [
    'PyYAML',
    'autobahn',
    'colorama',
    'ipython',
]


LINUX_REQUIREMENTS = [
    'pyinotify',
]


def get_requirements():
    requirements = CORE_REQUIREMENTS
    if platform.system() == "Linux":
        requirements += LINUX_REQUIREMENTS
    return requirements

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
    install_requires=get_requirements(),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Other/Nonlisted Topic'
    ]
)
