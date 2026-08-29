"""
Q-MedTriage Inference Module

Provides end-to-end inference pipeline from chest X-ray to classification.

NOTE: Heavy imports (ChestXRayInference) are NOT imported by default to avoid
eager loading of Qiskit and other ML dependencies. This allows lightweight
components like ChestXRayValidator to be imported independently.

Usage:
    # For validator (lightweight):
    from src.inference.chest_xray_validator import ChestXRayValidator
    
    # For inference (heavy, loads all ML models):
    from src.inference.predict import ChestXRayInference
"""

# DO NOT eagerly import heavy dependencies here
# This allows chest_xray_validator to be imported without loading:
# - ResNet50
# - Classical SVM
# - Quantum SVM
# - Qiskit
# - PCA models

__all__ = ["ChestXRayInference", "ChestXRayValidator"]

# Lazy import pattern - only load when accessed
def __getattr__(name):
    """Lazy import to avoid loading heavy dependencies at package initialization."""
    if name == "ChestXRayInference":
        from .predict import ChestXRayInference
        return ChestXRayInference
    elif name == "ChestXRayValidator":
        from .chest_xray_validator import ChestXRayValidator
        return ChestXRayValidator
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
