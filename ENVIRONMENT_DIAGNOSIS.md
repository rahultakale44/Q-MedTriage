# Python/Qiskit Environment Diagnosis
**Date**: 2026-08-26  
**Issue**: QSVM training fails with `TypeError: Too few arguments for collections.abc.Callable`

---

## DIAGNOSIS SUMMARY

### ✅ ROOT CAUSE IDENTIFIED
**The virtual environment (.venv) exists and is correctly configured with Qiskit, BUT PowerShell is NOT using it.**

---

## DETAILED FINDINGS

### A. Is python actually using .venv?
**❌ NO** - The `python` command resolves to **global Python 3.10.0**, not the `.venv` Python 3.14.4

**Evidence**:
```
Command: python -c "import sys; print(sys.executable)"
Result: C:\Users\Rahul\AppData\Local\Programs\Python\Python310\python.exe
```

**PowerShell Resolution**:
```
Get-Command python
Path: C:\Users\Rahul\AppData\Local\Programs\Python\Python310\python.exe
Version: 3.10.0
```

**Virtual Environment Status**:
```
$env:VIRTUAL_ENV = (empty/not set)
```

The terminal prompt shows `(.venv)` but **the environment is NOT actually activated**.

---

### B. Is Qiskit installed inside .venv or global Python 3.10?
**✅ Qiskit IS installed in BOTH locations**:

#### Global Python 3.10.0:
- **Location**: `C:\Users\Rahul\AppData\Local\Programs\Python\Python310\lib\site-packages`
- **Qiskit**: 2.5.2
- **NumPy**: 2.2.6
- **SciPy**: 1.15.3
- **Qiskit-Aer**: 0.17.2
- **Qiskit-Machine-Learning**: 0.9.1
- **Pip**: 21.2.3 (old version)
- **Import Status**: ❌ FAILS with `TypeError: Too few arguments for collections.abc.Callable`

#### .venv Python 3.14.4:
- **Location**: `D:\Q-MedTriage\.venv\Lib\site-packages`
- **Qiskit**: 2.5.2
- **NumPy**: 2.5.2
- **SciPy**: 1.18.1
- **Qiskit-Aer**: 0.17.2
- **Qiskit-Machine-Learning**: 0.9.1
- **Scikit-learn**: 1.9.0
- **Import Status**: ✅ WORKS - Qiskit imports successfully

**Test Results**:
```bash
# Global Python 3.10 - FAILS
python -c "import qiskit"
>>> TypeError: Too few arguments for collections.abc.Callable

# .venv Python 3.14 - WORKS
.\.venv\Scripts\python.exe -c "import qiskit; print(qiskit.__version__)"
>>> Qiskit: 2.5.2
>>> Qiskit path: D:\Q-MedTriage\.venv\Lib\site-packages\qiskit\__init__.py
```

---

### C. What exact Python version is .venv using?
**Python 3.14.4**

**Configuration** (`.venv/pyvenv.cfg`):
```ini
home = C:\Users\Rahul\AppData\Local\Programs\Python\Python314
include-system-site-packages = false
version = 3.14.4
executable = C:\Users\Rahul\AppData\Local\Programs\Python\Python314\python.exe
```

**Verification**:
```
.\.venv\Scripts\python.exe --version
Python 3.14.4 (tags/v3.14.4:23116f9, Apr  7 2026, 14:10:54) [MSC v.1944 64 bit (AMD64)]
```

---

### D. What exact Qiskit version is installed?
**Qiskit 2.5.2** (in both global Python 3.10 and .venv Python 3.14)

**Dependencies**:
- qiskit: 2.5.2
- qiskit-aer: 0.17.2
- qiskit-machine-learning: 0.9.1

---

### E. Are packages mutually compatible?

#### Global Python 3.10.0 Environment:
**❌ INCOMPATIBLE** - Qiskit 2.5.2 has type annotation issues with Python 3.10

#### .venv Python 3.14.4 Environment:
**✅ COMPATIBLE** - All packages work correctly:
- Python 3.14.4
- Qiskit 2.5.2 (imports successfully)
- NumPy 2.5.2
- SciPy 1.18.1
- Scikit-learn 1.9.0
- Qiskit-Aer 0.17.2
- Qiskit-Machine-Learning 0.9.1

---

## THE ACTUAL PROBLEM

**The `.venv` virtual environment is NOT activated in PowerShell**, even though the prompt shows `(.venv)`.

**Why the training fails**:
1. User runs: `python src/models/train_quantum_svm.py`
2. PowerShell resolves `python` → global Python 3.10.0
3. Python 3.10 tries to import Qiskit from its global site-packages
4. Qiskit 2.5.2 has type annotation incompatibility with Python 3.10's typing system
5. **Immediate crash**: `TypeError: Too few arguments for collections.abc.Callable`

**Why it SHOULD work**:
- The `.venv` has Python 3.14.4 with Qiskit 2.5.2 correctly installed
- Qiskit imports successfully in Python 3.14.4
- All required packages are present and compatible

---

## RECOMMENDED FIX

### ✅ CLEANEST SOLUTION: Activate the Virtual Environment Properly

**No rebuild necessary.** The `.venv` is correctly configured and functional.

**Steps**:

1. **Activate the virtual environment** in PowerShell:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

2. **Verify activation**:
   ```powershell
   # Should show .venv path
   $env:VIRTUAL_ENV
   
   # Should show Python 3.14.4 in .venv
   python -c "import sys; print(sys.executable)"
   
   # Should import successfully
   python -c "import qiskit; print(qiskit.__version__)"
   ```

3. **Run QSVM training**:
   ```powershell
   python src/models/train_quantum_svm.py
   ```

**Expected Result**: Training runs successfully with 500-sample stratified subset.

---

## ALTERNATIVE: Use Explicit .venv Python Path

If activation fails or is blocked by PowerShell execution policy, run training directly with the `.venv` Python executable:

```powershell
.\.venv\Scripts\python.exe src/models/train_quantum_svm.py
```

This bypasses the need for activation and uses the correct Python 3.14.4 environment directly.

---

## VERIFICATION CHECKLIST

After activation or using explicit path:
- [ ] `python --version` shows Python 3.14.4
- [ ] `$env:VIRTUAL_ENV` shows `D:\Q-MedTriage\.venv`
- [ ] `python -c "import qiskit; print(qiskit.__version__)"` prints `2.5.2`
- [ ] `python src/models/train_quantum_svm.py` runs without import errors

---

## DO NOT REBUILD .venv

**The virtual environment is correctly configured and functional.**

- ✅ Python 3.14.4 installed
- ✅ Qiskit 2.5.2 installed and working
- ✅ All dependencies present (numpy, scipy, scikit-learn, qiskit-aer, qiskit-machine-learning)
- ✅ Qiskit imports successfully from .venv

**The ONLY issue is that PowerShell is not using the activated environment.**

---

## FALLBACK: Rebuild with Python 3.12 (ONLY IF ACTIVATION FAILS)

**If activation consistently fails** (PowerShell execution policy restrictions, corrupted activation scripts), then rebuild `.venv` with Python 3.12 as originally requested:

```powershell
# Remove old .venv
Remove-Item -Recurse -Force .venv

# Create new .venv with Python 3.12
py -3.12 -m venv .venv

# Activate
.\.venv\Scripts\Activate.ps1

# Install packages
pip install --upgrade pip
pip install qiskit==2.5.2
pip install qiskit-aer==0.17.2
pip install qiskit-machine-learning==0.9.1
pip install numpy scipy scikit-learn
pip install pytest pillow matplotlib
```

**BUT: Try activation first. Rebuilding is unnecessary if activation works.**

---

## SUMMARY FOR USER APPROVAL

**Status**: Environment diagnosis complete.

**Finding**: `.venv` is correctly configured with Python 3.14.4 and Qiskit 2.5.2, but PowerShell is not using it (using global Python 3.10 instead).

**Recommended Fix**: Activate `.venv` properly or use explicit `.venv` Python path.

**No rebuild necessary** unless activation fails.

**Preserved**: All project code and data (`src/`, `data/`, `results/`, `models/`, `tests/`, `notebooks/`) remain unchanged.

**Next Step**: Await user approval to proceed with activation test and QSVM training.
