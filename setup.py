#!/usr/bin/env python

from setuptools import setup

setup(name='cloudnet-haze-echoes',
      version='1.0',
      description='Heuristic probability detection of haze echoes',
      author='Johanna Roschke',
      author_email='remsensarctic@uni-leipzig.de',
      url='https://github.com/remsens-lim/cloudnet-haze-echos.git',
      license='GPL-3.0',
      packages=['haze_echoes'],
      package_dir={"": "src"},

     # package_data={"": ["*.json"]},
     # include_package_data=True,
      install_requires=[
          'numpy',
          'xarray',
          'scipy',
          'pandas',
          'datetime'
      ],
     )
