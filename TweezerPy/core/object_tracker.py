import cv2
import csv
import numpy as np
from pathlib import Path
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')


class ObjectTracker:
    def __init__(self, tracker_type="CSRT"):
        """
        Initialize the tracker.
        :param tracker_type: Type of tracker to use (default is CSRT).
        """
        if tracker_type == "CSRT":
            self.tracker = cv2.legacy.TrackerCSRT_create()
        else:
            raise ValueError(f"Unsupported tracker type: {tracker_type}")
        self.bbox = None

    def select_roi_from_first_image(self, image_folder: str):
        """
        Automatically selects the first image in the folder and allows manual ROI selection.
        :param image_folder: Path to the folder containing images.
        """
        image_folder_path = Path(image_folder)

        # Ensure folder exists and is not empty
        if not image_folder_path.is_dir():
            raise NotADirectoryError(f"{image_folder_path} is not a valid directory.")
        image_files = sorted(image_folder_path.iterdir())
        if not image_files:
            raise FileNotFoundError(f"No images found in {image_folder_path}.")

        # Select the first image
        first_frame_path = image_files[0]
        first_frame = cv2.imread(str(first_frame_path))
        if first_frame is None:
            raise FileNotFoundError(f"Error loading the first image: {first_frame_path}")

        # Manually select ROI
        self.bbox = cv2.selectROI("Select ROI", first_frame, fromCenter=False, showCrosshair=True)
        cv2.destroyWindow("Select ROI")

        # Initialize the tracker with the first frame and ROI
        self.tracker.init(first_frame, self.bbox)

    def set_roi(self, bbox):
        """
        Set the ROI directly without manual selection.
        :param bbox: Tuple (x, y, width, height).
        """
        self.bbox = bbox

    def track_and_save(self, image_folder: str, csv_file: str):
        """
        Track object across images and save coordinates to a CSV file.
        :param image_folder: Folder containing image frames.
        :param csv_file: Path to save the CSV file.
        """
        image_folder_path = Path(image_folder)
        csv_file_path = Path(csv_file)

        # Validate image folder
        if not image_folder_path.is_dir():
            raise NotADirectoryError(f"{image_folder_path} is not a valid directory.")

        image_files = sorted(image_folder_path.iterdir())
        if not image_files:
            raise FileNotFoundError(f"No images found in {image_folder_path}.")

        # Use the first image as the initial frame
        first_frame_path = image_files[0]
        first_frame = cv2.imread(str(first_frame_path))
        if first_frame is None:
            raise FileNotFoundError(f"Error loading the first image: {first_frame_path}")

        if self.bbox is None:
            raise ValueError("ROI not set. Use 'select_roi_from_first_image' or 'set_roi' to define ROI.")

        # Initialize tracker
        self.tracker.init(first_frame, self.bbox)

        # CSV file to save coordinates
        with csv_file_path.open(mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Frame", "Center_X", "Center_Y"])  # Write header row

            # Iterate through frames and track ROI
            for frame_file in image_files:
                frame = cv2.imread(str(frame_file))
                if frame is None:
                    print(f"Error loading image: {frame_file}")
                    continue

                # Update the tracker
                success, bbox = self.tracker.update(frame)

                # Draw the tracking result
                if success:
                    x, y, w, h = [int(v) for v in bbox]
                    center_x, center_y = x + w // 2, y + h // 2  # Calculate center coordinates

                    # Draw the rectangle and center point
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.circle(frame, (center_x, center_y), 5, (255, 0, 0), -1)

                    # Save coordinates to the CSV file
                    writer.writerow([frame_file.name, center_x, center_y])
                else:
                    cv2.putText(frame, "Tracking failed!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
                    writer.writerow([frame_file.name, "Failed", "Failed"])  # Mark failure in CSV

                # Display the frame
                cv2.imshow("Tracking", frame)

                # Exit if 'q' is pressed
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        cv2.destroyAllWindows()
        print(f"Tracking complete. Coordinates saved to {csv_file_path}.")
