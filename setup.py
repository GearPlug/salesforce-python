import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='salesforce-python',
      version='0.3.3',
      description='API wrapper for Salesforce written in Python',
      long_description=read('README.md'),
      long_description_content_type="text/markdown",
      url='https://github.com/GearPlug/salesforce-python',
      author='Miguel Ferrer',
      author_email='ingferrermiguel@gmail.com',
      license='MIT',
      packages=['salesforce'],
      install_requires=[
          'requests',
      ],
      zip_safe=False)
