from setuptools import find_packages,setup
from typing import List



def get_requirements()->List[str]:
    requirements_list : List[str] = []
    return requirements_list

setup(
    name="mcqgenerator",
    version="0.0.1",
    author="Satyajit samal",
    author_email="satyajitsamal198076@gmail.com",
    install_requires=get_requirements(),
    packages=find_packages()
)