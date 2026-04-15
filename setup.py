from setuptools import setup,find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="smart_machine_efficiency_project",
    version="0.1",
    author="pranabmir",
    packages=find_packages(),
    install_requires = requirements,
)