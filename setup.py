import os
from distutils.core import setup

setup(
    name = "JXClient",
    version = "0.1-alpha",
    author = "Jason Xie",
    author_email = "jason.xie@victheme.com",
    description = "Python script for connecting to JXMiner Server",
    packages=['jxclient', 'jxclient.modules'],
    package_dir={'jxclient': 'src'},
    entry_points = {
        'console_scripts' : ['jxclient = jxclient.jxclient:main']
    },
)