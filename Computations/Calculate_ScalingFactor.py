# Performs a scaling factor calculation for the given data
from TweezerPy.core.scaling_factor_helpers import ScalingFactorHelperFunctions
import pandas as pd
import argparse

ScalingFactorCalculator = ScalingFactorHelperFunctions()

def main():
    distance_dict = {}
    # Argument parser setup
    parser = argparse.ArgumentParser(description='Calculate scaling factor for the given data')
    parser.add_argument('--input', help='Input folder containing the images')
    parser.add_argument('--output', help='Output file to store the scaling factor')
    parser.add_argument('--plot', help='Plot specified sample images', nargs='*', default=None)
    args = parser.parse_args()
    
    # Read images into a dictionary
    data = ScalingFactorCalculator.read_images_to_arrays(args.input)
    for image_name in data:
        images = ScalingFactorCalculator.preprocess_image(data[image_name])
        lines = ScalingFactorCalculator.detect_lines(images[2])
        axis = 'x' if image_name.startswith('x') else 'y'
        distance = ScalingFactorCalculator.calculate_distances(lines,axis)
        distance_dict[image_name] = distance

    # Save distances to the output file
    pd.DataFrame.from_dict(distance_dict, orient='index').to_csv(args.output, header=False)
    print(f"Scaling factors saved to '{args.output}'")
    # Plotting specific sample images
    if args.plot:
        for image_name in args.plot:
            if image_name in data:
                images = ScalingFactorCalculator.preprocess_image(data[image_name])
                lines = ScalingFactorCalculator.detect_lines(images[2])
                ScalingFactorCalculator.draw_and_plot(images[0],images[1],images[2],images[3],lines)
                
            else:
                print(f"Image '{image_name}' not found in the input folder.")
                
        
if __name__ == '__main__':
    main()
