from .nwm import NwmHs
from ._version import get_versions

__all__ = ["NwmHs"]

__version__ = get_versions()['version']
del get_versions
