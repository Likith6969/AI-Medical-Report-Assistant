"""
Confusion Matrix Generator for Presentation Defense
"""
from typing import List, Dict, Any


def generate_confusion_matrix_data(labels: List[str], matrix: List[List[int]]) -> Dict[str, Any]:
    """Formats confusion matrix for Chart.js / Seaborn visual rendering."""
    return {
        "labels": labels,
        "matrix": matrix
    }
