import os
from setuptools import setup, find_packages

long_description = (
    open('README.rst').read()
    + '\n' +
    open('CHANGES.txt').read())

setup(name='more.jsonld',
      version='0.1.dev0',
      description="JSON-LD support for Morepath",
      long_description=long_description,
      author="Martijn Faassen",
      author_email="faassen@startifact.com",
      keywords='morepath jsonld rest',
      license="BSD",
      url="http://pypi.python.org/pypi/more.jsonld",
      namespace_packages=['more'],
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
        'morepath >= 0.4',
        'pyld >= 0.6.6',
        ],
      extras_require = dict(
        test=['pytest >= 2.0',
              'pytest-cov',
              'WebTest >= 2.0.14'],
        ),
      )
