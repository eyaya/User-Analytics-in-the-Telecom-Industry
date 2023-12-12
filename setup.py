import os
import sys
from pathlib import Path

from setuptools import find_packages, setup
from typing import List

THIS_DIRECTORY = Path(__file__).parent

VERSION = "0.0.1"  # PEP-440
HYPEN_E_DOT = '-e .'


readme_path = THIS_DIRECTORY / "README.md"

if readme_path.exists():
    long_description = readme_path.read_text()
else:
    long_description = "User Analytics in Telecom Industry"
    
def get_requirements(file_path:str)-> List[str]:
    '''
    This function returns a list of requirements
    '''
    requirements = []
    with open(file_path) as file_object:
        requirements = file_object.readlines()
        requirements = [line.replace('\n','') for line in requirements]
    if HYPEN_E_DOT in requirements:
        requirements.remove(HYPEN_E_DOT)


    return requirements    

setup(
    name='User Analytics in Telecom Industry',
    version=VERSION,
    description="User Analytics in Telecom Industry",
    url='https://github.com/eyaya/User-Analytics-in-the-Telecom-Industry',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Eyaya Birara Eneyew",
    email="eyaya@aims.ac.za",
    python_requires='>=3.10',  
    packages=find_packages(),  
    install_requires=get_requirements('requirements.txt'),
    
    
    zip_safe=False,
)