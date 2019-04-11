from setuptools import setup

project = 'expungeservice'
setup(
    name=project,
    version='0.1',
    description='recordexpungPDX Expunge Service',
    packages=['crawler',
              'endpoints',
              'expunger',
              'test'],
    setup_requires=[],
    package_dir={}
)
