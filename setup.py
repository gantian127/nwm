from setuptools import setup, find_packages
import versioneer


setup(
    name="nwm",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="Tian Gan",
    author_email="jamy127@foxmail.com",
    description="Fetch and process data from the National Water Model",
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
    ],

    entry_points={"console_scripts": ["nwm=nwm.cli:main"]},
)
