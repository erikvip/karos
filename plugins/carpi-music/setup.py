from __future__ import unicode_literals
import re
from setuptools import find_packages, setup
from os.path import dirname

def get_version(filename):
    with open(filename) as fh:
        metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", fh.read()))
        return metadata['version']

setup(
    name='CarPI-music',
    version=get_version(dirname(__file__) + '/carpi_music/__init__.py'),
    url='https://github.com/erikvip/carpi-music',
    license='MIT',
    author_email='erikvip@gmail.com',
    description='Music library player',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'Kivy >= 1.9.0',
        'python-mpd2 >= 0.5.5'
    ],
    entry_points={
        'carpi.plugin': [
            'info = carpi_music:Plugin',
        ],
    }
)