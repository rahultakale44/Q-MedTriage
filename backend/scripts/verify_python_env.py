"""
Verify that the correct Python environment is being used.
This script should be run from a fresh terminal to test the permanent configuration.
"""
import sys
import os

print("=" * 70)
print("PYTHON ENVIRONMENT VERIFICATION")
print("=" * 70)

# Python executable and version
print(f"\n✓ Python Executable:\n  {sys.executable}")
print(f"\n✓ Python Version:\n  {sys.version}")

# Check if running from .venv
expected_venv_path = os.path.join(os.getcwd(), ".venv", "Scripts", "python.exe")
is_correct_venv = os.path.normpath(sys.executable).lower() == os.path.normpath(expected_venv_path).lower()

if is_correct_venv:
    print(f"\n✅ CORRECT: Using project .venv Python")
else:
    print(f"\n❌ WRONG: Not using project .venv Python")
    print(f"   Expected: {expected_venv_path}")
    print(f"   Actual:   {sys.executable}")

# Qiskit version and location
print("\n" + "-" * 70)
try:
    import qiskit
    print(f"\n✓ Qiskit Version:\n  {qiskit.__version__}")
    print(f"\n✓ Qiskit Location:\n  {qiskit.__file__}")
    
    # Check if Qiskit is from .venv
    expected_qiskit_path = os.path.join(os.getcwd(), ".venv", "Lib", "site-packages", "qiskit")
    is_correct_qiskit = qiskit.__file__.lower().startswith(expected_qiskit_path.lower())
    
    if is_correct_qiskit:
        print(f"\n✅ CORRECT: Using Qiskit from project .venv")
    else:
        print(f"\n❌ WRONG: Using Qiskit from different location")
        print(f"   Expected path prefix: {expected_qiskit_path}")
    
    # Test Qiskit import functionality
    print("\n" + "-" * 70)
    print("\n✓ Testing Qiskit Import...")
    from qiskit import QuantumCircuit
    from qiskit_machine_learning.kernels import FidelityQuantumKernel
    print("  ✅ Qiskit imports successfully")
    print("  ✅ Qiskit Machine Learning available")
    
except ImportError as e:
    print(f"\n❌ ERROR: Failed to import Qiskit")
    print(f"   {e}")

# Pip location
print("\n" + "-" * 70)
import subprocess
result = subprocess.run([sys.executable, "-m", "pip", "-V"], 
                       capture_output=True, text=True, shell=False)
print(f"\n✓ Pip Info:\n  {result.stdout.strip()}")

expected_pip_path = os.path.join(os.getcwd(), ".venv", "Lib", "site-packages", "pip")
is_correct_pip = expected_pip_path.lower() in result.stdout.lower()

if is_correct_pip:
    print(f"\n✅ CORRECT: Using pip from project .venv")
else:
    print(f"\n❌ WRONG: Using pip from different location")

# Summary
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

if is_correct_venv and is_correct_qiskit and is_correct_pip:
    print("\n✅ ALL CHECKS PASSED")
    print("   The project is correctly using the .venv Python environment.")
    print("   Ready to run QSVM training!")
else:
    print("\n❌ CONFIGURATION ISSUE DETECTED")
    print("   The project may not be using the correct Python environment.")
    print("   Please check VS Code Python interpreter settings.")

print("\n" + "=" * 70)
