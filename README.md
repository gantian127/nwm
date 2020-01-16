# nwm
[![Documentation Status](https://readthedocs.org/projects/nwm/badge/?version=latest)](https://nwm.readthedocs.io/en/latest/?badge=latest)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/gantian127/nwm/blob/master/LICENSE.txt)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/gantian127/nwm/master?filepath=notebooks%2Fnwm.ipynb)



Python library to fetch and process the National Water Model (NWM) NetCDF datasets. 

## Get Started



Install package

```
$ python setup.py install nwm
```

Example 

```python
import matplotlib.pyplot as plt
from nwm import NwmHs

# get data from National water model HydroShare App
dataset = NwmHs().get_data()

# show metadata
dataset.attrs

# plot data
dataset.plot()
plt.ylabel('{}({})'.format(dataset.variable_unit_name,dataset.variable_unit))
plt.title('{}; {}'.format(dataset.archive.upper(), dataset.site_name))
```


