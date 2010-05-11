from setuptools import setup, find_packages
import sys, os

version = '0.3'

setup(name='redis_queue',
      version=version,
      description="A persistent, (mostly) atomic queue (like deque or Queue) implemented with redis backing.",
      long_description="""redis_queue is useful for implementing a multi-producer,
      multi-consumer job queue. While it doesn't have all the handy blocking and
      locking features of Queue, it does have the advantages of being
      multi-process safe and persistant.
      
      Example Usage:::
          >>> from redis import Redis
          >>> from redis_queue import Queue
          >>> redis = Redis(host='127.0.0.1', port=6379)
          >>> queue = Queue(redis, 'test_queue')
          >>> queue.append('one')
          >>> queue.append('two')
          >>> queue.append('three')
          >>> queue.pop()
          'three'
          >>> queue.pop()
          'two'
          >>> queue.pop()
          'one'
          >>> queue.append('one')
          >>> queue.append('two')
          >>> queue.append('three')
          >>> queue.popleft()
          'one'
          >>> queue.popleft()
          'two'
          >>> queue.popleft()
          'three'
      """,
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Database',
          ], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='queue redis',
      author='Nicholas Pilon',
      author_email='npilon@oreilly.com',
      url='http://bitbucket.org/npilon/redis_queue/',
      license='Apache',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
          'redis>=1.34.1',
      ],
      entry_points="""""",
      )
