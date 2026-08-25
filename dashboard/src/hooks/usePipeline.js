import { useState, useCallback } from "react";
import { DEMO_ANALYSIS } from "../data/demoData";

/**
 * Custom hook for managing Q-MedTriage pipeline state
 * 
 * This hook centralizes the analysis pipeline state and provides
 * a clean interface for future backend integration.
 * 
 * Currently uses demo data. When backend is ready, replace
 * DEMO_ANALYSIS with actual API responses.
 */
export function usePipeline() {
  // Uploaded image
  const [uploadedImage, setUploadedImage] = useState(null);

  // Analysis state
  const [analysisState, setAnalysisState] = useState({
    status: "idle", // idle | processing | complete | error
    currentStage: null,
    data: null,
  });

  // Start analysis with uploaded image
  const startAnalysis = useCallback((imageFile) => {
    // Create object URL for display
    const imageUrl = URL.createObjectURL(imageFile);
    setUploadedImage(imageUrl);

    // TODO: When backend is ready, replace this with API call
    // For now, use demo data
    setAnalysisState({
      status: "processing",
      currentStage: "input",
      data: DEMO_ANALYSIS,
    });

    // Simulate analysis completion
    setTimeout(() => {
      setAnalysisState((prev) => ({
        ...prev,
        status: "complete",
      }));
    }, 500);
  }, []);

  // Clear analysis
  const clearAnalysis = useCallback(() => {
    if (uploadedImage) {
      URL.revokeObjectURL(uploadedImage);
    }
    setUploadedImage(null);
    setAnalysisState({
      status: "idle",
      currentStage: null,
      data: null,
    });
  }, [uploadedImage]);

  // Update current stage (for scroll tracking)
  const updateStage = useCallback((stageId) => {
    setAnalysisState((prev) => ({
      ...prev,
      currentStage: stageId,
    }));
  }, []);

  // Get data for specific stage
  const getStageData = useCallback(
    (stageId) => {
      if (!analysisState.data) return null;

      const stageMap = {
        input: analysisState.data.image,
        preprocess: analysisState.data.preprocessing,
        cnn: analysisState.data.cnn,
        pca: analysisState.data.pca,
        quantum: analysisState.data.quantum,
        evidence: analysisState.data.evidence,
        reason: analysisState.data.reasoning,
        triage: analysisState.data.triage,
      };

      return stageMap[stageId] || null;
    },
    [analysisState.data]
  );

  return {
    // State
    uploadedImage,
    analysisState,
    isProcessing: analysisState.status === "processing",
    isComplete: analysisState.status === "complete",
    hasImage: uploadedImage !== null,

    // Actions
    startAnalysis,
    clearAnalysis,
    updateStage,
    getStageData,
  };
}
