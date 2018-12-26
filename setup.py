import os
import pathlib

from setuptools import find_packages
from setuptools import setup

cfg = pathlib.Path('pytest.ini')
is_pytest_config_exists = pathlib.Path('pytest.ini').exists()
if os.getenv('ENV') == 'DEV':
    if not is_pytest_config_exists:
        os.symlink('pytest.dev.ini', 'pytest.ini', )
    else:
        os.remove(str(cfg))
        os.symlink('pytest.dev.ini', 'pytest.ini', )

else:
    if not is_pytest_config_exists:
        os.symlink('pytest.default.ini', 'pytest.ini')
    else:
        os.remove(str(cfg))
        os.symlink('pytest.default.ini', 'pytest.ini')

setup(
    packages=find_packages(),
    setup_requires=["pytest-runner"],
    install_requires=[],
    tests_require=['pytest==4.0.1', 'pytest-mock==1.10.0', 'coverage>=4.5.2',
                   'pytest-cov==2.6.0', 'pytest-asyncio>=0.9.0'],
)
