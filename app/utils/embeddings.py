from typing import List, Optional
import torch
from torchvision import models, transforms

class EmbeddingModel:
    _instance: Optional['EmbeddingModel'] = None
    _initialized_flag: bool = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if EmbeddingModel._initialized_flag:
            return

        self._model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V2)
        self._model = torch.nn.Sequential(*list(self._model.children())[:-1])
        self._preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

        EmbeddingModel._initialized_flag = True

    def embed(self, image_tensor: torch.Tensor) -> List[float]:
        """Embeds the given image tensor using the model."""
        with torch.no_grad():
            embedding = self._model(image_tensor)
    
        if isinstance(embedding, torch.Tensor):
            return embedding.squeeze()
        else:
            raise ValueError("Embedding output is not a PyTorch tensor.")
