.. image:: _static/nwm_logo.png
    :align: center
    :scale: 120%
    :alt: nwm
    :target: https://nwm.readthedocs.io/


nwm package provides a set of functions that allows downloading of the `National Water Model
(NWM) <https://water.noaa.gov/about/nwm>`_ datasets for data analysis and visualization.
These functions were implemented using the API from the
`HydroShare National Water Model Web App <https://hs-apps.hydroshare.org/apps/nwm-forecasts/>`_.

nwm package includes a Basic Data Interface (BDI),
which converts the NWM dataset into a reusable, plug-and-play data component for
`Community Surface Dynamics Modeling System (CSDMS) <https://csdms.colorado.edu/wiki/Main_Page>`_ modeling framework.
This BDI was implemented using `Basic Model Interface (BMI) <https://bmi.readthedocs.io/en/latest/>`_
library specification created by CSDMS.


Getting Started
===============

Installation
++++++++++++

.. code-block:: console

    $ pip install nwm


Download NWM Data
+++++++++++++++++++++

"NwmHs" class downloads and stores the NWM data as an xarray object for visualization or analysis.

.. code-block:: python

    import matplotlib.pyplot as plt
    from nwm import NwmHs

    # get data from National water model HydroShare App
    dataset = NwmHs().get_data(archive='harvey', config='short_range', geom='channel_rt',
                               variable='streamflow', comid=(5781915,), init_time=0, start_date='2017-08-23')

    # show metadata
    dataset.attrs

    # plot data
    dataset.plot()
    plt.ylabel('{}({})'.format(dataset.variable_unit_name,dataset.variable_unit))
    plt.title('{}; {}'.format(dataset.archive.upper(), dataset.site_name))


Parameter settings
+++++++++++++++++++
"get_data()" method includes multiple parameters for NWM data download. Details for each parameter are listed below.

* **archive**:
    * description:The archived data source of the forecast.
    * values:

* **config**:
    * description:
    * values:

* **geom**:
    * description:
    * values:

* **variable**:
    * description:
    * values:

* **comid**:
    * description:
    * values:

* **init_time**:
    * description:
    * values:

* **time_lag**:
    * description:
    * values:

* **start_date**:
    * description:
    * values:

* **end_date**:
    * description:
    * values:

* **output**:
    * description:
    * values:







