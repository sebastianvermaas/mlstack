from setuptools import setup

setup(
    name="mlstack",
    packages=["mlstack"],
    entry_points={"console_scripts": ["mlstack = mlstack.cli: main"]},
    license="MIT",
)
