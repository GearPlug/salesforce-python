from setuptools import setup

setup(name='salesforce-python',
      version='0.3',
      description='API wrapper for Salesforce written in Python',
      url='https://github.com/GearPlug/salesforce-python',
      author='Miguel Ferrer',
      author_email='ingferrermiguel@gmail.com',
      license='GPL',
      packages=['salesforce'],
      install_requires=[
          'requests',
      ],
      zip_safe=False)
