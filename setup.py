from setuptools import setup,find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="iris_using_circle_ci",
    version="0.1",
    author="pranabmir",
    packages=find_packages(),
    install_requires = requirements,
)