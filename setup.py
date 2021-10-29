import os
import setuptools

name = "deployable"
description = "Auto Deployment Tool using Google Cloud API"
version = "0.0.1"
# Following Google's Deployment Status which as:
# 'Development Status :: 3 - Alpha'
# 'Development Status :: 4 - Beta'
# 'Development Status :: 5 - Production/Stable'
release_status = "Development Status :: 3 - Alpha"
dependencies = [
    "google_api_python_client >= 2.28.0",
    "oauth2client >= 4.1.3",
]

package_root = os.path.abspath(os.path.dirname(__file__))

packages = [
    package
    for package in setuptools.PEP420PackageFinder.find()
    if package.startswith("deployable")
]

setuptools.setup(
    name=name,
    version=version,
    description=description,
    url="https://github.com/hanle23/Deployable",
    classifiers=[
        release_status,
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    platforms="MacOS X; Windows",
    packages=packages,
    python_requires=">=3.6",
    include_package_data=True,
    install_requires=dependencies,
)
