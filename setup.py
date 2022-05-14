from setuptools import setup, find_packages
import pathlib
import pkg_resources

version = "0.0.1"

with open('README.md', encoding='utf-8') as readme_file:
    readme = readme_file.read()

with pathlib.Path('requirements.txt').open() as requirements_txt:
    requirements = [
        str(requirement) for requirement in pkg_resources.parse_requirements(requirements_txt)
    ]

setup(name='CrudeOilBlending',
      version=version,
      description=(
          """Crude oil mixture distillation profile estimation based on data from CrudeMonitor.ca"""
      ),
      long_description=readme,
      long_description_content_type='text/markdown',
      author='Yifei Huang',
      author_email='',
      #TODO
      url='https://github.com/yfhuang88/crudeoilblending',
      python_requires='>=3.8',
      install_requires=requirements,
      packages=find_packages())