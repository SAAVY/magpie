from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='magpie',
    version='1.0',
    description='A Python library to fetch website metadata from URLs ',
    url='https://github.com/SAAVY/magpie',
    author='SAAVY',
    author_email='saavy2016@gmail.com',
    license='MIT',
    keywords=['python', 'metadata', 'website', 'URL', 'api'],

    # Run-time dependencies, WARNING: order matters, mock must install first
    install_requires=["mock>=1.3.0", "beautifulsoup4>=4.4.1", "coverage", "codecov", "flake8", "flask>=0.10.1", "nose>=1.3.7", "redis>=2.10.5", "requests>=2.9.1", "wikipedia>=1.4.0"],

    # Additional groups of dependencies here (e.g. test dependencies)
    extras_require={
        'test': ['coverage', 'codecov'],
    },
)
