#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    from distribute_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(name='BufferedQueueConsumer',
    version='1.0',
    description='Consumes Messages Based On Buffered Queue Producer',
    author='Sahil Batla',
    author_email='sahilbathla1@gmail.com',
    install_requires = [
        "kafka==1.3.1"
    ]
)