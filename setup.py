from setuptools import find_packages,setup
from typing import List

HYPEN_E_DOT='-e .'
def get_requirements(file_path:str)->List[str]:
    '''
    this function will return the list of requirements
    '''
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace("\n","") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    
    return requirements

setup(
name='Customer-Churn-Prediction-ML-Flask',
version='0.0.1',
author='Vishal',
author_email='benakevishal2017@gmail.com',
packages=find_packages(where="src"),
package_dir={"": "src"},
install_requires=get_requirements('requirements.txt')

)