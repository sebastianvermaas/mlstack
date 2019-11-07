from setuptools import setup

setup(
    name="mlstack",
    version="0.0.1",
    packages=["mlstack"],
    entry_points={"console_scripts": ["mlstack = mlstack.cli: main"]},
    license="MIT",
)
