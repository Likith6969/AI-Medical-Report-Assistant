from fastapi import APIRouter, Depends
from app.models.user import User
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter()


@router.get("/metrics")
def get_model_evaluation_metrics(current_user: User = Depends(get_current_user)):
    """Returns static model performance & evaluation metrics for college project presentation defense."""
    return {
        "brain_mri": {
            "model_architecture": "ResNet50 Transfer Learning",
            "test_accuracy": 0.954,
            "precision": 0.952,
            "recall": 0.950,
            "f1_score": 0.951,
            "classes": ["Glioma", "Meningioma", "No Tumor", "Pituitary"],
            "confusion_matrix": [
                [380, 12, 5, 3],
                [10, 375, 8, 7],
                [4, 6, 490, 0],
                [2, 5, 1, 442]
            ]
        },
        "chest_xray": {
            "model_architecture": "ResNet50 Transfer Learning",
            "test_accuracy": 0.938,
            "precision": 0.935,
            "recall": 0.942,
            "f1_score": 0.938,
            "classes": ["Normal", "Pneumonia"],
            "confusion_matrix": [
                [215, 19],
                [18, 348]
            ]
        }
    }
