import cv2
import csv
import numpy as np
from pathlib import Path
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

class TrackerHelperFunctions:
    def __init__(self):
        pass
    
            
    def calculate_msd(self,values: np.ndarray) -> np.ndarray:
        values = np.array(values)
        N = len(values)
        msd = np.zeros(N)
        for tau in range(N):
            differences = values[tau:] - values[:N-tau]
            msd[tau] = np.mean(differences**2)
        return msd
    
    def plot_msd(self,msd_x:np.ndarray,msd_y:np.ndarray) -> None:
        mean_msdx = msd_x.mean()
        mean_msdy = msd_y.mean()

        fig, axes = plt.subplots(1, 2, figsize=(15, 5))

# Plot Center_X MSD
        axes[0].plot(msd_x)
        axes[0].axhline(mean_msdx, color='r', linestyle='--', label=f'Mean: {mean_msdx:.2f}')
        axes[0].set_title('X MSD over Frames')
        axes[0].set_xlabel(r'$\tau$')
        axes[0].set_ylabel('MSD')
        axes[0].legend()

# Plot Center_Y MSD
        axes[1].plot(msd_y)
        axes[1].axhline(mean_msdy, color='r', linestyle='--', label=f'Mean: {mean_msdy:.2f}')
        axes[1].set_title('Y MSD over Frames')
        axes[1].set_xlabel(r'$\tau$')
        axes[1].set_ylabel('MSD')
        axes[1].legend()

        plt.tight_layout()
        plt.show()
