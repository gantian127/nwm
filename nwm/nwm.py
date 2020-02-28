# -*- coding: utf-8 -*-
import xarray as xr
import requests
from datetime import datetime, timedelta

from owslib.waterml.wml11 import WaterML_1_1 as wml


class NwmHs:
    HS_INFO = {
        'archive': {
            '40-Day Rolling Window': 'rolling',
            'Florence': 'florence',
            'Harvey': 'harvey',
            'Irma': 'irma'
        },

        'available_date': {
            'rolling': [(datetime.today() - timedelta(days=24)).strftime('%Y-%m-%d'),
                        datetime.today().strftime('%Y-%m-%d')],
            'florence': ['2018-09-01', '2019-10-19'],
            'harvey': ['2017-08-18', '2017-09-06'],
            'irma': ['2017-08-29', '2017-09-15']
        },

        'geom': {
            'Channel': 'channel_rt',
            'Land': 'land',
            'Reservoir': 'reservoir',
            'Forcing': 'forcing'
        },

        'config': {
            'Analysis and Assimilation': 'analysis_assim',
            'Short Range': 'short_range',
            'Medium Range': 'medium_range',
            'Long Range': 'long_range'
        },

        'land': {
            'Snow Depth': 'SNOWH',
            'Snow Water Equivalent': 'SNEQV',
            'Snow Cover': 'FSNO',
            'Accumulated Total ET': 'ACCET',
            'Near Surface Soil Saturation': 'SOILSAT_TOP',
            'Accumulated Groundwater Runoff': 'UGDRNOFF',
            'Accumulated Surface Runoff': 'SFCRNOFF',
            'Accumulated Canopy Evaporation': 'ACCECAN',
            'Soil Temperature': 'SOIL_T',
            'Volumetric Soil Moisture': 'SOIL_M',
            'Total Canopy Water': 'CANWAT',
        },

        'channel_rt': {
            'Streamflow': 'streamflow',
            'Velocity': 'velocity'
        },

        'reservoir': {
            'Inflow': 'inflow',
            'Outflow': 'outflow'
        },

        'forcing': {
            'Rain Rate': 'RAINRATE',
            'Surface Downward Longwave Radiation': 'LWDOWN',
            'Surface Downward Shortwave Radiation Flux': 'SWDOWN',
            '2-m Specific Humidity': 'Q2D',
            '2-m Air Temperature': 'T2D',
            '10-m U-component of Wind': 'U2D',
            '10-m V-component of Wind': 'V2D'
        },

    }

    def __init__(self):
        self._dataset = None
        self._user_input = None

    @property
    def dataset(self):
        return self._dataset

    @property
    def user_input(self):
        return self._user_input

    def get_data(self, archive='harvey', config='short_range', geom='channel_rt',
                 variable='streamflow', comid=(5781915,), init_time=0, time_lag=0,
                 start_date='2017-08-23', end_date='2017-09-06',
                 output=""):

        # check user input
        user_input = NwmHs._get_hs_user_input(archive, config, geom, variable, comid, init_time,
                                              time_lag, start_date, end_date)
        self._user_input = user_input

        # get hs wml
        data_array = NwmHs._get_hs_wml(output, user_input)

        # store results
        self._dataset = data_array

        return data_array

    @staticmethod
    def _get_hs_user_input(archive, config, geom, variable, comid, init_time, time_lag, start_date, end_date):
        # init user input dict
        user_input = {}

        # check archive
        if archive in NwmHs.HS_INFO['archive'].values():
            user_input['archive'] = archive
        else:
            raise ValueError('Please set "archive" with the following options: {}.'.format(
                ', '.join(NwmHs.HS_INFO['archive'].values())))

        # check config
        if config in NwmHs.HS_INFO['config'].values():
            user_input['config'] = config
        else:
            raise ValueError('Please set config with following options: {}'.format(
                ', '.join(NwmHs.HS_INFO['config'].values())))

        # check time
        try:
            start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
            end_datetime = datetime.strptime(end_date, '%Y-%m-%d')
        except Exception:
            raise ValueError("Incorrect date format, should be YYYY-MM-DD")

        for archive_option in NwmHs.HS_INFO['archive'].values():
            if archive == archive_option:
                start_lim = datetime.strptime(NwmHs.HS_INFO['available_date'][archive][0], '%Y-%m-%d')
                end_lim = datetime.strptime(NwmHs.HS_INFO['available_date'][archive][1], '%Y-%m-%d')

                if start_lim <= start_datetime <= end_lim:
                    user_input['startDate'] = start_date
                else:
                    raise ValueError('Incorrect start date, should between {} and {} for {} archive'.format(
                        NwmHs.HS_INFO['available_date'][archive][0], NwmHs.HS_INFO['available_date'][archive][1],
                        archive))

                if config == 'analysis_assim':
                    if start_datetime < end_datetime:
                        user_input['endDate'] = end_date
                    else:
                        raise ValueError('Incorrect start date, should be earlier than end date.')
                break

        # check initiation time and time lag
        if config == 'short_range':
            if init_time in list(range(24)):
                user_input['time'] = '{:02}'.format(init_time)
            else:
                raise ValueError('Incorrect time, value should be between 0 and 23')

        elif config == 'medium_range':
            if init_time in list(range(0, 19, 6)):
                user_input['time'] = '{:02}'.format(init_time)
            else:
                raise ValueError('Incorrect time, value should be 0, 6, 12, or 18.')

        if time_lag in list(range(0, 13, 6)):
            user_input['lag'] = 't{:02}z'.format(init_time)
        else:
            raise ValueError('Incorrect time, value should be 0, 6, 12, or 18.')

        # check geom and variable
        if geom in NwmHs.HS_INFO['geom'].values():
            user_input['geom'] = geom

            for geom_option in NwmHs.HS_INFO['geom'].values():
                if geom == geom_option:
                    if variable in NwmHs.HS_INFO[geom_option].values():
                        user_input['variable'] = variable
                        break
                    else:
                        raise ValueError('Please set "variable" with following options: {}.'.format(
                            ', '.join(NwmHs.HS_INFO[geom_option].values())))
        else:
            raise ValueError('Please set "geom" with following options: {}.'.format(
                ', '.join(NwmHs.HS_INFO['geom'].values())))

        # check comid
        if isinstance(comid, (int, list, tuple)) and all(isinstance(item, int) for item in comid):
            if geom in ['land', 'forcing'] and len(comid) == 2:
                user_input['COMID'] = ','.join(str(x) for x in comid)
            elif geom in ['channel_rt', 'reservoir'] and len(comid) == 1:
                user_input['COMID'] = str(comid[0])
            else:
                raise ValueError('Please set "comid" as a list of one COMID (e.g. [11359107]) for channel_rt and '
                                 'reservoir or two COMID (e.g., [1636,2036]) for land and forcing')
        else:
            raise ValueError('Please set "comid" as a list of one value (e.g. [11359107]) for channel_rt and reservoir '
                             'or two values (e.g., [1636,2036]) for land and forcing')

        return user_input

    @staticmethod
    def _get_hs_wml(output, user_input):
        # form the link and make http request
        hs_link = 'https://hs-apps.hydroshare.org/apps/nwm-forecasts/api/GetWaterML/'
        r = requests.get(hs_link, params=user_input,
                         headers={'Authorization': 'Token 2b2c17f99447ad2497c8090569caac530e1ce13a'})
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            print('Requested data is not available.\n'
                  'Please check available data options and corresponding parameter settings '
                  'at https://nwm.readthedocs.io/')
            raise

        # get time series data from waterML
        series = wml(r.content).response
        var = series.time_series[0]
        records = var.values[0].values
        times = [record.date_time_utc for record in records]
        values = [float(record.value) for record in records]

        # create data array
        data_array = xr.DataArray(values, coords={'time': times}, dims=['time'])

        data_array.attrs['site_name'] = var.source_info.site_name
        data_array.attrs['variable_name'] = var.variable.variable_name
        data_array.attrs['variable_unit_name'] = var.variable.unit.name
        data_array.attrs['variable_unit'] = var.variable.unit.abbreviation
        data_array.attrs['value_type'] = var.variable.value_type
        data_array.attrs['no_data_value'] = var.variable.no_data_value
        data_array.attrs['method_description']: var.values[0].methods[0].description
        data_array.attrs['quality_control_level']: var.values[0].qualit_control_levels[0].definition
        data_array.attrs['archive'] = user_input['archive']

        # save waterML file
        if output:
            try:
                with open(output, 'w') as f:
                    f.write(r.text)
            except Exception:
                print('Failed to save the data as a waterML file. Please provide a valid file path.'.format(output))

        return data_array
