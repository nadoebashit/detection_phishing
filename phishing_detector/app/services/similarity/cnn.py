import torch
import torchvision.transforms as transforms
from torchvision.models import resnet50, ResNet50_Weights
from PIL import Image
from torch.nn import CosineSimilarity
import numpy as np

class CNNSimilarity:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = resnet50(weights=ResNet50_Weights.IMAGENET1K_V1)
        self.model = torch.nn.Sequential(*(list(self.model.children())[:-1]))
        self.model.to(self.device)
        self.model.eval()
        
        self.preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        self.cos = CosineSimilarity(dim=1, eps=1e-6)

    def extract_features(self, image_path: str) -> list[float]:
        image = Image.open(image_path).convert('RGB')
        input_tensor = self.preprocess(image)
        input_batch = input_tensor.unsqueeze(0).to(self.device)

        with torch.no_grad():
            features = self.model(input_batch)
            
        features = features.squeeze().cpu().numpy()
        return features.tolist()

    def compare(self, features1: list[float], features2: list[float]) -> float:
        t1 = torch.tensor(features1).unsqueeze(0)
        t2 = torch.tensor(features2).unsqueeze(0)
        similarity = self.cos(t1, t2).item()
        return similarity
        
    @staticmethod
    def is_similar(score: float, threshold: float = 0.90) -> bool:
        return score > threshold
        
cnn_similarity = CNNSimilarity()
