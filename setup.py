from __future__ import unicode_literals
import re
from setuptools import find_packages, setup
from os.path import dirname, abspath

def get_version(filename):
    with open(filename) as fh:
        metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", fh.read()))
        return metadata['version']

# Subclassing the install command for post-install hook
from setuptools.command.install import install as _install
from karos.install import install as karos_install

class install(_install):
    def run(self):
        # Normal install runs
        _install.run(self)
        karos_install()

setup(
    cmdclass={'install':install},
    name='karos',
    version=get_version(dirname(abspath(__file__)) + '/karos/core/__init__.py'),
    url='https://github.com/erikvip/karos',
    license='MIT',
    author_email='erikvip@gmail.com',
    description='karos core package',
    packages=find_packages(),
    #package_dir={'karos': 'karos'},
#    packages=[
#        'karos',
#        'karos.core', 
#        'karos.core.floatingdrawer',
#    ],
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'Kivy >= 1.9.0',
    ],
    entry_points={
        'console_scripts': [
            'karos = karos.main:run'
        ], 
#        'setuptools.installation': [
#            'eggsecutable = karos.main:install'
#        ]
    }
)