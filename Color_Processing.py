import numpy as np 
import cv2


class ColorProcessor:
    def __init__(self):
        pass

    def detect_green_points(self, color_frame):
        # Convert the color frame to HSV (Hue, Saturation, Value) for better color segmentation
        hsv_image = cv2.cvtColor(color_frame, cv2.COLOR_BGR2HSV)
        
        # Define the range for green color in HSV space
        lower_green = np.array([35, 50, 50])  # Lower bound of green
        upper_green = np.array([85, 255, 255])  # Upper bound of green
        
        # Create a mask for green points
        green_mask = cv2.inRange(hsv_image, lower_green, upper_green)
        
        # Find contours of the green regions in the mask
        contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        green_points = []
        for contour in contours:
            if len(contour) >= 6:  # Ensure there are enough points
                for point in contour:
                    green_points.append(point[0])  # Save x, y coordinates of green points
        return green_points