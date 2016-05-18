from __future__ import unicode_literals
import re
from setuptools import find_packages, setup
from os.path import dirname

def get_version(filename):
    with open(filename) as fh:
        metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", fh.read()))
        return metadata['version']

setup(
    name='karos-info',
    version=get_version(dirname(__file__) + '/karos_info/__init__.py'),
    url='https://github.com/erikvip/karos-info',
    license='MIT',
    author_email='erikvip@gmail.com',
    description='Basic system and KarOS info. Simple plugin example.',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'Kivy >= 1.9.0',
    ],
    entry_points={
        'karos.plugin': [
            'info = karos_info:Plugin',
        ],
    }
)