"""
Q-MedTriage Inference Module

Provides end-to-end inference pipeline from chest X-ray to classification.
"""

from .predict import ChestXRayInference

__all__ = ["ChestXRayInference"]
