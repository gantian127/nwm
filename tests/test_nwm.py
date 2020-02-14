import pytest
import os
from datetime import datetime, timedelta

import xarray

from nwm import NwmHs


# test default argument settings
def test_save_wml_valid_dir(tmpdir):
    dataset = NwmHs().get_data(output=os.path.join(tmpdir, 'test.wml'))

    assert isinstance(dataset, xarray.core.dataarray.DataArray)
    assert len(os.listdir(tmpdir)) == 1


def test_save_wml_invalid_dir(tmpdir):
    dataset = NwmHs().get_data(output=tmpdir)

    assert isinstance(dataset, xarray.core.dataarray.DataArray)
    assert len(os.listdir(tmpdir)) == 0


# test user input for get_data_from_hs
def test_archive():
    with pytest.raises(ValueError):
        NwmHs().get_data(archive='wrong_archive')


def test_config():
    with pytest.raises(ValueError):
        NwmHs().get_data(config='wrong_config')


def test_start_end_date():
    with pytest.raises(ValueError):  # start date format
        NwmHs().get_data(start_date='2017/12/3')

    with pytest.raises(ValueError):  # end date format
        NwmHs().get_data(end_date='2019/12/17')

    for archive in NwmHs.HS_INFO['archive'].values():  # start and end date is within limit
        start_lim = datetime.strptime(NwmHs.HS_INFO['available_date'][archive][0], '%Y-%m-%d')
        end_lim = datetime.strptime(NwmHs.HS_INFO['available_date'][archive][1], '%Y-%m-%d')

        with pytest.raises(ValueError):  # test start date with start limit
            NwmHs().get_data(archive=archive, config='short_range',
                             start_date=(start_lim - timedelta(days=2)).strftime('%Y-%m-%d'))

        with pytest.raises(ValueError):  # test start date with end limit
            NwmHs().get_data(archive=archive, config='short_range',
                             start_date=(end_lim + timedelta(days=2)).strftime('%Y-%m-%d'))

    with pytest.raises(ValueError):  # test end date
        NwmHs().get_data(archive='harvey', config='analysis_assim', start_date='2017-09-10', end_date='2017-09-01')


def test_init_time_and_lag():
    with pytest.raises(ValueError):
        NwmHs().get_data(archive='harvey', config='short_range', init_time=29)

    with pytest.raises(ValueError):
        NwmHs().get_data(archive='harvey', config='medium_range', init_time=20)

    with pytest.raises(ValueError):
        NwmHs().get_data(archive='harvey', config='long_range', time_lag=18)


def test_geom_and_variable():
    with pytest.raises(ValueError):
        NwmHs().get_data(geom='wrong_geom')

    for geom in NwmHs.HS_INFO['geom'].values():
        with pytest.raises(ValueError):
            NwmHs().get_data(archive='harvey', geom=geom, variable='wrong_variable')


def test_comid():
    with pytest.raises(ValueError):  # test comid format as a list of int
        NwmHs().get_data(geom='channel_rt', comid=['1234'])

    with pytest.raises(ValueError):  # test comid format as a list of int
        NwmHs().get_data(geom='channel_rt', comid=[1234.23])

    for geom in ['land', 'forcing']:  # test comid as two int value
        with pytest.raises(ValueError):
            NwmHs().get_data(geom=geom, comid=[1223])

    for geom in ['channel_rt', 'reservoir']:  # test comid as one int value
        with pytest.raises(ValueError):
            NwmHs().get_data(geom=geom, comid=[1232, 1231])


# test http requests for multiple archive options (streamflow variable)

# this is disabled because rolling data availability is not stable
# def test_hs_request_for_rolling():
#     for config in NwmHs.HS_INFO['config'].values():
#
#         start_date = NwmHs.HS_INFO['available_date']['rolling'][0]
#         end_date = NwmHs.HS_INFO['available_date']['rolling'][1]
#         print(config, start_date, end_date)
#         if config != 'medium_range':  # the medium range data doesn't work in HydroShare
#             dataset = NwmHs().get_data(archive='rolling', config=config, geom='channel_rt',
#                                        variable='streamflow', start_date=start_date, end_date=end_date)
#         else:
#             continue
#
#         assert isinstance(dataset, xarray.core.dataarray.DataArray)


def test_hs_request_for_harvey():
    for config in NwmHs.HS_INFO['config'].values():
        start_date = NwmHs.HS_INFO['available_date']['harvey'][0]
        end_date = NwmHs.HS_INFO['available_date']['harvey'][1]
        print(config, start_date, end_date)

        dataset = NwmHs().get_data(archive='harvey', config=config, geom='channel_rt',
                                   variable='streamflow', start_date=start_date, end_date=end_date)

        assert isinstance(dataset, xarray.core.dataarray.DataArray)


def test_hs_request_for_irma():
    for config in NwmHs.HS_INFO['config'].values():
        start_date = NwmHs.HS_INFO['available_date']['irma'][0]
        end_date = NwmHs.HS_INFO['available_date']['irma'][1]
        print(config, start_date, end_date)

        dataset = NwmHs().get_data(archive='irma', config=config, geom='channel_rt',
                                   variable='streamflow', start_date=start_date, end_date=end_date)

        assert isinstance(dataset, xarray.core.dataarray.DataArray)


def test_hs_request_for_florence():
    for config in NwmHs.HS_INFO['config'].values():
        start_date = NwmHs.HS_INFO['available_date']['florence'][0]
        end_date = NwmHs.HS_INFO['available_date']['florence'][1]
        print(config, start_date, end_date)

        dataset = NwmHs().get_data(archive='florence', config=config, geom='channel_rt',
                                   variable='streamflow', start_date=start_date, end_date=end_date)

        assert isinstance(dataset, xarray.core.dataarray.DataArray)
