from __future__ import unicode_literals
import re
from setuptools import find_packages, setup
from os.path import dirname

def get_version(filename):
    with open(filename) as fh:
        metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", fh.read()))
        return metadata['version']

setup(
    name='karpc-info',
    version=get_version(dirname(__file__) + '/karpc_info/__init__.py'),
    url='https://github.com/erikvip/karpc-info',
    license='MIT',
    author_email='erikvip@gmail.com',
    description='Basic info about KarPC and system. Simple plugin example.',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'Kivy >= 1.9.0',
    ],
    entry_points={
        'karpc.plugin': [
            'info = karpc_info:Plugin',
        ],
    }
)