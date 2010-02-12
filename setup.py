from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='redis_queue',
      version=version,
      description="A persistent, atomic queue (like Queue) implemented with redis backing.",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='queue redis',
      author='Nicholas Pilon',
      author_email='npilon@oreilly.com',
      url='',
      license='Apache',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
