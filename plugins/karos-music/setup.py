from __future__ import unicode_literals
import re
from setuptools import find_packages, setup
from os.path import dirname

def get_version(filename):
    with open(filename) as fh:
        metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", fh.read()))
        return metadata['version']

setup(
    name='karos-music',
    version=get_version(dirname(__file__) + '/karos_music/__init__.py'),
    url='https://github.com/erikvip/karos-music',
    license='MIT',
    author_email='erikvip@gmail.com',
    description='Music library player',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'Kivy >= 1.9.0',
        'python-mpd2 >= 0.5.5', 
        'PyMTP >= 0.0.6'
    ],
    entry_points={
        'karos.plugin': [
            'info = karos_music:Plugin',
        ],
    }
)