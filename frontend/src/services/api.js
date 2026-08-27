/**
 * API SERVICE LAYER FOR Q-MEDTRIAGE
 * 
 * This module provides a clean interface for backend communication.
 * Currently returns demo data. When backend is ready, update the
 * BASE_URL and implement actual HTTP requests.
 */

import { DEMO_ANALYSIS, DEMO_SYSTEM_STATUS } from "../data/demoData";

// Backend API base URL
// Updated to use real backend
const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

// Demo mode flag
// Set to false to use real backend
const USE_DEMO_DATA = false;

/**
 * Simulated API delay for realistic UX
 */
const simulateDelay = (ms = 800) =>
  new Promise((resolve) => setTimeout(resolve, ms));

/**
 * Check API health status
 */
export async function checkHealth() {
  if (USE_DEMO_DATA) {
    await simulateDelay(200);
    return {
      success: true,
      data: DEMO_SYSTEM_STATUS,
    };
  }

  try {
    const response = await fetch(`${BASE_URL}/health`);
    const data = await response.json();
    return { success: true, data };
  } catch (error) {
    return {
      success: false,
      error: error.message,
    };
  }
}

/**
 * Analyze medical image
 * 
 * @param {File} imageFile - The uploaded chest X-ray image
 * @returns {Promise} Analysis result containing all pipeline stages
 */
export async function analyzeImage(imageFile) {
  if (USE_DEMO_DATA) {
    // Simulate processing time
    await simulateDelay(1200);

    return {
      success: true,
      data: DEMO_ANALYSIS,
    };
  }

  try {
    const formData = new FormData();
    formData.append("file", imageFile);

    const response = await fetch(`${BASE_URL}/predict`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    const data = await response.json();

    return {
      success: true,
      data,
    };
  } catch (error) {
    return {
      success: false,
      error: error.message,
    };
  }
}

/**
 * Build minimal analysis context from pipeline state for /ask
 */
function buildAnalysisContext(context) {
  const data = context?.prediction;
  if (!data?.triage) return null;

  const analysisContext = {
    prediction: data.triage.prediction,
    confidence: data.triage.confidence,
    analysis_type: "chest_xray_triage",
    priority: data.triage.priority,
    classifier: data.raw?.classifier || "classical",
    model: data.classical?.model || null,
  };

  if (data.classical?.probability) {
    analysisContext.probabilities = {
      NORMAL: data.classical.probability.normal,
      PNEUMONIA: data.classical.probability.pneumonia,
    };
  }

  return analysisContext;
}

/**
 * Ask medical question (RAG-based Q&A)
 * 
 * @param {string} question - User's medical question
 * @param {object} context - Optional context (image analysis results, etc.)
 * @returns {Promise} Answer with sources
 */
export async function askQuestion(question, context = null) {
  if (USE_DEMO_DATA) {
    await simulateDelay(600);

    return {
      success: true,
      data: {
        question,
        answer:
          "This is a demo response. The RAG pipeline will provide " +
          "evidence-grounded medical information once the backend is connected.",
        sources: DEMO_ANALYSIS.evidence.results.slice(0, 2),
      },
    };
  }

  try {
    const analysisContext = buildAnalysisContext(context);
    const body = analysisContext ? { analysis_context: analysisContext } : {};

    const response = await fetch(`${BASE_URL}/ask?question=${encodeURIComponent(question)}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    const data = await response.json();

    return {
      success: true,
      data,
    };
  } catch (error) {
    return {
      success: false,
      error: error.message,
    };
  }
}

/**
 * Get model comparison metrics
 * 
 * @returns {Promise} Classical vs Quantum performance comparison
 */
export async function getModelComparison() {
  if (USE_DEMO_DATA) {
    await simulateDelay(300);

    return {
      success: true,
      data: {
        classical: {
          model: "SVM",
          accuracy: 0.891,
          precision: 0.887,
          recall: 0.893,
          f1Score: 0.890,
          rocAuc: 0.925,
        },
        quantum: {
          model: "QSVM",
          accuracy: 0.903,
          precision: 0.901,
          recall: 0.906,
          f1Score: 0.904,
          rocAuc: 0.938,
        },
      },
    };
  }

  try {
    const response = await fetch(`${BASE_URL}/api/models/comparison`);
    const data = await response.json();
    return { success: true, data };
  } catch (error) {
    return {
      success: false,
      error: error.message,
    };
  }
}

/**
 * Upload configuration helper
 */
export const UPLOAD_CONFIG = {
  maxSizeMB: 10,
  acceptedFormats: ["image/png", "image/jpeg", "image/jpg", "image/webp"],
  acceptedExtensions: [".png", ".jpg", ".jpeg", ".webp"],
};

/**
 * Validate uploaded file
 */
export function validateImageFile(file) {
  const errors = [];

  // Check file type
  if (!UPLOAD_CONFIG.acceptedFormats.includes(file.type)) {
    errors.push(
      `Invalid file type. Accepted formats: ${UPLOAD_CONFIG.acceptedExtensions.join(", ")}`
    );
  }

  // Check file size
  const sizeMB = file.size / (1024 * 1024);
  if (sizeMB > UPLOAD_CONFIG.maxSizeMB) {
    errors.push(`File too large. Maximum size: ${UPLOAD_CONFIG.maxSizeMB}MB`);
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}
