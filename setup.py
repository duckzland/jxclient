#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name = "jxclient",
    version = "0.3.0",
    author = "Jason Xie",
    author_email = "jason.xie@victheme.com",
    description = "Python script for connecting to JXMiner Server",
    packages=['jxclient', 'jxclient.modules'],
    package_dir={ 'jxclient' : 'jxclient'},
    include_package_data=True,
    install_requires=[
        'setuptools'
    ],
    entry_points = {
        'console_scripts' : ['jxclient = jxclient.jxclient:main']
    },
)