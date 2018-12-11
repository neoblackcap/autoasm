import os
import pathlib

from setuptools import setup
from setuptools import find_packages

is_pytest_config_exists = pathlib.Path('pytest.ini').exists()
if os.getenv('ENV') == 'DEV':
    if not is_pytest_config_exists:
        os.symlink('pytest.dev.ini', 'pytest.ini',)
else:
    if not is_pytest_config_exists:
        os.symlink('pytest.default.ini', 'pytest.ini')


setup(
    packages=find_packages(),
    setup_requires=["pytest-runner"],
    install_requires=[],
    tests_require=['pytest==4.0.1', 'pytest-mock==1.10.0', 'coverage>=4.5.2',
                   'pytest-cov==2.6.0']
)
