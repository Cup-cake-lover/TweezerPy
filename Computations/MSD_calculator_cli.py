import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')

from TweezerPy.core.tracker_helpers import TrackerHelperFunctions

def main()->None:
    # Argument parser setup
    
    parser = argparse.ArgumentParser(description='Calculate MSD for the given data')
    parser.add_argument('--input', help='Input file containing the data')
    parser.add_argument('--output', help='Output file to store the MSD values')
    parser.add_argument('--plot', help='Plot the MSD values', action='store_true')
    args = parser.parse_args()
    
    # Read data from the input file
    df = pd.read_csv(args.input)
    X_values,Y_values = np.array(df['Center_X']),np.array(df['Center_Y'])
    
    
    # Calculate MSD values
    tracker = TrackerHelperFunctions()
    msd_x,msd_y = tracker.calculate_msd(X_values),tracker.calculate_msd(Y_values)
    
    # Save MSD values to the output file
    pd.DataFrame({'MSD_X':msd_x,'MSD_Y':msd_y}).to_csv(args.output,index=False)
    print(f"MSD values saved to '{args.output}'")
    # Plot MSD values
    
    if args.plot:
        tracker.plot_msd(msd_x,msd_y)


if __name__ == '__main__':
    main()