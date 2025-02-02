import cv2
import csv
import numpy as np
from pathlib import Path
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

class ScalingFactorHelperFunctions:
    def __init__(self):
        pass

    def read_images_to_arrays(self, folder_path: str) -> dict:
        """
        Reads all images from a specified folder and stores them in a dictionary.
        """
        file_arrays = {}
        folder = Path(folder_path)
        for file_path in folder.iterdir():
            if file_path.is_file():
                image = cv2.imread(str(file_path))
                if image is not None:
                    file_arrays[file_path.name] = image  # Use file name as the key
        return file_arrays

    def preprocess_image(self, image: np.ndarray) -> list:
        """
        Applies preprocessing to an image, including blurring, thresholding, and edge enhancement.
        """
        blurred_image = cv2.GaussianBlur(image, (5, 5), 0)
        _, thresholded_image = cv2.threshold(blurred_image, 20, 45, cv2.THRESH_BINARY_INV)
        edges_enhanced = cv2.Canny(thresholded_image, 50, 150, apertureSize=3)
        line_image_enhanced = cv2.cvtColor(image[:, :, 2], cv2.COLOR_GRAY2BGR)
        return [blurred_image, thresholded_image, edges_enhanced, line_image_enhanced]

    def detect_lines(self, edges_enhanced: np.ndarray) -> np.ndarray:
        """
        Detects lines in an edge-enhanced image using the Hough Transform method.
        """
        lines_enhanced = cv2.HoughLines(edges_enhanced, 1, np.pi / 180, 130)
        return lines_enhanced

    def draw_and_plot(self, blurred_image: np.ndarray, thresholded_image: np.ndarray,
                      enhanced_image: np.ndarray, line_image_enhanced: np.ndarray,
                      lines_enhanced: np.ndarray) -> None:
        """
        Draws lines on the enhanced image and plots the blurred, thresholded, 
        and enhanced images with detected lines.
        """
        # Draw lines on the enhanced image
        dim_a, dim_b = enhanced_image.shape[:2]
        if lines_enhanced is not None:
            for rho, theta in lines_enhanced[:, 0]:
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                x1 = int(x0 + dim_b * (-b))
                y1 = int(y0 + dim_a * (a))
                x2 = int(x0 - dim_b * (-b))
                y2 = int(y0 - dim_a * (a))
                cv2.line(line_image_enhanced, (x1, y1), (x2, y2), (0, 0, 255), 3)

        # Plot the images
        plt.figure(figsize=(15, 7))
        plt.subplot(1, 3, 1)
        plt.title("Blurred Image")
        plt.imshow(blurred_image, cmap="bone")
        plt.axis("off")

        plt.subplot(1, 3, 2)
        plt.title("Thresholded Image")
        plt.imshow(thresholded_image, cmap="bone")
        plt.axis("off")

        plt.subplot(1, 3, 3)
        plt.title("Enhanced Detected Lines")
        plt.imshow(cv2.cvtColor(line_image_enhanced, cv2.COLOR_BGR2RGB))
        plt.axis("off")

        plt.tight_layout()
        plt.show()

    def calculate_distances(self, lines: np.ndarray, axis='x') -> list:
        """
        Calculates distances between detected lines along the specified axis (x or y).
        """
        if axis == 'x':
            vertical_lines = [line for line in lines[:, 0] if abs(line[1] - np.pi / 2) > 0.5]
        elif axis == 'y':
            vertical_lines = [line for line in lines[:, 0] if abs(line[1] - np.pi / 2) < 0.5]
        else:
            raise ValueError("Axis must be 'x' or 'y'")

        vertical_lines.sort(key=lambda x: x[0])
        distances = [abs(vertical_lines[i + 1][0] - vertical_lines[i][0]) for i in range(len(vertical_lines) - 1)]
        distances = 1e-6 / np.array(distances)
        return distances
