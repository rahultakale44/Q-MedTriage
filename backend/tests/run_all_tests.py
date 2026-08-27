"""
Stage 7: Comprehensive Test Suite Runner

Runs all backend tests for Q-MedTriage and generates a test report.
"""

import sys
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))


def run_test_suite(test_file: str, description: str) -> tuple[bool, str]:
    """
    Run a test suite and return success status and output
    
    Args:
        test_file: Path to test file
        description: Human-readable description
    
    Returns:
        (success, output) tuple
    """
    print(f"\n{'='*70}")
    print(f"Running: {description}")
    print(f"{'='*70}")
    
    try:
        result = subprocess.run(
            [sys.executable, test_file],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        # Print output
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        
        success = result.returncode == 0
        
        if success:
            print(f"✓ {description}: PASSED")
        else:
            print(f"✗ {description}: FAILED (exit code: {result.returncode})")
        
        return success, result.stdout + result.stderr
        
    except subprocess.TimeoutExpired:
        print(f"✗ {description}: TIMEOUT (exceeded 5 minutes)")
        return False, "Test timed out"
    except Exception as e:
        print(f"✗ {description}: ERROR ({e})")
        return False, str(e)


def main():
    """Run all Q-MedTriage tests"""
    print("\n" + "="*70)
    print("Q-MEDTRIAGE COMPREHENSIVE TEST SUITE")
    print("Stage 7: Backend Testing & Integration")
    print("="*70)
    
    # Define test suites
    test_suites = [
        # Phase 1: Core ML Pipeline Tests
        ("tests/test_splits.py", "Phase 1: Dataset Splits"),
        ("tests/test_preprocessing.py", "Phase 1: Preprocessing Pipeline"),
        ("tests/test_feature_extraction.py", "Phase 1: Feature Extraction"),
        ("tests/test_pca_reduction.py", "Phase 1: PCA Reduction"),
        ("tests/test_classical_svm.py", "Phase 1: Classical SVM"),
        ("tests/test_quantum_svm.py", "Phase 1: Quantum SVM"),
        
        # Phase 2: Intelligence Layer Tests
        ("tests/test_stage3_faiss.py", "Stage 3: FAISS Index + Embeddings"),
        ("tests/test_stage4_retriever.py", "Stage 4: RAG Retrieval Service"),
        ("tests/test_stage5_gemini.py", "Stage 5: Gemini Synthesis"),
        ("tests/test_stage6_intelligence.py", "Stage 6: /intelligence Endpoint"),
    ]
    
    results = []
    total_tests = 0
    passed_tests = 0
    
    for test_file, description in test_suites:
        test_path = PROJECT_ROOT / test_file
        
        if not test_path.exists():
            print(f"\n⚠ Skipping {description}: File not found ({test_file})")
            continue
        
        success, output = run_test_suite(str(test_path), description)
        results.append((description, success, output))
        total_tests += 1
        if success:
            passed_tests += 1
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUITE SUMMARY")
    print("="*70)
    
    print(f"\nTotal Test Suites: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Success Rate: {passed_tests/total_tests*100:.1f}%")
    
    print(f"\nDetailed Results:")
    print("-"*70)
    for description, success, _ in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status:8} | {description}")
    
    print("="*70)
    
    # Exit with appropriate code
    if passed_tests == total_tests:
        print("\n✅ ALL TESTS PASSED")
        return 0
    else:
        print(f"\n✗ {total_tests - passed_tests} TEST SUITE(S) FAILED")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
