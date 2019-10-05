from setuptools import setup

setup(name="mlstack", entry_points={"console_scripts": ["ml = mlstack.cli: main"]})
