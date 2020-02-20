.. image:: _static/nwm_logo.png
    :align: center
    :scale: 85%
    :alt: nwm
    :target: https://nwm.readthedocs.io/


nwm package provides a set of functions that allows downloading of the `National Water Model
(NWM) <https://water.noaa.gov/about/nwm>`_ datasets.

nwm package includes a Basic Data Interface (BDI),
which converts the NWM dataset into a reusable, plug-and-play data component for
`Community Surface Dynamics Modeling System (CSDMS) <https://csdms.colorado.edu/wiki/Main_Page>`_ modeling framework.


Installation
++++++++++++++++

.. code-block::bash
    $ pip install nwm

Getting Started
+++++++++++++++++

**NWM class**

The following code shows how to use NWM class to download and visualize time series data.

.. code-block::python
  :linenos:
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

Additional Resources
++++++++++++++++++++++
- **BMI**
    nwm package implements BDI using `Basic Model Interface (BMI) <https://bmi.readthedocs.io/en/latest/>`_
    library specification created by CSDMS.

- **HydroShare National Water Model Web App**
    nwm package downloads NWM data using the API from the
    `HydroShare National Water Model Web App <https://hs-apps.hydroshare.org/apps/nwm-forecasts/>`_.
    This web app provides both graphical web user interface and API to download NWM datasets.
    To use this web app, it requires a `HydroShare <https://www.hydroshare.org/>`_ user account.






