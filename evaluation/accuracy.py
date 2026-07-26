"""
Epoch Loss and Accuracy Curve Plotter
"""
from typing import List, Dict


def format_loss_accuracy_history(epochs: int) -> Dict[str, List[float]]:
    """Returns sample epoch loss & accuracy curves for presentation reporting."""
    return {
        "train_loss": [0.65, 0.42, 0.28, 0.18, 0.12, 0.09],
        "val_loss": [0.68, 0.45, 0.31, 0.22, 0.16, 0.14],
        "train_acc": [0.72, 0.84, 0.89, 0.93, 0.96, 0.97],
        "val_acc": [0.70, 0.82, 0.88, 0.91, 0.94, 0.95]
    }
