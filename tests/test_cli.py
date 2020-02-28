#!/usr/bin/env python
import os

from click.testing import CliRunner

from nwm.cli import main


def test_command_line_interface():
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output

    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert "version" in result.output


def test_output_argument(tmpdir):
    runner = CliRunner()
    with tmpdir.as_cwd():
        result = runner.invoke(main, ["test.xml"])
        assert result.exit_code == 0
        assert len(os.listdir(tmpdir)) == 1


def test_archive_option(tmpdir):
    runner = CliRunner()
    with tmpdir.as_cwd():
        result = runner.invoke(main, ["--archive=error", "test.xml"])
        assert result.exit_code != 0

        result = runner.invoke(main, ["--archive=harvey", "test.xml"])
        assert result.exit_code == 0


def test_config_option(tmpdir):
    runner = CliRunner()
    with tmpdir.as_cwd():
        result = runner.invoke(main, ["--config=error", "test.xml"])
        assert result.exit_code != 0

        result = runner.invoke(main, ["--config=short_range", "test.xml"])
        assert result.exit_code == 0


def test_geom_option(tmpdir):
    runner = CliRunner()
    with tmpdir.as_cwd():
        result = runner.invoke(main, ["--geom=error", "test.xml"])
        assert result.exit_code != 0

        result = runner.invoke(main, ["--geom=channel_rt", "test.xml"])
        assert result.exit_code == 0


def test_variable_option(tmpdir):
    runner = CliRunner()
    with tmpdir.as_cwd():
        result = runner.invoke(main, ["--variable=error", "test.xml"])
        assert result.exit_code != 0

        result = runner.invoke(main, ["--variable=streamflow", "test.xml"])
        assert result.exit_code == 0


def test_comid_option(tmpdir):
    runner = CliRunner()
    with tmpdir.as_cwd():
        result = runner.invoke(main, ["--comid=error", "test.xml"])
        assert result.exit_code != 0

        result = runner.invoke(main, ["--comid=5781915", "test.xml"])
        assert result.exit_code == 0

        result = runner.invoke(main, ["--comid=1635, 2030", "--geom=forcing", "--variable=RAINRATE", "test.xml"])
        assert result.exit_code == 0


def test_init_time_option(tmpdir):
    runner = CliRunner()
    with tmpdir.as_cwd():
        result = runner.invoke(main, ["--init_time=100", "test.xml"])
        assert result.exit_code != 0

        result = runner.invoke(main, ["--init_time=2", "test.xml"])
        assert result.exit_code == 0


def test_time_lag_option(tmpdir):
    runner = CliRunner()
    with tmpdir.as_cwd():
        result = runner.invoke(main, ["--time_lag=100", "test.xml"])
        assert result.exit_code != 0

        result = runner.invoke(main, ["--time_lag=6", "test.xml"])
        assert result.exit_code == 0


def test_start_date_option(tmpdir):
    runner = CliRunner()
    with tmpdir.as_cwd():
        result = runner.invoke(main, ["--start_date=error", "test.xml"])
        assert result.exit_code != 0

        result = runner.invoke(main, ["--start_date=2017-01-23", "test.xml"])
        assert result.exit_code != 0

        result = runner.invoke(main, ["--start_date=2017-08-23", "test.xml"])
        assert result.exit_code == 0


def test_end_date_option(tmpdir):
    runner = CliRunner()
    with tmpdir.as_cwd():
        result = runner.invoke(main, ["--end_date=error", "test.xml"])
        assert result.exit_code != 0

        result = runner.invoke(main, ["--config=analysis_assim", "--start_date=2017-09-10",
                                      "--end_date=2017-09-06", "test.xml"])
        assert result.exit_code != 0

        result = runner.invoke(main, ["--config=analysis_assim", "--start_date=2017-09-05",
                                      "--end_date=2017-09-06", "test.xml"])
        assert result.exit_code == 0
