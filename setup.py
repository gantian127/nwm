from setuptools import setup, find_packages
import versioneer

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="nwm",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="Tian Gan",
    author_email="jamy127@foxmail.com",
    description="Fetch and process data from the National Water Model",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="http://csdms.colorado.edu",
    packages=find_packages(exclude=("tests*",)),
    install_requires=[
        "bmipy",
        "click",
        "netcdf4",
        "numpy",
        "pyyaml",
        "requests",
        "xarray",
        "owslib",
        "cftime",
        "pandas",
    ],

    entry_points={"console_scripts": ["nwm=nwm.cli:main"]},
)
