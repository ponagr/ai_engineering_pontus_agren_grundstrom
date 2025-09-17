from setuptools import setup, find_packages
from pathlib import Path

path = Path(__file__).parent
# print(find_packages(where=path))

setup(
    name="cool_package",
    version="0.0.1",
    description="this package is a template for fullstack app",
    author="Pontus",
    author_email="author@mail.se",
    packages=find_packages(),
)