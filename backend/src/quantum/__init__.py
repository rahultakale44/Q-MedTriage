"""
Quantum Machine Learning Module for Q-MedTriage
"""

try:
    from .qsvm_classifier import QuantumSVM
    __all__ = ["QuantumSVM"]
except ImportError:
    print("Warning: Quantum module requires Qiskit")
    __all__ = []
