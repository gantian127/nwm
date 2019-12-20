# nwm
[![Documentation Status](https://readthedocs.org/projects/ansicolortags/badge/?version=latest)](https://readthedocs.org/)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/gantian127/nwm/blob/master/LICENSE.txt)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/)



Python library to fetch and process the National Water Model (NWM) NetCDF datasets. 

## Get Started



Install package

```
$ python setup.py install nwm
```

Example 

```python
import matplotlib.pyplot as plt
from nwm import Nwm

# get data from National water model HydroShare App
nwm_obj = Nwm()
dataset = nwm_obj.get_data_from_hs()

# show metadata
dataset.attrs

# plot data
dataset.plot()
plt.ylabel('{}({})'.format(dataset.variable_name,dataset.variable_unit))
plt.title('{}; {}'.format(dataset.archive.upper(), dataset.site_name))
```


