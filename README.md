
# TweezerPy

TweezerPy is a Python package designed for analyzing and tracking objects in optical tweezer experiments. It provides tools for object tracking, scaling factor calculations, and Mean Squared Displacement (MSD) analysis.

## Features

- **Object Tracking:** Track objects in an image sequence and save their positions.
- **Scaling Factor Calculation:** Compute the scaling factor of the optical tweezer instrument.
- **MSD Analysis:** Analyze the Mean Squared Displacement (MSD) of tracked objects.

## Installation

To install TweezerPy, use pip (currently not available as PyPI package):

```bash
pip install git+https://github.com/cup-cake-lover/TweezerPy#egg=TweezerPy
```

## Directory Structure

The package is organized as follows:

```
TweezerPy/
├── Computations
│   ├── Calculate_ScalingFactor.py    # Script to calculate scaling factor
│   └── MSD_calculator_cli.py         # Script for MSD calculations
├── TweezerPy
│   ├── __init__.py                   # Package initializer
│   ├── core/
│       ├── object_tracker.py         # Main object tracker implementation
│       ├── scaling_factor_helpers.py # Helper functions for scaling factor
│       └── tracker_helpers.py        # Additional utilities for tracking
├── tests/
│   └── test.ipynb                    # Example notebook for testing
```

## Usage

### Object Tracking

```python
from TweezerPy.core.object_tracker import ObjectTracker

tracker = ObjectTracker(tracker_type="CSRT")
tracker.select_roi_from_first_image("path/to/image_folder")
tracker.track_and_save("path/to/image_folder", "output.csv")
```

Running `tracker.select_roi_from_first_image("path/to/image_folder")` will prompt you to window where you select the 'Region of Interest'; ROI. Afterwards pressing space will directly start the tracking and saves in the output filename provided.

![Sample image](/Example_images/test_image.tif)

### Scaling Factor Calculation 

```python
from TweezerPy.core.scaling_factor_helpers import ScalingFactorHelperFunctions

helper = ScalingFactorHelperFunctions()
images = helper.read_images_to_arrays("path/to/image_folder")
scaling_factor = helper.calculate_distances(lines_detected, axis="x")
```


### MSD Analysis

```python
from TweezerPy.core.tracker_helpers import TrackerHelperFunctions

helper = TrackerHelperFunctions()
msd_x = helper.calculate_msd(values_x)
msd_y = helper.calculate_msd(values_y)
helper.plot_msd(msd_x, msd_y)
```

### Both Scaling Factor and MSD calculations can be done via CLI

```bash
python3 MSD_calculator_cli.py --input '/path/to/file.csv' --output 'output.csv' --plot 
```

```bash
 python3 Calculate_ScalingFactor.py --input '/path/to/folder' --output 'output.csv' --plot 'sample_1.tif' 'sample_2.tif'
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Happy Tracking with TweezerPy!
