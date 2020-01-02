from .nwm import Nwm
from ._version import get_versions

__all__ = ["Nwm"]

__version__ = get_versions()['version']
del get_versions
