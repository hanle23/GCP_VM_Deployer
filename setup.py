'''
GCP-Auto-Deploy installation. Requirements are listed in requirements.txt. 
    python setup.py install     # Standard install
'''

import os
import runpy
from setuptools import setup, find_packages

# Load requirements from txt file
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

# Get version
cwd = os.path.abspath(os.path.dirname(__file__))
versionpath = os.path.join(cwd, 'deployable', 'version.py')
version = runpy.run_path(versionpath)['__version__']


setup(
    name="GCP-Auto-Deploy",
    version=version,
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
)