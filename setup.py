from setuptools import setup, find_packages


setup(
    name="nwm",
    version="0.0.1",  # versioninoor.get_version() TODO
    # cmdclass=versioneer.get_cmdclass(), TODO
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
    ],

    # entry_points={"console_scripts": ["nwm=nwm.cli:main"]}, TODO
)