# Wifi Module

## Deps


**Matlab Note:** Initial testing seems like matlabplot sucks on the Pi...the garden-graph package might be better...  
- Matplotlib (Graphing library)
  - libfreetype6-dev (? was not present...)
  - All required libs for matplotlib:
    - numpy
    - dateutil
    - pytz
    - cycler
    - tornado
    - pyparsing
    - libagg
    - freetype (above)
    - png
    - qhull
- **Note:** It might just be easier to install matplotlib with apt instead of pip... it's under python-matplotlib
  - Which works to install, but we need at least version 1.5.0, and apt-get installs 1.4.2...
  - So remember to do *pip install --upgrade matplotlib*
