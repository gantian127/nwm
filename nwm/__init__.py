from .nwm import NwmHs
from .bmi import BmiNwmHs
from ._version import get_versions

__all__ = ["NwmHs", "BmiNwmHs"]

__version__ = get_versions()['version']
del get_versions
