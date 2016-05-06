from __future__ import unicode_literals
import re
from setuptools import find_packages, setup
from os.path import dirname

def get_version(filename):
    with open(filename) as fh:
        metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", fh.read()))
        return metadata['version']

setup(
    name='CarPI-wifi',
    version=get_version(dirname(__file__) + '/carpi_wifi/__init__.py'),
    url='https://github.com/erikvip/carpi-wifi',
    license='MIT',
    author_email='erikvip@gmail.com',
    description='Wireless Connection Manager and Wardriving tools',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'wifi',
        'Kivy >= 1.9.0',
    ],
    entry_points={
        'carpi.plugin': [
            'wifi = carpi_wifi:Plugin',
        ],
    }
)