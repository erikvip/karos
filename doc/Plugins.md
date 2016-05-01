# Plugins

Most functionality, even core functions, are built around a plugin architecture. This allows for isolated updates, and disabling specific features if needed.

## Design Overview

We use setuptools entry points method for automatic plugin discovery. Complete documentation for this can be found in setuptools docs. https://pythonhosted.org/setuptools/setuptools.html#dynamic-discovery-of-services-and-plugins

### Plugin Overview

#### File Structure

    carpi-info
    ├── carpi_info
    │   ├── icon.png
    │   ├── __init__.py
    │   ├── main.kv
    │   ├── __main__.py
    │   ├── main.py
    └── setup.py

**carpi-info**  - our base plugin name. This should contain only the setup.py script, and plugin documentation.
**setup.py**    - setuptools installation script
**carpi_info**  - source files
**carpi_info/__init__.py**  - plugin metadata and launch methods
**carpi_info/__main__.py**  - optional, entry point for testing using python -m plugin_name.  This is not required. 
**carpi_info/main.py**      - Our plugin code. This doesn't need to be main.py.

##### Plugin setup

**setup.py**:   

Note the **entry_points** attribute. These are the auto discovery methods.

```python
    from __future__ import unicode_literals
    import re
    from setuptools import find_packages, setup
    from os.path import dirname

    def get_version(filename):
        with open(filename) as fh:
            metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", fh.read()))
            return metadata['version']

    setup(
        name='CarPI-info',
        version=get_version(dirname(__file__) + '/carpi_info/__init__.py'),
        url='https://github.com/erikvip/carpi-info',
        license='MIT',
        author_email='email@example.com',
        description='Basic plugin example',
        packages=find_packages(),
        zip_safe=False,
        include_package_data=True,
        install_requires=[
            'Kivy >= 1.9.0',
        ],
        entry_points={
            'carpi.plugin': [
                'info = carpi_info',
            ],
        }
    )
```

**plugin_name/__init__.py**:

This contains our plugin metadata, configuration and launch method. 

```python
    from __future__ import unicode_literals
    from os.path import dirname

    __version__ = '0.1.1'
    __name__ = "Info"
    __title__ = "System Information"
    __icon__ = dirname(__file__) + "/icon.png"

    def launch():
        from .main import CarPI_info as info
        return info().build()
```

Note the *from .main import CarPI_info as info*.  You can name this however you like, but we must return a Kivy Screen widget. the *.main* package will load the file main.py, which contains our main plugin code.

