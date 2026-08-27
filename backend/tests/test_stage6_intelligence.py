"""
Stage 6: /intelligence FastAPI Endpoint - Comprehensive Tests

Tests the complete integration of Phase 1 classifier with Phase 2 intelligence layer.

Updated to use GrokSynthesizer (Groq-based LLM) instead of GrokSynthesizer.
"""

import sys
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, AsyncMock
from fastapi.testclient import TestClient
from PIL import Image
import io

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================================
# MOCK HELPERS
# ============================================================================

def create_test_image():
    """Create a simple test image"""
    img = Image.new('L', (224, 224), color=128)
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    return img_byte_arr


MOCK_CLASSIFIER_RESULT_PNEUMONIA = {
    "success": True,
    "model": "Classical SVM",
    "model_type": "classical",
    "prediction": 1,
    "prediction_label": "PNEUMONIA",
    "confidence": 0.91,
    "probabilities": {
        "NORMAL": 0.09,
        "PNEUMONIA": 0.91
    },
    "inference_time_ms": 45.2,
    "disclaimer": "AI-assisted triage prediction for research purposes..."
}

MOCK_CLASSIFIER_RESULT_NORMAL = {
    "success": True,
    "model": "Classical SVM",
    "model_type": "classical",
    "prediction": 0,
    "prediction_label": "NORMAL",
    "confidence": 0.87,
    "probabilities": {
        "NORMAL": 0.87,
        "PNEUMONIA": 0.13
    },
    "inference_time_ms": 43.8,
    "disclaimer": "AI-assisted triage prediction for research purposes..."
}

MOCK_RETRIEVED_EVIDENCE = [
    {
        "rank": 1,
        "document_id": "mayo_clinic_pneumonia_symptoms_001",
        "title": "Symptoms of Pneumonia",
        "source": "Mayo Clinic",
        "source_url": "https://www.mayoclinic.org/...",
        "condition": "pneumonia",
        "category": "symptoms",
        "text": "Pneumonia symptoms can vary...",
        "keywords": ["symptoms", "fever", "cough"],
        "distance": 0.31,
        "similarity_score": 0.69
    }
]

MOCK_SYNTHESIS_RESULT = {
    "success": True,
    "answer": "According to Mayo Clinic, pneumonia symptoms can vary from mild to severe.",
    "sources": [
        {
            "title": "Symptoms of Pneumonia",
            "source": "Mayo Clinic",
            "url": "https://www.mayoclinic.org/...",
            "condition": "pneumonia",
            "category": "symptoms"
        }
    ],
    "disclaimer": "This information is for educational purposes only...",
    "retrieved_count": 1,
    "model": "openai/gpt-oss-120b"
}


# ============================================================================
# TEST 1: Endpoint Exists
# ============================================================================

def test_endpoint_exists():
    """TEST 1: /intelligence endpoint exists"""
    print("\n" + "=" * 70)
    print("TEST 1: Endpoint Exists")
    print("=" * 70)
    
    # Import with mocked dependencies
    with patch.dict(os.environ, {"XAI_API_KEY": "test_key", "INTELLIGENCE_ENABLED": "false"}):
        # Mock the imports to avoid loading models
        with patch('src.api.main.ChestXRayInference'):
            with patch('src.api.main.INTELLIGENCE_IMPORTS_AVAILABLE', True):
                from src.api.main import app
                
                client = TestClient(app)
                
                # Check that endpoint is registered
                routes = [route.path for route in app.routes]
                assert "/intelligence" in routes, "/intelligence endpoint not registered"
                print("✓ /intelligence endpoint registered")


# ============================================================================
# TEST 2: Missing Image
# ============================================================================

def test_missing_image():
    """TEST 2: Missing image"""
    print("\n" + "=" * 70)
    print("TEST 2: Missing Image")
    print("=" * 70)
    
    with patch.dict(os.environ, {"XAI_API_KEY": "test_key"}):
        with patch('src.api.main.ChestXRayInference'):
            with patch('src.api.main.INTELLIGENCE_ENABLED', True):
                with patch('src.api.main.PIPELINE_LOADED', True):
                    from src.api.main import app
                    
                    client = TestClient(app)
                    
                    # Test without file
                    response = client.post("/intelligence")
                    assert response.status_code == 422, "Should reject missing file"
                    print("✓ Missing file rejected with 422")


# ============================================================================
# TEST 3: Invalid Image
# ============================================================================

def test_invalid_image():
    """TEST 3: Invalid image"""
    print("\n" + "=" * 70)
    print("TEST 3: Invalid Image")
    print("=" * 70)
    
    with patch.dict(os.environ, {"XAI_API_KEY": "test_key"}):
        with patch('src.api.main.ChestXRayInference'):
            with patch('src.api.main.INTELLIGENCE_ENABLED', True):
                with patch('src.api.main.PIPELINE_LOADED', True):
                    from src.api.main import app
                    
                    client = TestClient(app)
                    
                    # Test with text file (not image)
                    files = {"file": ("test.txt", b"not an image", "text/plain")}
                    response = client.post("/intelligence", files=files)
                    assert response.status_code == 400, "Should reject non-image file"
                    print("✓ Non-image file rejected with 400")


# ============================================================================
# TEST 4: Classifier Integration
# ============================================================================

def test_classifier_integration():
    """TEST 4: Classifier integration"""
    print("\n" + "=" * 70)
    print("TEST 4: Classifier Integration")
    print("=" * 70)
    
    with patch.dict(os.environ, {"XAI_API_KEY": "test_key"}):
        # Mock inference pipeline
        mock_pipeline = Mock()
        mock_pipeline.predict.return_value = MOCK_CLASSIFIER_RESULT_PNEUMONIA
        
        # Mock RAG retriever
        mock_retriever = Mock()
        mock_retriever.is_ready = True
        mock_retriever.retrieve.return_value = MOCK_RETRIEVED_EVIDENCE
        
        # Mock Grok synthesizer
        mock_synthesizer = Mock()
        mock_synthesizer.is_ready = True
        mock_synthesizer.synthesize.return_value = MOCK_SYNTHESIS_RESULT
        
        with patch('src.api.main.ChestXRayInference', return_value=mock_pipeline):
            with patch('src.api.main.RAGRetriever', return_value=mock_retriever):
                with patch('src.api.main.GrokSynthesizer', return_value=mock_synthesizer):
                    with patch('src.api.main.INTELLIGENCE_ENABLED', True):
                        with patch('src.api.main.PIPELINE_LOADED', True):
                            with patch('src.api.main.inference_pipeline', mock_pipeline):
                                with patch('src.api.main.rag_retriever', mock_retriever):
                                    with patch('src.api.main.grok_synthesizer', mock_synthesizer):
                                        from src.api.main import app
                                        
                                        client = TestClient(app)
                                        
                                        # Create test image
                                        img_bytes = create_test_image()
                                        files = {"file": ("test.jpg", img_bytes, "image/jpeg")}
                                        
                                        # Make request
                                        response = client.post("/intelligence", files=files)
                                        
                                        # Verify classifier was called
                                        assert mock_pipeline.predict.called, "Classifier not called"
                                        print("✓ Classifier called")
                                        
                                        # Verify response includes prediction
                                        assert response.status_code == 200
                                        data = response.json()
                                        assert "prediction" in data
                                        assert data["prediction"]["condition"] == "PNEUMONIA"
                                        print("✓ Classifier prediction included in response")


# ============================================================================
# TEST 5: Confidence Preservation
# ============================================================================

def test_confidence_preservation():
    """TEST 5: Classifier confidence preserved"""
    print("\n" + "=" * 70)
    print("TEST 5: Confidence Preservation")
    print("=" * 70)
    
    with patch.dict(os.environ, {"XAI_API_KEY": "test_key"}):
        mock_pipeline = Mock()
        mock_pipeline.predict.return_value = MOCK_CLASSIFIER_RESULT_PNEUMONIA
        
        mock_retriever = Mock()
        mock_retriever.is_ready = True
        mock_retriever.retrieve.return_value = MOCK_RETRIEVED_EVIDENCE
        
        mock_synthesizer = Mock()
        mock_synthesizer.is_ready = True
        mock_synthesizer.synthesize.return_value = MOCK_SYNTHESIS_RESULT
        
        with patch('src.api.main.inference_pipeline', mock_pipeline):
            with patch('src.api.main.rag_retriever', mock_retriever):
                with patch('src.api.main.grok_synthesizer', mock_synthesizer):
                    with patch('src.api.main.INTELLIGENCE_ENABLED', True):
                        with patch('src.api.main.PIPELINE_LOADED', True):
                            from src.api.main import app
                            
                            client = TestClient(app)
                            
                            img_bytes = create_test_image()
                            files = {"file": ("test.jpg", img_bytes, "image/jpeg")}
                            
                            response = client.post("/intelligence", files=files)
                            data = response.json()
                            
                            # Verify confidence is exactly from classifier
                            assert data["prediction"]["confidence"] == 0.91
                            assert data["prediction"]["probabilities"]["PNEUMONIA"] == 0.91
                            print("✓ Classifier confidence preserved: 0.91")


# ============================================================================
# TEST 6: Condition Mapping
# ============================================================================

def test_condition_mapping():
    """TEST 6: Condition mapping"""
    print("\n" + "=" * 70)
    print("TEST 6: Condition Mapping")
    print("=" * 70)
    
    with patch.dict(os.environ, {"XAI_API_KEY": "test_key"}):
        mock_pipeline = Mock()
        mock_retriever = Mock()
        mock_retriever.is_ready = True
        mock_synthesizer = Mock()
        mock_synthesizer.is_ready = True
        mock_synthesizer.synthesize.return_value = MOCK_SYNTHESIS_RESULT
        
        with patch('src.api.main.inference_pipeline', mock_pipeline):
            with patch('src.api.main.rag_retriever', mock_retriever):
                with patch('src.api.main.grok_synthesizer', mock_synthesizer):
                    with patch('src.api.main.INTELLIGENCE_ENABLED', True):
                        with patch('src.api.main.PIPELINE_LOADED', True):
                            from src.api.main import app
                            
                            client = TestClient(app)
                            
                            # Test PNEUMONIA mapping
                            mock_pipeline.predict.return_value = MOCK_CLASSIFIER_RESULT_PNEUMONIA
                            mock_retriever.retrieve.return_value = MOCK_RETRIEVED_EVIDENCE
                            
                            img_bytes = create_test_image()
                            files = {"file": ("test.jpg", img_bytes, "image/jpeg")}
                            
                            response = client.post("/intelligence", files=files)
                            data = response.json()
                            
                            # Check retriever was called with correct condition
                            call_args = mock_retriever.retrieve.call_args
                            assert call_args[1]["condition"] == "pneumonia"
                            print("✓ PNEUMONIA → pneumonia")
                            
                            # Test NORMAL mapping
                            mock_pipeline.predict.return_value = MOCK_CLASSIFIER_RESULT_NORMAL
                            
                            img_bytes = create_test_image()
                            files = {"file": ("test2.jpg", img_bytes, "image/jpeg")}
                            
                            response = client.post("/intelligence", files=files)
                            data = response.json()
                            
                            call_args = mock_retriever.retrieve.call_args
                            assert call_args[1]["condition"] == "normal_chest_xray"
                            print("✓ NORMAL → normal_chest_xray")


# ============================================================================
# TEST 7: RAG Integration
# ============================================================================

def test_rag_integration():
    """TEST 7: RAG integration"""
    print("\n" + "=" * 70)
    print("TEST 7: RAG Integration")
    print("=" * 70)
    
    with patch.dict(os.environ, {"XAI_API_KEY": "test_key"}):
        mock_pipeline = Mock()
        mock_pipeline.predict.return_value = MOCK_CLASSIFIER_RESULT_PNEUMONIA
        
        mock_retriever = Mock()
        mock_retriever.is_ready = True
        mock_retriever.retrieve.return_value = MOCK_RETRIEVED_EVIDENCE
        
        mock_synthesizer = Mock()
        mock_synthesizer.is_ready = True
        mock_synthesizer.synthesize.return_value = MOCK_SYNTHESIS_RESULT
        
        with patch('src.api.main.inference_pipeline', mock_pipeline):
            with patch('src.api.main.rag_retriever', mock_retriever):
                with patch('src.api.main.grok_synthesizer', mock_synthesizer):
                    with patch('src.api.main.INTELLIGENCE_ENABLED', True):
                        with patch('src.api.main.PIPELINE_LOADED', True):
                            from src.api.main import app
                            
                            client = TestClient(app)
                            
                            img_bytes = create_test_image()
                            files = {"file": ("test.jpg", img_bytes, "image/jpeg")}
                            
                            response = client.post("/intelligence", files=files)
                            
                            # Verify RAG retriever was called
                            assert mock_retriever.retrieve.called
                            print("✓ RAG retriever called")
                            
                            # Verify it was called with top_k=5
                            call_args = mock_retriever.retrieve.call_args
                            assert call_args[1]["top_k"] == 5
                            print("✓ top_k=5")
                            
                            # Verify condition filter applied
                            assert call_args[1]["condition"] == "pneumonia"
                            print("✓ Condition filter applied")


# ============================================================================
# TEST 8: Evidence Passed to Grok
# ============================================================================

def test_evidence_passed_to_Grok():
    """TEST 8: Evidence passed to Grok"""
    print("\n" + "=" * 70)
    print("TEST 8: Evidence Passed to Grok")
    print("=" * 70)
    
    with patch.dict(os.environ, {"XAI_API_KEY": "test_key"}):
        mock_pipeline = Mock()
        mock_pipeline.predict.return_value = MOCK_CLASSIFIER_RESULT_PNEUMONIA
        
        mock_retriever = Mock()
        mock_retriever.is_ready = True
        mock_retriever.retrieve.return_value = MOCK_RETRIEVED_EVIDENCE
        
        mock_synthesizer = Mock()
        mock_synthesizer.is_ready = True
        mock_synthesizer.synthesize.return_value = MOCK_SYNTHESIS_RESULT
        
        with patch('src.api.main.inference_pipeline', mock_pipeline):
            with patch('src.api.main.rag_retriever', mock_retriever):
                with patch('src.api.main.grok_synthesizer', mock_synthesizer):
                    with patch('src.api.main.INTELLIGENCE_ENABLED', True):
                        with patch('src.api.main.PIPELINE_LOADED', True):
                            from src.api.main import app
                            
                            client = TestClient(app)
                            
                            img_bytes = create_test_image()
                            files = {"file": ("test.jpg", img_bytes, "image/jpeg")}
                            
                            response = client.post("/intelligence", files=files)
                            
                            # Verify synthesizer was called with retrieved evidence
                            assert mock_synthesizer.synthesize.called
                            call_args = mock_synthesizer.synthesize.call_args
                            
                            # Check that retrieved_results parameter matches what retriever returned
                            passed_evidence = call_args[1]["retrieved_results"]
                            assert passed_evidence == MOCK_RETRIEVED_EVIDENCE
                            print("✓ Retrieved evidence passed to Grok")


# ============================================================================
# TEST 9: Grok Response Integration
# ============================================================================

def test_Grok_response_integration():
    """TEST 9: Grok response integration"""
    print("\n" + "=" * 70)
    print("TEST 9: Grok Response Integration")
    print("=" * 70)
    
    with patch.dict(os.environ, {"XAI_API_KEY": "test_key"}):
        mock_pipeline = Mock()
        mock_pipeline.predict.return_value = MOCK_CLASSIFIER_RESULT_PNEUMONIA
        
        mock_retriever = Mock()
        mock_retriever.is_ready = True
        mock_retriever.retrieve.return_value = MOCK_RETRIEVED_EVIDENCE
        
        mock_synthesizer = Mock()
        mock_synthesizer.is_ready = True
        mock_synthesizer.synthesize.return_value = MOCK_SYNTHESIS_RESULT
        
        with patch('src.api.main.inference_pipeline', mock_pipeline):
            with patch('src.api.main.rag_retriever', mock_retriever):
                with patch('src.api.main.grok_synthesizer', mock_synthesizer):
                    with patch('src.api.main.INTELLIGENCE_ENABLED', True):
                        with patch('src.api.main.PIPELINE_LOADED', True):
                            from src.api.main import app
                            
                            client = TestClient(app)
                            
                            img_bytes = create_test_image()
                            files = {"file": ("test.jpg", img_bytes, "image/jpeg")}
                            
                            response = client.post("/intelligence", files=files)
                            data = response.json()
                            
                            # Verify answer is included
                            assert "intelligence" in data
                            assert "answer" in data["intelligence"]
                            assert data["intelligence"]["answer"] == MOCK_SYNTHESIS_RESULT["answer"]
                            print("✓ Grok answer included in response")


# ============================================================================
# TEST 10: Sources Preserved
# ============================================================================

def test_sources_preserved():
    """TEST 10: Sources preserved"""
    print("\n" + "=" * 70)
    print("TEST 10: Sources Preserved")
    print("=" * 70)
    
    with patch.dict(os.environ, {"XAI_API_KEY": "test_key"}):
        mock_pipeline = Mock()
        mock_pipeline.predict.return_value = MOCK_CLASSIFIER_RESULT_PNEUMONIA
        
        mock_retriever = Mock()
        mock_retriever.is_ready = True
        mock_retriever.retrieve.return_value = MOCK_RETRIEVED_EVIDENCE
        
        mock_synthesizer = Mock()
        mock_synthesizer.is_ready = True
        mock_synthesizer.synthesize.return_value = MOCK_SYNTHESIS_RESULT
        
        with patch('src.api.main.inference_pipeline', mock_pipeline):
            with patch('src.api.main.rag_retriever', mock_retriever):
                with patch('src.api.main.grok_synthesizer', mock_synthesizer):
                    with patch('src.api.main.INTELLIGENCE_ENABLED', True):
                        with patch('src.api.main.PIPELINE_LOADED', True):
                            from src.api.main import app
                            
                            client = TestClient(app)
                            
                            img_bytes = create_test_image()
                            files = {"file": ("test.jpg", img_bytes, "image/jpeg")}
                            
                            response = client.post("/intelligence", files=files)
                            data = response.json()
                            
                            # Verify sources are present
                            assert "sources" in data["intelligence"]
                            assert len(data["intelligence"]["sources"]) == 1
                            
                            source = data["intelligence"]["sources"][0]
                            assert source["source"] == "Mayo Clinic"
                            assert source["title"] == "Symptoms of Pneumonia"
                            print("✓ Sources preserved in response")


# ============================================================================
# TEST 11: Disclaimer Preserved
# ============================================================================

def test_disclaimer_preserved():
    """TEST 11: Disclaimer preserved"""
    print("\n" + "=" * 70)
    print("TEST 11: Disclaimer Preserved")
    print("=" * 70)
    
    with patch.dict(os.environ, {"XAI_API_KEY": "test_key"}):
        mock_pipeline = Mock()
        mock_pipeline.predict.return_value = MOCK_CLASSIFIER_RESULT_PNEUMONIA
        
        mock_retriever = Mock()
        mock_retriever.is_ready = True
        mock_retriever.retrieve.return_value = MOCK_RETRIEVED_EVIDENCE
        
        mock_synthesizer = Mock()
        mock_synthesizer.is_ready = True
        mock_synthesizer.synthesize.return_value = MOCK_SYNTHESIS_RESULT
        
        with patch('src.api.main.inference_pipeline', mock_pipeline):
            with patch('src.api.main.rag_retriever', mock_retriever):
                with patch('src.api.main.grok_synthesizer', mock_synthesizer):
                    with patch('src.api.main.INTELLIGENCE_ENABLED', True):
                        with patch('src.api.main.PIPELINE_LOADED', True):
                            from src.api.main import app
                            
                            client = TestClient(app)
                            
                            img_bytes = create_test_image()
                            files = {"file": ("test.jpg", img_bytes, "image/jpeg")}
                            
                            response = client.post("/intelligence", files=files)
                            data = response.json()
                            
                            # Verify intelligence disclaimer
                            assert "disclaimer" in data["intelligence"]
                            assert len(data["intelligence"]["disclaimer"]) > 0
                            assert "educational purposes" in data["intelligence"]["disclaimer"].lower()
                            print("✓ Intelligence disclaimer present")
                            
                            # Verify classifier disclaimer
                            assert "classifier_disclaimer" in data
                            assert len(data["classifier_disclaimer"]) > 0
                            print("✓ Classifier disclaimer present")


# ============================================================================
# TEST 12: Grok Failure
# ============================================================================

def test_Grok_failure():
    """TEST 12: Grok failure"""
    print("\n" + "=" * 70)
    print("TEST 12: Grok Failure")
    print("=" * 70)
    
    with patch.dict(os.environ, {"XAI_API_KEY": "test_key"}):
        mock_pipeline = Mock()
        mock_pipeline.predict.return_value = MOCK_CLASSIFIER_RESULT_PNEUMONIA
        
        mock_retriever = Mock()
        mock_retriever.is_ready = True
        mock_retriever.retrieve.return_value = MOCK_RETRIEVED_EVIDENCE
        
        # Mock Grok failure
        mock_synthesizer = Mock()
        mock_synthesizer.is_ready = True
        mock_synthesizer.synthesize.side_effect = Exception("API Error")
        
        with patch('src.api.main.inference_pipeline', mock_pipeline):
            with patch('src.api.main.rag_retriever', mock_retriever):
                with patch('src.api.main.grok_synthesizer', mock_synthesizer):
                    with patch('src.api.main.INTELLIGENCE_ENABLED', True):
                        with patch('src.api.main.PIPELINE_LOADED', True):
                            from src.api.main import app
                            
                            client = TestClient(app)
                            
                            img_bytes = create_test_image()
                            files = {"file": ("test.jpg", img_bytes, "image/jpeg")}
                            
                            response = client.post("/intelligence", files=files)
                            data = response.json()
                            
                            # Verify classifier prediction still present and unchanged
                            assert data["prediction"]["condition"] == "PNEUMONIA"
                            assert data["prediction"]["confidence"] == 0.91
                            print("✓ Classifier prediction unchanged")
                            
                            # Verify controlled error handling
                            assert not data["success"]
                            assert "error" in data["intelligence"]
                            print("✓ Controlled error response")
                            
                            # Verify no fabricated answer
                            assert "could not complete" in data["intelligence"]["answer"].lower() or \
                                   "explanation service" in data["intelligence"]["answer"].lower()
                            print("✓ No fabricated answer")


# ============================================================================
# TEST 13: Retrieval Failure
# ============================================================================

def test_retrieval_failure():
    """TEST 13: Retrieval failure"""
    print("\n" + "=" * 70)
    print("TEST 13: Retrieval Failure")
    print("=" * 70)
    
    with patch.dict(os.environ, {"XAI_API_KEY": "test_key"}):
        mock_pipeline = Mock()
        mock_pipeline.predict.return_value = MOCK_CLASSIFIER_RESULT_PNEUMONIA
        
        # Mock retrieval failure
        mock_retriever = Mock()
        mock_retriever.is_ready = True
        mock_retriever.retrieve.side_effect = Exception("Index error")
        
        mock_synthesizer = Mock()
        mock_synthesizer.is_ready = True
        
        with patch('src.api.main.inference_pipeline', mock_pipeline):
            with patch('src.api.main.rag_retriever', mock_retriever):
                with patch('src.api.main.grok_synthesizer', mock_synthesizer):
                    with patch('src.api.main.INTELLIGENCE_ENABLED', True):
                        with patch('src.api.main.PIPELINE_LOADED', True):
                            from src.api.main import app
                            
                            client = TestClient(app)
                            
                            img_bytes = create_test_image()
                            files = {"file": ("test.jpg", img_bytes, "image/jpeg")}
                            
                            response = client.post("/intelligence", files=files)
                            data = response.json()
                            
                            # Verify classifier still works
                            assert data["prediction"]["condition"] == "PNEUMONIA"
                            print("✓ Classifier result preserved")
                            
                            # Verify retrieval error recorded
                            assert not data["retrieval"]["success"]
                            assert "error" in data["retrieval"]
                            print("✓ Retrieval error recorded")
                            
                            # Verify no evidence fabricated
                            assert data["retrieval"]["retrieved_count"] == 0
                            print("✓ No fabricated evidence")


# ============================================================================
# TEST 14: /predict Regression
# ============================================================================

def test_predict_regression():
    """TEST 14: /predict regression"""
    print("\n" + "=" * 70)
    print("TEST 14: /predict Regression")
    print("=" * 70)
    
    with patch.dict(os.environ, {"XAI_API_KEY": "test_key", "INTELLIGENCE_ENABLED": "false"}):
        mock_pipeline = Mock()
        mock_pipeline.predict.return_value = MOCK_CLASSIFIER_RESULT_PNEUMONIA
        
        with patch('src.api.main.inference_pipeline', mock_pipeline):
            with patch('src.api.main.PIPELINE_LOADED', True):
                from src.api.main import app
                
                client = TestClient(app)
                
                # Test /predict endpoint
                img_bytes = create_test_image()
                files = {"file": ("test.jpg", img_bytes, "image/jpeg")}
                
                response = client.post("/predict", files=files)
                
                assert response.status_code == 200
                data = response.json()
                
                # Verify /predict response format unchanged
                assert data["success"]
                assert data["prediction_label"] == "PNEUMONIA"
                assert data["confidence"] == 0.91
                assert "probabilities" in data
                assert "disclaimer" in data
                print("✓ /predict endpoint still functional")
                print("✓ /predict response format unchanged")


# ============================================================================
# RUN ALL TESTS
# ============================================================================

def run_all_tests():
    """Run all Stage 6 tests"""
    print("\n" + "=" * 70)
    print("STAGE 6: /INTELLIGENCE FASTAPI ENDPOINT - COMPREHENSIVE TESTS")
    print("=" * 70)
    
    try:
        # Tests 1-14
        test_endpoint_exists()
        test_missing_image()
        test_invalid_image()
        test_classifier_integration()
        test_confidence_preservation()
        test_condition_mapping()
        test_rag_integration()
        test_evidence_passed_to_Grok()
        test_Grok_response_integration()
        test_sources_preserved()
        test_disclaimer_preserved()
        test_Grok_failure()
        test_retrieval_failure()
        test_predict_regression()
        
        # Final summary
        print("\n" + "=" * 70)
        print("STAGE 6 TEST SUMMARY")
        print("=" * 70)
        print("✓ All 14 tests passed successfully")
        print(f"\n/intelligence Endpoint:")
        print(f"  ✓ Endpoint registered")
        print(f"  ✓ Image validation working")
        print(f"  ✓ Classifier integration working")
        print(f"  ✓ Confidence preserved")
        print(f"  ✓ Condition mapping working (PNEUMONIA → pneumonia, NORMAL → normal_chest_xray)")
        print(f"  ✓ RAG retrieval integrated")
        print(f"  ✓ Evidence passed to Grok")
        print(f"  ✓ Grok response integrated")
        print(f"  ✓ Sources preserved")
        print(f"  ✓ Disclaimers included")
        print(f"  ✓ Error handling working")
        print(f"\nSafety Verification:")
        print(f"  ✓ Classifier prediction never overridden")
        print(f"  ✓ No fabricated evidence on retrieval failure")
        print(f"  ✓ No fabricated answers on Grok failure")
        print(f"  ✓ Controlled error responses")
        print(f"\nRegression:")
        print(f"  ✓ /predict endpoint unchanged")
        print("\n✅ Stage 6 is COMPLETE and ready for Stage 7")
        print("=" * 70)
        
        return True
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"\n✗ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
