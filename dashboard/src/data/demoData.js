/**
 * DEMO DATA FOR Q-MEDTRIAGE FRONTEND
 * 
 * This file contains deterministic mock data used while the Kermany Chest X-Ray
 * dataset is being prepared and the ML pipeline is being implemented.
 * 
 * ⚠️ TEMPORARY: This demo data shows NODULE detection for UI development.
 * The actual backend will use NORMAL vs PNEUMONIA classification (Kermany dataset).
 * Frontend will be updated to reflect PNEUMONIA detection once backend is integrated.
 * These values are clearly separated from future real model outputs.
 * When backend integration is complete, this data will be replaced by
 * actual API responses.
 */

export const DEMO_ANALYSIS = {
  // Image metadata
  image: {
    status: "processed",
    format: "JPEG",
    dimensions: "224x224",
    uploaded: true,
  },

  // Preprocessing stage
  preprocessing: {
    steps: [
      { name: "RESIZE 224×224", completed: true },
      { name: "NORMALIZE", completed: true },
      { name: "DENOISE", completed: true },
      { name: "CHANNEL ALIGN", completed: true },
    ],
    output: "NORMALIZED",
  },

  // CNN feature extraction
  cnn: {
    backbone: "ResNet50",
    featureDimension: 2048,
    extractionTime: "42ms",
    status: "complete",
  },

  // PCA dimensionality reduction
  pca: {
    inputDimension: 2048,
    outputDimension: 4,
    varianceRetained: 0.89,
    components: [0.82, -0.34, 0.61, 0.17],
  },

  // Classical SVM classifier
  classical: {
    model: "SVM",
    prediction: "Nodule",
    confidence: 0.923,
    probability: {
      nodule: 0.923,
      nonNodule: 0.077,
    },
  },

  // Quantum classifier
  quantum: {
    model: "QSVM",
    qubits: 4,
    featureMap: "ZZFeatureMap",
    backend: "qasm_simulator",
    shots: 1024,
    prediction: "Nodule",
    confidence: 0.947,
    probability: {
      nodule: 0.947,
      nonNodule: 0.053,
    },
    measurement: 0.947,
  },

  // Evidence retrieval
  evidence: {
    retrievalMethod: "FAISS",
    embeddingModel: "sentence-transformers",
    results: [
      {
        title: "Imaging characteristics of pulmonary nodules",
        relevance: 0.92,
        source: "Medical Knowledge Base",
        snippet: "Round opacity in lung parenchyma...",
      },
      {
        title: "Clinical guidelines for nodule assessment",
        relevance: 0.85,
        source: "Clinical References",
        snippet: "Size, shape, and density evaluation...",
      },
      {
        title: "Relevant diagnostic criteria",
        relevance: 0.78,
        source: "Diagnostic Guidelines",
        snippet: "Follow-up recommendations based on...",
      },
    ],
  },

  // LLM reasoning
  reasoning: {
    llmModel: "GPT-4",
    synthesis: "grounded",
    inputSources: ["model_output", "evidence", "image_context"],
    explanation:
      "The quantum classifier detected a nodular pattern with high confidence (94.7%). " +
      "This finding is supported by retrieved medical evidence regarding pulmonary nodule " +
      "characteristics. The model's attention focused on a region consistent with typical " +
      "nodule presentation.",
  },

  // Final triage result
  triage: {
    classification: "ABNORMAL",
    prediction: "Nodule",
    confidence: 0.947,
    priority: "HIGH",
    recommendation: "Further radiological assessment recommended",
    disclaimer: "AI-assisted decision support. Not a medical diagnosis.",
  },

  // System performance metrics
  performance: {
    totalLatency: "156ms",
    stages: {
      preprocessing: "18ms",
      cnn: "42ms",
      pca: "3ms",
      quantum: "67ms",
      evidence: "21ms",
      reasoning: "5ms",
    },
  },
};

/**
 * Demo data for quantum circuit visualization
 */
export const DEMO_QUANTUM_CIRCUIT = {
  inputs: [0.82, -0.34, 0.61, 0.17],
  qubits: ["Q0", "Q1", "Q2", "Q3"],
  gates: [
    { type: "H", position: 0 },
    { type: "RY", position: 1 },
    { type: "RZ", position: 2 },
  ],
  measurement: 0.947,
};

/**
 * Demo comparison between classical and quantum models
 */
export const DEMO_MODEL_COMPARISON = {
  classical: {
    accuracy: 0.891,
    precision: 0.887,
    recall: 0.893,
    f1Score: 0.890,
    rocAuc: 0.925,
  },
  quantum: {
    accuracy: 0.903,
    precision: 0.901,
    recall: 0.906,
    f1Score: 0.904,
    rocAuc: 0.938,
  },
};

/**
 * System status for dashboard
 */
export const DEMO_SYSTEM_STATUS = {
  api: "online",
  visionModel: "ready",
  quantumCore: "ready",
  vectorDb: "ready",
  llm: "ready",
  latency: "42ms",
};

/**
 * Helper to get stage-specific demo data
 */
export function getDemoDataForStage(stageId) {
  const stageMap = {
    input: DEMO_ANALYSIS.image,
    preprocess: DEMO_ANALYSIS.preprocessing,
    cnn: DEMO_ANALYSIS.cnn,
    pca: DEMO_ANALYSIS.pca,
    quantum: DEMO_ANALYSIS.quantum,
    evidence: DEMO_ANALYSIS.evidence,
    reason: DEMO_ANALYSIS.reasoning,
    triage: DEMO_ANALYSIS.triage,
  };

  return stageMap[stageId] || null;
}
