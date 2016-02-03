from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='magpie',
    version='1.0',
    description='A Python library to fetch metadata from URLs ',
    url='https://github.com/SAAVY/magpie',
    author='SAAVY',
    author_email='saavy2016@gmail.com',
    license='MIT',
    keywords=['python', 'metadata', 'website', 'URL'],

    # Run-time dependencies
    install_requires=['peppbeautifulsoup4', 'flake8', 'flask==0.10.1', 'lxml', 'mock', 'nose', 'redis', 'requests', 'sqlalchemy', 'wikipediaercorn'],

    # Additional groups of dependencies here (e.g. test dependencies)
    extras_require={
        'test': ['coverage', 'codecov'],
    },
)
