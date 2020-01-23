#!/usr/bin/env python
import os

from click.testing import CliRunner

from nwm.cli import nwm


def test_command_line_interface():
    runner = CliRunner()
    result = runner.invoke(nwm, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output

    result = runner.invoke(nwm, ["--version"])
    assert result.exit_code == 0
    assert "version" in result.output


def test_archive_option():
    runner = CliRunner()
    result = runner.invoke(nwm, ["--archive=error"])
    assert result.exit_code != 0

    result = runner.invoke(nwm, ["--archive=harvey"])
    assert result.exit_code == 0


def test_config_option():
    runner = CliRunner()
    result = runner.invoke(nwm, ["--config=error"])
    assert result.exit_code != 0

    result = runner.invoke(nwm, ["--config=short_range"])
    assert result.exit_code == 0


def test_geom_option():
    runner = CliRunner()
    result = runner.invoke(nwm, ["--geom=error"])
    assert result.exit_code != 0

    result = runner.invoke(nwm, ["--geom=channel_rt"])
    assert result.exit_code == 0


def test_variable_option():
    runner = CliRunner()
    result = runner.invoke(nwm, ["--variable=error"])
    assert result.exit_code != 0

    result = runner.invoke(nwm, ["--variable=streamflow"])
    assert result.exit_code == 0


def test_comid_option():
    runner = CliRunner()
    result = runner.invoke(nwm, ["--comid=error"])
    assert result.exit_code != 0

    result = runner.invoke(nwm, ["--comid=5781915"])
    assert result.exit_code == 0

    result = runner.invoke(nwm, ["--comid=1635, 2030", "--geom=forcing", "--variable=RAINRATE"])
    assert result.exit_code == 0


def test_init_time_option():
    runner = CliRunner()
    result = runner.invoke(nwm, ["--init_time=100"])
    assert result.exit_code != 0

    result = runner.invoke(nwm, ["--init_time=2"])
    assert result.exit_code == 0


def test_time_lag_option():
    runner = CliRunner()
    result = runner.invoke(nwm, ["--time_lag=100"])
    assert result.exit_code != 0

    result = runner.invoke(nwm, ["--time_lag=6"])
    assert result.exit_code == 0


def test_start_date_option():
    runner = CliRunner()
    result = runner.invoke(nwm, ["--start_date=error"])
    assert result.exit_code != 0

    result = runner.invoke(nwm, ["--start_date=2017-01-23"])
    assert result.exit_code != 0

    result = runner.invoke(nwm, ["--start_date=2017-08-23"])
    assert result.exit_code == 0


def test_end_date_option():
    runner = CliRunner()
    result = runner.invoke(nwm, ["--end_date=error"])
    assert result.exit_code != 0

    result = runner.invoke(nwm, ["--config=analysis_assim", "--start_date=2017-09-10", "--end_date=2017-09-06"])
    assert result.exit_code != 0

    result = runner.invoke(nwm, ["--config=analysis_assim", "--start_date=2017-09-05", "--end_date=2017-09-06"])
    assert result.exit_code == 0


def test_output_option(tmpdir):
    runner = CliRunner()
    output = os.path.join(tmpdir, 'test.wml')
    result = runner.invoke(nwm, ["--output={}".format(output)])
    assert result.exit_code == 0
    assert len(os.listdir(tmpdir)) == 1