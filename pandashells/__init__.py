# flake8: noqa

# wrap each of these in try blocks, because I want tools to work with just
# plain python
try:
    from pandashells.lib.outlier_lib import sigma_edit_dataframe
except ImportError:  # pragma no cover
    pass

try:
    from pandashells.lib.lomb_scargle_lib import lomb_scargle
except ImportError:  # pragma no cover
    pass

try:
    from pandashells.lib.utils_lib import Timer
except ImportError:  # pragma no cover
    pass

__version__ = '0.3.0'

