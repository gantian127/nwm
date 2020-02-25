.. image:: _static/nwm_logo.png
    :align: center
    :scale: 120%
    :alt: nwm
    :target: https://nwm.readthedocs.io/


nwm package provides a set of functions that allows downloading of the `National Water Model
(NWM) <https://water.noaa.gov/about/nwm>`_ datasets for data analysis and visualization.
These functions were implemented using the API of the
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

"NwmHs" class is used to download and store the NWM data as an xarray object for visualization or analysis.

You can launch binder to test and run the code below. |binder|

.. |binder| image:: https://mybinder.org/badge_logo.svg
 :target: https://mybinder.org/v2/gh/gantian127/nwm/master?filepath=notebooks%2Fnwm.ipynb

.. code-block:: python

    import matplotlib.pyplot as plt
    from nwm import NwmHs

    # get data from National water model HydroShare App
    dataset = NwmHs().get_data(archive='harvey', config='short_range', geom='channel_rt',
                               variable='streamflow', comid=[5781915], init_time=0, start_date='2017-08-23')

    # show metadata
    dataset.attrs

    # plot data
    dataset.plot()
    plt.ylabel('{}({})'.format(dataset.variable_unit_name,dataset.variable_unit))
    plt.title('{}; {}'.format(dataset.archive.upper(), dataset.site_name))


Parameter settings
+++++++++++++++++++
"get_data()" method includes multiple parameters for NWM data download. Details for each parameter are listed below.


* **archive**: The archived data source of the forecast. Options include:
    * rolling: Data for 40-day rolling window
    * florence: Data for Hurricane Florence (2018-09-01 to 2018-10-19)
    * harvey: Data for Hurricane Harvey (2017-08-18 to 2017-09-06)
    * irma: Data for Hurricane Irma (2017-08-29 to 2017-09-15)

* **config**: The configuration of the forecast. Options include:
    * short_range: short range forecast data
    * medium_range: medium range forecast data
    * long_range: long range forecast data
    * analysis_assim: analysis and assimilation data

* **geom**: The geometry of the forecast or model forcing. Options include:
    * channel_rt: river channel stream routing forecast result
    * land: land surface processing forecast result
    * reservoir: 1260 reservoirs forecast result
    * forcing: climate forcing variable data

* **variable**: The variable of the forecast. Variable option is available depending on the specified configuration
  (config) and geometry (geom) settings. Details for variable option are listed in the table below. Please note data may
  be unavailable for some archive options with the following configurations.

    * analysis_assim + channel_rt: "streamflow" or "velocity".
    * analysis_assim + reservoir: "inflow" or "outflow".
    * analysis_assim + land: "SNOWH", "SNEQV", "FSNO", "ACCET", or "SOILSAT_TOP".
    * analysis_assim + forcing: "RAINRATE", "LWDOWN", "PSFC", "Q2D", "SWDOWN", "T2D", "U2D", "V2D".
    * short_range + channel_rt: "streamflow" or "velocity".
    * short_range + reservoir: "inflow" or "outflow".
    * short_range + land: "SNOWH", "SNEQV", "FSNO", "ACCET", or "SOILSAT_TOP".
    * short_range + forcing: "RAINRATE", "LWDOWN", "SWDOWN", "Q2D", "T2D", "U2D", "V2D".
    * medium_range + channel_rt: "streamflow" or "velocity".
    * medium_range + reservoir: "inflow" or "outflow".
    * medium_range + land: "SNOWH", "SNEQV", "FSNO", "ACCET", "SOILSAT_TOP", "UGDRNOFF",
      "ACCECAN","SOIL_T", "SOIL_M", or "CANWAT".
    * medium_range + forcing: "RAINRATE", "LWDOWN", "SWDOWN", "Q2D", "T2D", "U2D", "V2D".
    * long_range + channel_rt: "streamflow".
    * long_range + reservoir: "inflow" or "outflow".
    * long_range + land: "SNEQV", "ACCET", "SOILSAT_TOP", "UGDRNOFF", "SFCRNOFF", "CANWAT".
    * long_range + forcing: N/A (long_range has no forcing files.)

    .. table:: **Variable Options**

        ================    ==========================================    =====================
        Option              Full variable name                            associated geom
        ================    ==========================================    =====================
        streamflow          Stream flow                                   channel_rt
        velocity            Stream Velocity                               channel_rt
        SNOWH               Snow Depth                                    land
        SNEQV               Snow Water Equivalent                         land
        FSNO                Snow Cover                                    land
        ACCET               Accumulated Total ET                          land
        SOILSAT_TOP         Near Surface Soil Saturation                  land
        UGDRNOFF            Accumulated Groundwater Runoff                land
        SFCRNOFF            Accumulated Surface Runoff                    land
        ACCECAN             Accumulated Canopy Evaporation                land
        SOIL_T              Soil Temperature                              land
        SOIL_M              Volumetric Soil Moisture                      land
        CANWAT              Total Canopy Water                            land
        inflow              Inflow                                        reservoir
        outflow             Outflow                                       reservoir
        RAINRATE            Rain Rate                                     forcing
        LWDOWN              Surface Downward Longwave Radiation           forcing
        SWDOWN              Surface Downward Shortwave Radiation Flux     forcing
        Q2D                 2-m Specific Humidity                         forcing
        T2D                 2-m Air Temperature                           forcing
        U2D                 10-m U-component of Wind                      forcing
        V2D                 10-m V-component of Wind                      forcing
        ================    ==========================================    =====================

* **comid**: The identifier of the stream reach, reservoir, or grid cell for the forecast. Options are listed below.
  To find out the corresponding comid of an interested geometry, please use the
  `HydroShare National Water Model Web App <https://hs-apps.hydroshare.org/apps/nwm-forecasts/>`_
  (HydroShare user account is required).

    * single value: identifier for a stream reach or reservoir when "geom" is "channel_rt" or "reservoir". e.g. [5781915]
    * two values: identifier for a grid cell when "geom" is "land" or "forcing".
      Enter the grid south_north index followed by a comma and then the grid west_east index. e.g., [1636, 2036]

* **init_time**: The UTC time of day at which the forecast is initialized, represented by an hour from "00" to "23".
  Time "00" corresponds to 12:00AM, and so forth up to time "23" for 11:00PM.
  Only applicable if "config" is "short_range" or "medium_range".

    * init_time option for short_range: "00", "01",..."23".
    * init_time option for medium_range: "00", "06", "12", "18".

* **time_lag**: The time lag of the long range ensemble forecast. Only applicable if "config" is "long_range".
    * time_lag option for long_range: "t00z", "t06z", "t12z", "t18z".

* **start_date**: The start date of the forecast. A string of the form "YYYY-MM-DD".

* **end_date**: The ending date of the analysis assimilation data. Only applicable if "config" is "analysis_assim".
  A string of the form "YYYY-MM-DD'.

* **output**: The file path of the WaterML file to store the downloaded data.



