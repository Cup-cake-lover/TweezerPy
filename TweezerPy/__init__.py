from .core.object_tracker import ObjectTracker
from .core.scaling_factor_helpers import ScalingFactorHelperFunctions
from .core.tracker_helpers import TrackerHelperFunctions

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
# __init__.py

# Import necessary modules and classes

# Define the package version
# Define what is available for import
__all__ = ['ObjectTracker', 'ScalingFactorCalculator', 'TrackerHelperFunctions']