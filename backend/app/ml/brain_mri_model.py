import json
from pathlib import Path

import torch
import torch.nn as nn
from torchvision.models import (
    convnext_tiny,
    ConvNeXt_Tiny_Weights
)
from PIL import Image

from app.ml.transforms import brain_mri_transform


class BrainMRIModel:

    def __init__(self):

        # Device
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )

        # Base project directory
        BASE_DIR = Path(__file__).resolve().parents[2]

        # Paths
        self.model_path = (
            BASE_DIR /
            "ml_weights" /
            "brain_mri" /
            "best_convnext_tiny_finetuned.pth"
        )

        self.class_path = (
            BASE_DIR /
            "ml_weights" /
            "brain_mri" /
            "class_names.json"
        )

        # Load class names
        with open(self.class_path, "r") as f:
            self.class_names = json.load(f)

        # Load model
        self.model = self._load_model()

        print("✅ Brain MRI Model Loaded Successfully")
    

    def _load_model(self):

        model = convnext_tiny(weights=ConvNeXt_Tiny_Weights.DEFAULT)

        model.classifier[2] = nn.Linear(768, len(self.class_names))

        state_dict = torch.load(self.model_path,map_location=self.device,weights_only=True)

        model.load_state_dict(state_dict)

        model.to(self.device)

        model.eval()

        return model

    def predict(self, image: Image.Image):

    # Apply preprocessing
        image = brain_mri_transform(image)

    # Add batch dimension
        image = image.unsqueeze(0).to(self.device)

        with torch.no_grad():

            outputs = self.model(image)

            probabilities = torch.softmax(outputs, dim=1)
 
            confidence, predicted = torch.max(probabilities, dim=1)

        predicted_class = self.class_names[predicted.item()]

        return {
            "prediction": predicted_class,
            "confidence": round(confidence.item() * 100, 2),
            "probabilities": {
                self.class_names[i]: round(probabilities[0][i].item() * 100, 2)
                for i in range(len(self.class_names))
        }
    }

     
    

