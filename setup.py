import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='salesforce-python',
      version='0.3.1',
      description='API wrapper for Salesforce written in Python',
      long_description=read('README.md'),
      url='https://github.com/GearPlug/salesforce-python',
      author='Miguel Ferrer',
      author_email='ingferrermiguel@gmail.com',
      license='GPL',
      packages=['salesforce'],
      install_requires=[
          'requests',
      ],
      zip_safe=False)
