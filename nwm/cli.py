import os
import click

from . import __version__
from nwm import NwmHs


@click.command()
@click.version_option(version=__version__)
@click.option(
    "--archive",
    default="harvey",
    help="Archive type for data download, including harvey, irma, florence, and rolling.",
    show_default="harvey"
)
@click.option(
    "--config",
    default="short_range",
    help="Configuration type for data download, including short_range, medium_range, long_range, and analysis_assim.",
    show_default="short_range"
)
@click.option(
    "--geom",
    default="channel_rt",
    help="Geometry type for data download, including channel_rt, land, reservoir, and forcing.",
    show_default="channel_rt"
)
@click.option(
    "--variable",
    default="streamflow",
    help="Variable type for data download, such as streamflow and velocity.",
    show_default="streamflow"
)
@click.option(  # TODO fix int input issue
    "--comid",
    default='5781915',
    help="COMID for a river reach (e.g. 5781915) or a grid (e.g. 1635, 2030)",
    show_default="5781915",

)
@click.option(
    "--init_time",
    metavar="<int>",
    default=0,
    help="Initiation time for data download, integer value from 0 to 23 (hr).",
    show_default="0",
)
@click.option(
    "--time_lag",
    metavar="<int>",
    default=0,
    help="Time lag for data download, integer value as 0, 6, or 12 (hr).",
    show_default="0",
)
@click.option(
    "--start_date",
    metavar="YYYY-MM-DD",
    default="2017-08-23",
    help="Start date for data download.",
    show_default="2017-08-23",
)
@click.option(
    "--end_date",
    metavar="YYYY-MM-DD",
    default="2017-09-06",
    help="End date for data download.",
    show_default="2017-09-06",
)
@click.argument(
    'output',
    type=click.Path(exists=False)
)
def main(archive, config, geom, variable, init_time, time_lag, comid, start_date, end_date, output):
    comid_list = list(map(int, comid.split(',')))
    NwmHs().get_data(archive=archive, config=config, geom=geom, variable=variable,
                     comid=comid_list, init_time=init_time, time_lag=time_lag,
                     start_date=start_date, end_date=end_date, output=output)
    if os.path.isfile(output):
        print('Done')
