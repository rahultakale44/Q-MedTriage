# QSVM Results Validation and Analysis Report
## Q-MedTriage Project - Commit 09

---

## 1. QSVM Run Status

✅ **TRAINING COMPLETED SUCCESSFULLY**

- **Model File**: `models/quantum_svm.pkl` (28,288 bytes, saved 2026-08-26 12:19:41)
- **Results File**: `results/quantum_svm_training_results.json`
- **Process Status**: Completed successfully after extensive computation
- **Model Loadable**: ✅ Yes (verified with joblib)

---

## 2. Actual Saved Results

**From `results/quantum_svm_training_results.json`:**

### Configuration
- **Model**: Quantum SVM (QSVC)
- **Feature Dimension**: 4 (4 qubits)
- **Feature Map**: ZZFeatureMap
- **Repetitions**: 2
- **Entanglement**: linear
- **Kernel**: FidelityQuantumKernel (ComputeUncompute method)
- **Sampler**: StatevectorSampler
- **C Parameter**: 1.0
- **Probability**: Enabled
- **Random State**: 42

### Dataset
- **Full Training Samples**: 4,172
- **QSVM Training Samples Used**: 500 (stratified subset)
- **Test Samples**: 624 (complete test set)

### Training Class Distribution (500 samples)
- **NORMAL**: 128 (25.6%)
- **PNEUMONIA**: 372 (74.4%)

### Test Class Distribution (624 samples)
- **NORMAL**: 234 (37.5%)
- **PNEUMONIA**: 390 (62.5%)

### Metrics
- **Accuracy**: 0.6122 (61.22%)
- **Precision**: 0.6217 (62.17%)
- **Recall**: 0.9692 (96.92%)
- **F1 Score**: 0.7575 (75.75%)
- **ROC-AUC**: 0.4703 (47.03%)

### Confusion Matrix
```
                    Predicted NORMAL    Predicted PNEUMONIA
Actual NORMAL              4                    230
Actual PNEUMONIA          12                    378
```

---

## 3. Confusion Matrix Breakdown

### Raw Values
- **True Negatives (TN)**: 4 — Correctly identified NORMAL
- **False Positives (FP)**: 230 — NORMAL misclassified as PNEUMONIA
- **False Negatives (FN)**: 12 — PNEUMONIA misclassified as NORMAL
- **True Positives (TP)**: 378 — Correctly identified PNEUMONIA
- **Total Samples**: 624

### Prediction Distribution
- **Predicted NORMAL**: 16 samples (2.6%)
- **Predicted PNEUMONIA**: 608 samples (97.4%)

**Finding**: The model is extremely biased toward predicting PNEUMONIA.

---

## 4. Metric Verification

### Manual Calculations

**Accuracy = (TP + TN) / Total**
- = (378 + 4) / 624
- = **0.6121794871794872** ✅ MATCHES

**Precision = TP / (TP + FP)**
- = 378 / (378 + 230)
- = **0.6217105263157895** ✅ MATCHES

**Recall = TP / (TP + FN)**
- = 378 / (378 + 12)
- = **0.9692307692307692** ✅ MATCHES

**F1 Score = 2 × (Precision × Recall) / (Precision + Recall)**
- = 2 × (0.6217 × 0.9692) / (0.6217 + 0.9692)
- = **0.7575150300601202** ✅ MATCHES

### Verification Status
✅ **ALL METRICS VERIFIED** — Confusion matrix perfectly matches reported values.

---

## 5. Medical-Triage Interpretation

### What These Results Mean for Pneumonia Detection

#### Recall = 96.92% (Sensitivity) ✅ EXCELLENT
- The model correctly identifies **96.92%** of actual pneumonia cases
- Only **12 out of 390** pneumonia patients are missed
- **Low false negative rate** is critical in medical screening

#### Specificity = 1.71% ✗ EXTREMELY POOR
- The model correctly identifies only **1.71%** of healthy patients
- **230 out of 234** healthy patients are incorrectly flagged as having pneumonia
- **High false positive rate** would overwhelm clinical resources

#### Precision = 62.17% (Positive Predictive Value) ⚠️ MODERATE
- When the model predicts PNEUMONIA, it's correct **62.17%** of the time
- **37.83%** of positive predictions are false alarms
- 608 positive predictions, but only 378 are actually pneumonia

#### Accuracy = 61.22% ⚠️ BARELY ABOVE MAJORITY CLASS
- Test set has 62.5% pneumonia cases
- The model performs only slightly better than "always predict pneumonia"

### The Trade-off

**Strategy**: The QSVM has adopted an extremely aggressive screening strategy, predicting PNEUMONIA for 97.4% of all cases.

**Benefits**:
- ✅ Catches almost all pneumonia cases (high recall)
- ✅ Minimizes dangerous false negatives

**Costs**:
- ✗ Generates massive false positive rate (98.29% of healthy patients)
- ✗ Would overwhelm clinical resources with unnecessary follow-ups
- ✗ High patient anxiety and unnecessary treatments

### Clinical Context

**⚠️ DISCLAIMER**: This is a research/experimental project only. The QSVM model has NOT been clinically validated and is NOT suitable for medical diagnosis or patient care.

**Theoretical Triage Scenario**:
- In a true screening/triage context, high recall is desirable
- However, 98% false positive rate makes this model clinically impractical
- A useful triage system needs balanced sensitivity and specificity

---

## 6. ROC-AUC Diagnosis

### The Problem: ROC-AUC = 0.47 < 0.5

**ROC-AUC of 0.47 is worse than random guessing (0.5).**

### Root Cause Analysis

#### Confirmed Facts:
1. ✅ The model predicts PNEUMONIA 97.4% of the time
2. ✅ Only 16/624 samples predicted as NORMAL
3. ✅ The model achieves high recall (96.92%) but terrible specificity (1.71%)
4. ✅ Implementation uses `probabilities[:, 1]` (PNEUMONIA probability) for ROC-AUC
5. ✅ Metrics are mathematically correct and verified

#### Most Likely Cause: **Poor Probability Discrimination**

**Explanation**:
- ROC-AUC measures the model's ability to rank positive cases higher than negative cases using probability scores
- The model has learned an "almost always predict PNEUMONIA" strategy
- This means most samples receive similar **high** PNEUMONIA probabilities
- When probability scores are too similar, the ranking ability is destroyed
- Result: ROC-AUC ≈ 0.47, indicating essentially no discriminative power

**Why not exactly 0.5?**
- With 96.92% recall and 1.71% specificity, the model has a slight asymmetry
- If probability calibration is poor (common with quantum kernels + Platt scaling), the ranking can be worse than random

#### Contributing Factors:

**1. Quantum Kernel Probability Calibration**
- QSVC uses the decision function values and applies Platt scaling for probabilities
- The fidelity quantum kernel may produce decision values that don't calibrate well to probabilities
- The quantum kernel is designed for classification, not probability estimation

**2. Training Data Imbalance Effect**
- Training: 74.4% PNEUMONIA (372/500)
- Testing: 62.5% PNEUMONIA (390/624)
- The model learned on highly imbalanced data, reinforcing "predict PNEUMONIA" bias
- Probability calibration was fit to the 74.4% distribution but tested on 62.5%

**3. Small Training Set (500 samples)**
- Quantum SVM trained on only 500 samples (vs 4,172 full training set)
- Limited data for probability calibration, especially for minority class (128 NORMAL)
- SVMs generally need more data for reliable probability estimates

**4. The "Always Positive" Trap**
- The model discovered that predicting PNEUMONIA most of the time yields decent metrics
- High recall: 96.92%
- Moderate F1: 75.75%
- The loss function may not penalize poor probability ranking (only final predictions matter)

### Hypothesis: Not Probability Inversion

If probabilities were simply inverted, ROC-AUC would be 1 - 0.47 = 0.53, which would still be poor but at least above random. The fact that it's 0.47 suggests the probability scores have genuinely poor discriminative power, not just inverted polarity.

### Diagnostic Summary

| Aspect | Status | Evidence |
|--------|--------|----------|
| **Implementation Correctness** | ✅ Correct | Code uses `probabilities[:, 1]` as expected |
| **Metric Calculation** | ✅ Correct | All metrics verified mathematically |
| **Model Behavior** | ✗ Poor | Predicts positive 97.4% of the time |
| **Probability Calibration** | ✗ Poor | Cannot distinguish NORMAL from PNEUMONIA |
| **Clinical Utility** | ✗ None | Worse than random for risk stratification |

---

## 7. Classical SVM vs QSVM Comparison

**From `results/classical_svm_training_results.json`:**

### Dataset
- **Classical SVM**: Trained on full 4,172 samples (validation metrics on 1,044 samples)
- **Quantum SVM**: Trained on 500 stratified samples (test metrics on 624 samples)

**Note**: Classical results show validation metrics (not test metrics), so this is not a perfect apples-to-apples comparison.

### Performance Comparison (Classical Validation vs QSVM Test)

| Metric | Classical SVM (Validation) | Quantum SVM (Test) | Difference |
|--------|---------------------------|-------------------|------------|
| **Accuracy** | 92.05% | 61.22% | -30.83% |
| **Precision** | 95.17% | 62.17% | -32.99% |
| **Recall** | 94.06% | 96.92% | +2.86% |
| **F1 Score** | 94.61% | 75.75% | -18.86% |
| **ROC-AUC** | 97.20% | 47.03% | -50.17% |

### Key Findings

1. **Classical SVM dominates across all metrics except recall**
   - Classical achieves excellent balanced performance (>92% on all metrics)
   - Quantum SVM only beats classical on recall, by a small margin (2.86%)

2. **ROC-AUC gap is catastrophic**
   - Classical: 97.20% (excellent discrimination)
   - Quantum: 47.03% (worse than random)
   - The quantum model cannot properly rank risk

3. **Training Set Size Impact**
   - Classical: Trained on 4,172 samples
   - Quantum: Trained on 500 samples (12% of full dataset)
   - The quantum kernel's computational cost forced subset training

4. **Precision-Recall Trade-off**
   - Classical: Balanced (95.17% precision, 94.06% recall)
   - Quantum: Imbalanced (62.17% precision, 96.92% recall)
   - The quantum model sacrifices precision for slightly higher recall

### Conclusion
The classical RBF-kernel SVM vastly outperforms the Quantum SVM on this task. The quantum model's main advantage (slightly higher recall) is completely overshadowed by its poor precision, accuracy, and catastrophic ROC-AUC.

---

## 8. Saved Model Verification

### File Existence
✅ **Confirmed**: `models/quantum_svm.pkl` exists
- **Size**: 28,288 bytes
- **Last Modified**: 2026-08-26 12:19:41
- **Format**: Joblib pickle file

### Model Loading
✅ **Verified**: Model can be loaded successfully
```python
import joblib
model = joblib.load('models/quantum_svm.pkl')
```

### Model Attributes
- **Type**: `QuantumSVM` (from `src.models.quantum_svm`)
- **is_trained**: `True`
- **feature_dimension**: `4`
- **probability**: `True`
- **reps**: `2`
- **entanglement**: `linear`
- **C**: `1.0`
- **random_state**: `42`

### Integrity Check
✅ **Passed**: All expected attributes present and match configuration

**Note**: There is a minor issue with the `QuantumSVM.load()` class method due to module path checking, but the model can be loaded directly using `joblib.load()` without any problems.

---

## 9. Project Consistency Verification

### ✅ PCA Features
- **Confirmed**: Model uses frozen 4D PCA features from ResNet50
- **Feature source**: `data/pca_features_frozen.npz`
- **Dimension**: 4 (matches quantum circuit qubits)

### ✅ Training Subset
- **Confirmed**: Exactly 500 samples used for QSVM training
- **Method**: Stratified sampling preserving class distribution
- **Original**: 4,172 training samples
- **Subset**: 500 samples (11.98% of full training set)
- **Random state**: 42 (reproducible)

### ✅ Test Set
- **Confirmed**: Complete 624-sample test set evaluated
- **No modifications**: Test set unchanged from original split
- **NORMAL**: 234 samples (37.5%)
- **PNEUMONIA**: 390 samples (62.5%)

### ✅ Result Correspondence
- **Confirmed**: Saved results JSON matches completed run
- **Training config**: Matches hyperparameters
- **Class distributions**: Match actual data splits
- **Metrics**: Match confusion matrix calculations
- **Timestamp**: Results file and model file created at same time

### ✅ Model Correspondence
- **Confirmed**: Saved model matches this training run
- **Attributes**: Match configuration in results JSON
- **Training state**: Correctly set to `is_trained=True`
- **Reproducibility**: Random state 42 ensures reproducibility

---

## 10. Overall Conclusion

### Summary
The Quantum SVM training and evaluation completed successfully with all technical components functioning correctly. However, the model's performance reveals significant limitations in applying quantum kernel methods to this medical imaging classification task.

### Technical Success ✅
- ✅ Quantum circuit implementation correct (4 qubits, ZZFeatureMap, fidelity kernel)
- ✅ Training pipeline executed without errors
- ✅ Model saved and loadable
- ✅ Results documented and reproducible
- ✅ All metrics mathematically verified

### Performance Reality ✗
- ✗ Model adopts extreme "predict positive" bias (97.4% pneumonia predictions)
- ✗ ROC-AUC of 0.47 indicates no discriminative ability (worse than random)
- ✗ Specificity of 1.71% makes model clinically useless
- ✗ Classical SVM outperforms by massive margins across all key metrics
- ✗ High recall (96.92%) is the only positive metric, but comes at unacceptable cost

### Why Did This Happen?

1. **Limited Training Data**: Only 500 samples (especially 128 NORMAL cases) insufficient for quantum kernel
2. **Class Imbalance**: 74.4% PNEUMONIA in training encourages "always positive" strategy
3. **Quantum Kernel Limitations**: Fidelity kernel may not capture relevant patterns in PCA features
4. **Probability Calibration**: Quantum decision values don't translate well to probabilities
5. **Optimization Trap**: Model found a local optimum (high recall) that sacrifices everything else

### Clinical Interpretation ⚠️
This is an **experimental research model** with **zero clinical utility**:
- Cannot be used for patient diagnosis or screening
- False positive rate (98.29%) is clinically disqualifying
- ROC-AUC below random means it cannot stratify patient risk
- Would cause massive harm through misdiagnosis and resource waste

### Research Value ✅
Despite poor performance, this experiment provides valuable insights:
- Demonstrates quantum kernel SVM can be implemented and trained
- Shows quantum methods face significant challenges with medical imaging
- Establishes a baseline for future quantum ML research
- Highlights the need for better quantum feature engineering or different quantum approaches

---

## 11. Recommended Next Steps

### Option A: Accept Current Results (Documentation Focus)
**Time**: Low  
**Effort**: Low

1. Document the QSVM performance honestly in the final project report
2. Emphasize this was a **research exploration**, not a practical implementation
3. Discuss why quantum methods struggled with this task
4. Compare with classical SVM to highlight when classical methods are superior
5. Keep the model and results as-is for demonstration purposes

**Rationale**: The project has successfully demonstrated quantum ML implementation. Poor performance is a legitimate research finding.

---

### Option B: Investigate Hyperparameter Optimization (Research Focus)
**Time**: High  
**Effort**: High  
**Cost**: Expensive (quantum computation time)

1. Try different C values (regularization): `[0.1, 0.5, 1.0, 2.0, 5.0]`
2. Experiment with feature map repetitions: `[1, 2, 3]`
3. Try different entanglement patterns: `['linear', 'full', 'circular']`
4. Test class weight balancing: `class_weight='balanced'`
5. Adjust training subset size if computationally feasible

**Warning**: Each QSVM training run takes hours. Hyperparameter search would take days/weeks.

---

### Option C: Try Alternative Quantum Approaches (Advanced Research)
**Time**: Very High  
**Effort**: Very High

1. **Quantum Feature Engineering**
   - Apply different data preprocessing before PCA
   - Explore amplitude encoding instead of basis encoding
   - Try quantum feature selection techniques

2. **Different Quantum Algorithms**
   - Variational Quantum Classifier (VQC)
   - Quantum Neural Networks (QNN)
   - Quantum Boltzmann Machines

3. **Hybrid Classical-Quantum**
   - Use quantum kernel for feature augmentation, not direct classification
   - Ensemble: Combine quantum and classical predictions

**Warning**: These approaches require significant additional research and development.

---

### Option D: Focus on Classical Methods (Practical Focus)
**Time**: Low  
**Effort**: Low

1. The classical SVM already achieves excellent performance (>92% on all metrics)
2. Focus project documentation on the classical pipeline
3. Position the QSVM as an "exploratory quantum component" in the final report
4. Demonstrate you understand when to choose classical vs quantum methods

**Rationale**: The classical solution works. Don't fix what isn't broken.

---

### **RECOMMENDED**: Option A + Option D

**Justification**:
1. The project's goal was to explore quantum ML, which has been achieved
2. The classical pipeline already performs excellently
3. Poor QSVM performance is a legitimate research finding worth documenting
4. Further quantum optimization would be extremely time-consuming with uncertain payoff
5. Demonstrating technical judgment (when NOT to use quantum) is valuable

**Action Items**:
1. ✅ Keep current QSVM results as-is
2. Document the comparison in project report
3. Discuss lessons learned about quantum vs classical ML
4. Emphasize the classical SVM as the production-ready solution
5. Position QSVM as proof-of-concept for future quantum research

---

## Files Generated

- ✅ `models/quantum_svm.pkl` — Trained quantum SVM model
- ✅ `results/quantum_svm_training_results.json` — Complete metrics and configuration
- ✅ This analysis report

---

**Report Generated**: 2026-08-26  
**Analyst**: Kiro AI  
**Status**: Complete
