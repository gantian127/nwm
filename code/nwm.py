# -*- coding: utf-8 -*-
import xarray as xr
import requests
from datetime import datetime, timedelta

from owslib.waterml.wml11 import WaterML_1_1 as wml


class Nwm:
    HS_INFO = {
        'archive': {
            '40-Day Rolling Window': 'rolling',
            'Florence': 'florence',
            'Harvey': 'harvey',
            'Irma': 'irma'
        },

        'available_date': {
            'rolling': [(datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d'),
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
            'Average Snow Temperature': 'SNOWT_AVG'
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
        self.data_array = None
        self.metadata = None

    def get_data_from_hs(self, archive='harvey', config='short_range', geom='channel_rt',
                         variable='streamflow', comid=(5781915,), init_time=0, time_lag=0,
                         start_date='2017-08-23', end_date='2017-09-06',
                         save_wml=True):

        # check user input
        user_input = Nwm._get_hs_user_input(archive, config, geom, variable, comid, init_time,
                                            time_lag, start_date, end_date)
        # get hs wml
        data_array, metadata = Nwm._get_hs_wml(save_wml, user_input)

        # store results
        self.datasets = data_array
        self.metadata = metadata

        return 'Data is downloaded from HydroShare.'

    @staticmethod
    def _get_hs_user_input(archive, config, geom, variable, comid, init_time, time_lag, start_date, end_date):
        # init user input dict
        user_input = {}

        # check archive
        if archive in Nwm.HS_INFO['archive'].values():
            user_input['archive'] = archive
        else:
            raise ValueError('Please set "archive" with the following options: {}'.format(Nwm.HS_INFO['archive']))

        # check config
        if config in Nwm.HS_INFO['config'].values():
            user_input['config'] = config
        else:
            raise ValueError('Please set config with following options: {}'.format(','.join(Nwm.HS_INFO['config'].values())))

        # check time
        try:
            start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
            end_datetime = datetime.strptime(end_date, '%Y-%m-%d')
        except Exception:
            raise ValueError("Incorrect date format, should be YYYY-MM-DD")

        for archive_option in Nwm.HS_INFO['archive'].values():
            if archive == archive_option:
                start_lim = datetime.strptime(Nwm.HS_INFO['available_date'][archive][0], '%Y-%m-%d')
                end_lim = datetime.strptime(Nwm.HS_INFO['available_date'][archive][1], '%Y-%m-%d')

                if start_lim <= start_datetime <= end_lim:
                    user_input['startDate'] = start_date
                else:
                    raise ValueError('Incorrect start date, should between {} and {} for {} archive'.format(
                        Nwm.HS_INFO['available_date'][archive][0], Nwm.HS_INFO['available_date'][archive][1], archive))

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

        elif config == 'long_range':
            if time_lag in list(range(0, 13, 6)):
                user_input['lag'] = 't{:02}z'.format(init_time)
            else:
                raise ValueError('Incorrect time, value should be 0, 6, or 12')

        # check geom and variable
        if geom in Nwm.HS_INFO['geom'].values():
            user_input['geom'] = geom

            for geom_option in Nwm.HS_INFO['geom'].values():
                if geom == geom_option:
                    if variable in Nwm.HS_INFO[geom_option].values():
                        user_input['variable'] = variable
                        break
                    else:
                        raise ValueError('Please set "variable" with following options:{}'.format(Nwm.HS_INFO[geom_option].values()))
        else:
            raise ValueError('Please set "geom" with following options:{}'.format(Nwm.HS_INFO['geom'].values()))

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
            raise ValueError('Please set "comid" as a list of one COMID (e.g. [11359107]) for channel_rt and reservoir '
                             'or two COMID (e.g., [1636,2036]) for land and forcing')

        return user_input

    @staticmethod
    def _get_hs_wml(save_wml, user_input):

        # form the link and make http request
        hs_link = 'https://hs-apps.hydroshare.org/apps/nwm-forecasts/api/GetWaterML/'
        r = requests.get(hs_link, params=user_input,
                         headers={'Authorization': 'Token 2b2c17f99447ad2497c8090569caac530e1ce13a'})

        if r.status_code != 200:
            return 'Failed to download data from HydroShare. {}:{}'.format(r.status_code, r.reason)

        # get time series data from waterML
        series = wml(r.content).response
        var = series.time_series[0]
        records = var.values[0].values
        times = [record.date_time_utc for record in records]
        values = [float(record.value) for record in records]
        data_array = xr.DataArray(values, coords={'time': times}, dims=['time'])

        # get time series metadata from waterML
        metadata = {
            'site_name': var.source_info.site_name,
            'variable_name': var.variable.variable_name,
            'variable_unit': var.variable.unit.abbreviation,
            'value_type': var.variable.value_type,
            'no_data_value': var.variable.no_data_value,
            'method_description': var.values[0].methods[0].description,
            'quality_control_level': var.values[0].qualit_control_levels[0].definition,
        }

        # save waterML file
        if save_wml:
            with open('{}_{}_waterML.xml'.format(user_input['archive'], user_input['COMID']), 'w') as f:
                f.write(r.text)

        return data_array, metadata

    def plot_data_from_hs(self):
        raise NotImplementedError('plot_data_from_hs')

    def get_data_from_noaa(self):
        raise NotImplementedError('get_data_from_noaa')



