/**
 * STATE-DRIVEN ANALYSIS PIPELINE HOOK
 * 
 * Manages the complete Q-MedTriage analysis workflow as a state machine
 * rather than scroll-driven stages.
 */

import { useState, useCallback, useRef, useEffect } from "react";
import { usePrediction } from "./usePrediction";

// Pipeline stages in order
export const STAGES = {
  LANDING: "landing",
  UPLOAD: "upload",
  PREVIEW: "preview",
  VALIDATING: "validating", // NEW: Validation gate before pipeline
  SCANNING: "scanning",
  PREPROCESSING: "preprocessing",
  FEATURE_EXTRACTION: "feature_extraction",
  DIMENSIONALITY_REDUCTION: "dimensionality_reduction",
  QUANTUM_PROCESSING: "quantum_processing",
  EVIDENCE_RETRIEVAL: "evidence_retrieval",
  REASONING: "reasoning",
  RESULT: "result",
  CHAT: "chat",
};

// Stage display metadata with SLOWER, more engaging durations
export const STAGE_INFO = {
  [STAGES.SCANNING]: {
    label: "IMAGE ANALYSIS",
    title: "Scanning medical image",
    duration: 3500, // Was 2000, now 3.5s
  },
  [STAGES.PREPROCESSING]: {
    label: "PREPROCESSING",
    title: "Clean the signal",
    duration: 3000, // Was 1500, now 3s
  },
  [STAGES.FEATURE_EXTRACTION]: {
    label: "FEATURE EXTRACTION",
    title: "See the patterns",
    duration: 4000, // Was 2000, now 4s
  },
  [STAGES.DIMENSIONALITY_REDUCTION]: {
    label: "DIMENSIONALITY REDUCTION",
    title: "Compress intelligence",
    duration: 4000, // Was 1500, now 4s
  },
  [STAGES.QUANTUM_PROCESSING]: {
    label: "QUANTUM CLASSIFICATION",
    title: "Enter the quantum core",
    duration: 7000, // Was 2500, now 7s (6-8s range)
  },
  [STAGES.EVIDENCE_RETRIEVAL]: {
    label: "EVIDENCE RETRIEVAL",
    title: "Bring the evidence",
    duration: 4000, // Was 2000, now 4s
  },
  [STAGES.REASONING]: {
    label: "AI REASONING",
    title: "Connect the dots",
    duration: 4000, // Was 2000, now 4s
  },
};

export function useAnalysisPipeline() {
  const [currentStage, setCurrentStage] = useState(STAGES.LANDING);
  const [completedStages, setCompletedStages] = useState(new Set());
  const [uploadedImage, setUploadedImage] = useState(null);
  const [imageFile, setImageFile] = useState(null);
  const stageTimeoutRef = useRef(null);
  const predictionStatusRef = useRef({ isComplete: false, error: null });

  // Use existing prediction hook for real API integration
  const { isLoading, isComplete, result, error, validationError, validation, predict } = usePrediction();

  // Update prediction status ref whenever prediction state changes
  useEffect(() => {
    predictionStatusRef.current = { isComplete, error };
  }, [isComplete, error]);

  /**
   * Navigate to a specific stage
   */
  const goToStage = useCallback((stage) => {
    setCurrentStage(stage);
    
    // Clear any pending stage timeout
    if (stageTimeoutRef.current) {
      clearTimeout(stageTimeoutRef.current);
      stageTimeoutRef.current = null;
    }
  }, []);

  /**
   * Start triage (go to upload)
   */
  const startTriage = useCallback(() => {
    goToStage(STAGES.UPLOAD);
  }, [goToStage]);

  /**
   * Mark current stage as complete and move to next
   */
  const completeStage = useCallback((nextStage) => {
    setCompletedStages((prev) => new Set([...prev, currentStage]));
    if (nextStage) {
      goToStage(nextStage);
    }
  }, [currentStage, goToStage]);

  /**
   * Handle image upload
   */
  const handleImageUpload = useCallback((file) => {
    const imageUrl = URL.createObjectURL(file);
    setUploadedImage(imageUrl);
    setImageFile(file);
    goToStage(STAGES.PREVIEW);
  }, [goToStage]);

  /**
   * Start analysis pipeline
   * CRITICAL: Validation must complete BEFORE visual pipeline starts
   */
  const startAnalysis = useCallback(async () => {
    if (!imageFile) return;

    // STEP 1: Show validation state and call prediction API
    console.log("[PIPELINE] Starting analysis - validating image...");
    goToStage(STAGES.VALIDATING);
    
    try {
      // Call predict and wait for result
      await predict(imageFile);
      
      // STEP 2: Validation passed and prediction complete - now start visual pipeline
      console.log("[PIPELINE] Validation passed - starting visual pipeline");
      goToStage(STAGES.SCANNING);
      
      // Progress through visual stages
      const progressPipeline = async () => {
        // Scanning
        await new Promise(resolve => {
          stageTimeoutRef.current = setTimeout(() => {
            completeStage(STAGES.PREPROCESSING);
            resolve();
          }, STAGE_INFO[STAGES.SCANNING].duration);
        });

        // Preprocessing
        await new Promise(resolve => {
          stageTimeoutRef.current = setTimeout(() => {
            completeStage(STAGES.FEATURE_EXTRACTION);
            resolve();
          }, STAGE_INFO[STAGES.PREPROCESSING].duration);
        });

        // Feature extraction
        await new Promise(resolve => {
          stageTimeoutRef.current = setTimeout(() => {
            completeStage(STAGES.DIMENSIONALITY_REDUCTION);
            resolve();
          }, STAGE_INFO[STAGES.FEATURE_EXTRACTION].duration);
        });

        // Dimensionality reduction
        await new Promise(resolve => {
          stageTimeoutRef.current = setTimeout(() => {
            completeStage(STAGES.QUANTUM_PROCESSING);
            resolve();
          }, STAGE_INFO[STAGES.QUANTUM_PROCESSING].duration);
        });

        // Quantum processing (already complete from predict call)
        await new Promise(resolve => {
          stageTimeoutRef.current = setTimeout(() => {
            completeStage(STAGES.EVIDENCE_RETRIEVAL);
            resolve();
          }, STAGE_INFO[STAGES.QUANTUM_PROCESSING].duration);
        });

        // Evidence retrieval
        await new Promise(resolve => {
          stageTimeoutRef.current = setTimeout(() => {
            completeStage(STAGES.REASONING);
            resolve();
          }, STAGE_INFO[STAGES.EVIDENCE_RETRIEVAL].duration);
        });

        // Reasoning
        await new Promise(resolve => {
          stageTimeoutRef.current = setTimeout(() => {
            completeStage(STAGES.RESULT);
            resolve();
          }, STAGE_INFO[STAGES.REASONING].duration);
        });
      };

      progressPipeline();
      
    } catch (error) {
      // Prediction/validation failed - error is thrown from predict()
      console.error("[PIPELINE] Prediction/validation failed:", error);
      // Go directly to result stage to show error
      // The validationError state is already set by usePrediction hook
      goToStage(STAGES.RESULT);
    }
  }, [imageFile, predict, goToStage, completeStage]);

  /**
   * Reset pipeline
   */
  const resetPipeline = useCallback(() => {
    if (uploadedImage) {
      URL.revokeObjectURL(uploadedImage);
    }
    
    if (stageTimeoutRef.current) {
      clearTimeout(stageTimeoutRef.current);
    }
    
    setCurrentStage(STAGES.LANDING);
    setCompletedStages(new Set());
    setUploadedImage(null);
    setImageFile(null);
  }, [uploadedImage]);

  /**
   * Open chat interface
   */
  const openChat = useCallback(() => {
    goToStage(STAGES.CHAT);
  }, [goToStage]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (stageTimeoutRef.current) {
        clearTimeout(stageTimeoutRef.current);
      }
      if (uploadedImage) {
        URL.revokeObjectURL(uploadedImage);
      }
    };
  }, [uploadedImage]);

  return {
    // Current state
    currentStage,
    completedStages,
    uploadedImage,
    imageFile,
    
    // Prediction data
    predictionResult: result,
    isPredicting: isLoading,
    predictionComplete: isComplete,
    predictionError: error,
    validationError: validationError,
    validation: validation,
    
    // Actions
    startTriage,
    handleImageUpload,
    startAnalysis,
    resetPipeline,
    openChat,
    goToStage,
    completeStage,
    
    // Helpers
    isStageComplete: (stage) => completedStages.has(stage),
    isStageActive: (stage) => currentStage === stage,
  };
}
