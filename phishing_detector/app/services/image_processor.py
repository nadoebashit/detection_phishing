import cv2
import numpy as np
import os

class ImageProcessor:
    @staticmethod
    def process_image(image_path: str, target_size: tuple = (1280, 720)) -> dict:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found at {image_path}")
            
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not read image at {image_path}")
            
        # Resize to standard size (width, height)
        resized = cv2.resize(image, target_size)
        
        # Grayscale conversion
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        
        # Histogram equalization
        equalized = cv2.equalizeHist(gray)
        
        # Noise reduction
        blurred = cv2.GaussianBlur(equalized, (5, 5), 0)
        
        # Edge detection (Canny)
        edges = cv2.Canny(blurred, 100, 200)
        
        return {
            "color": resized,
            "gray": gray,
            "equalized": equalized,
            "blurred": blurred,
            "edges": edges
        }
