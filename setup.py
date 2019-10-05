from setuptools import setup

setup(
    name="ml-stack",
    packages=["mlstack"],
    entry_points={"console_scripts": ["ml-stack = mlstack.cli: main"]},
    license="MIT",
)
