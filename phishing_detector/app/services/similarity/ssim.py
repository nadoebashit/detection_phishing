from skimage.metrics import structural_similarity as ssim
import cv2
import numpy as np

class SSIMSimilarity:
    @staticmethod
    def compare(image1_path: str, image2_path: str) -> tuple[float, np.ndarray]:
        img1 = cv2.imread(image1_path, cv2.IMREAD_GRAYSCALE)
        img2 = cv2.imread(image2_path, cv2.IMREAD_GRAYSCALE)
        
        if img1 is None or img2 is None:
            raise ValueError("Could not read images.")
            
        img1 = cv2.resize(img1, (1280, 720))
        img2 = cv2.resize(img2, (1280, 720))
        
        score, diff = ssim(img1, img2, full=True)
        diff = (diff * 255).astype("uint8")
        
        return score, diff
        
    @staticmethod
    def is_similar(score: float, threshold: float = 0.85) -> bool:
        return score >= threshold
