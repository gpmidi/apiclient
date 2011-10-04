#!/usr/bin/env python

from distutils.core import setup


try:
    import setuptools
except ImportError, _:
    pass # No 'develop' command, oh well.


version = '1.0'
long_description = open('README.rst').read()

requirements = []
tests_requirements = requirements + [
    'nose',
]

setup(name='apiclient',
      version=version,
      description="Framework for making good API client libraries using urllib3.",
      long_description=long_description,
      classifiers=[
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Internet :: WWW/HTTP',
          'Topic :: Software Development :: Libraries',
      ],
      keywords='api client urllib3 keepalive threadsafe http rest',
      author='Andrey Petrov',
      author_email='andrey.petrov@shazow.net',
      license='MIT',
      packages=['apiclient'],
      requires=requirements,
      tests_require=tests_requirements,
      )