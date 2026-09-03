/**
 * BULK PREDICTION HOOK FOR Q-MEDTRIAGE
 * 
 * Manages batch analysis of multiple chest X-rays
 */

import { useState, useCallback } from "react";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export function useBulkPrediction() {
  const [bulkState, setBulkState] = useState({
    isLoading: false,
    isComplete: false,
    results: null,
    error: null,
  });

  /**
   * Predict pneumonia for multiple chest X-rays
   */
  const predictBatch = useCallback(async (imageFiles) => {
    console.log("[useBulkPrediction] Starting batch prediction...");
    console.log("[useBulkPrediction] Total images:", imageFiles.length);
    
    // Reset state
    setBulkState({
      isLoading: true,
      isComplete: false,
      results: null,
      error: null,
    });

    try {
      // Prepare form data with multiple files
      const formData = new FormData();
      imageFiles.forEach((file) => {
        formData.append("files", file);
      });

      console.log("[useBulkPrediction] Sending POST to", `${API_URL}/predict/batch`);
      
      // Call batch API
      const response = await fetch(`${API_URL}/predict/batch`, {
        method: "POST",
        body: formData,
      });

      console.log("[useBulkPrediction] Response status:", response.status);

      // Handle response
      const data = await response.json();
      console.log("[useBulkPrediction] Response data:", data);

      if (!response.ok) {
        const errorMessage = data.detail || `API error: ${response.status} ${response.statusText}`;
        throw new Error(errorMessage);
      }

      // Success
      setBulkState({
        isLoading: false,
        isComplete: true,
        results: data,
        error: null,
      });

      console.log("[useBulkPrediction] Batch complete:", data.batch_summary);

      return data;
    } catch (error) {
      console.error("[useBulkPrediction] Batch error:", error);

      setBulkState({
        isLoading: false,
        isComplete: false,
        results: null,
        error: error.message || "Failed to analyze batch",
      });

      throw error;
    }
  }, []);

  /**
   * Reset bulk prediction state
   */
  const reset = useCallback(() => {
    setBulkState({
      isLoading: false,
      isComplete: false,
      results: null,
      error: null,
    });
  }, []);

  return {
    // State
    isLoading: bulkState.isLoading,
    isComplete: bulkState.isComplete,
    results: bulkState.results,
    error: bulkState.error,

    // Actions
    predictBatch,
    reset,
  };
}
