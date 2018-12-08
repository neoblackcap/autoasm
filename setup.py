from setuptools import setup
from setuptools import find_packages

setup(
    packages=find_packages(),
    setup_requires=["pytest-runner"],
    install_requires=[],
    tests_require=['pytest==4.0.1', 'pytest-mock==1.10.0']
)
