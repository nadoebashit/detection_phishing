import imagehash
from PIL import Image

class PHashSimilarity:
    @staticmethod
    def compute_hash(image_path: str) -> str:
        image = Image.open(image_path)
        return str(imagehash.phash(image))

    @staticmethod
    def compare(hash1_str: str, hash2_str: str) -> float:
        hash1 = imagehash.hex_to_hash(hash1_str)
        hash2 = imagehash.hex_to_hash(hash2_str)
        distance = hash1 - hash2
        return float(distance)
        
    @staticmethod
    def is_similar(distance: float, threshold: float = 10.0) -> bool:
        return distance < threshold
