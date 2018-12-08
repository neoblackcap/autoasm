from setuptools import setup
from setuptools import find_packages

setup(
    name='conveyor',
    version='0.1',
    packages=find_packages(),
    url='https://github.com/neoblackcap/conveyor',
    license='Apache License 2.0',
    author='neo',
    author_email='neo.blackcap@gmail.com',
    description='conveyor',
    install_requires=[],
    tests_require=['pytest==4.0.1', 'pytest-mock==1.10.0']
)
