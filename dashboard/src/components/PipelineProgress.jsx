/**
 * PIPELINE PROGRESS INDICATOR
 */

import { motion } from "framer-motion";
import { STAGES } from "../hooks/useAnalysisPipeline";

const PROGRESS_STAGES = [
  { id: STAGES.SCANNING, label: "SCAN" },
  { id: STAGES.PREPROCESSING, label: "PREPROCESS" },
  { id: STAGES.FEATURE_EXTRACTION, label: "FEATURES" },
  { id: STAGES.DIMENSIONALITY_REDUCTION, label: "PCA" },
  { id: STAGES.QUANTUM_PROCESSING, label: "QUANTUM" },
  { id: STAGES.EVIDENCE_RETRIEVAL, label: "EVIDENCE" },
  { id: STAGES.REASONING, label: "REASONING" },
  { id: STAGES.RESULT, label: "RESULT" },
];

export function PipelineProgress({ currentStage, completedStages }) {
  const getCurrentIndex = () => {
    return PROGRESS_STAGES.findIndex((s) => s.id === currentStage);
  };

  const currentIndex = getCurrentIndex();

  return (
    <div className="pipeline-progress">
      <div className="progress-track">
        {PROGRESS_STAGES.map((stage, index) => {
          const isComplete = completedStages.has(stage.id);
          const isActive = stage.id === currentStage;
          const isFuture = index > currentIndex;

          return (
            <div
              key={stage.id}
              className={`progress-stage ${isComplete ? "complete" : ""} ${isActive ? "active" : ""} ${isFuture ? "future" : ""}`}
            >
              <motion.div
                className="progress-dot"
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: index * 0.1, type: "spring" }}
              >
                {isComplete && <span className="dot-check">✓</span>}
                {isActive && !isComplete && (
                  <motion.div
                    className="dot-pulse"
                    animate={{ scale: [1, 1.5, 1], opacity: [1, 0, 1] }}
                    transition={{ duration: 2, repeat: Infinity }}
                  />
                )}
              </motion.div>
              <span className="progress-label">{stage.label}</span>
              {index < PROGRESS_STAGES.length - 1 && (
                <div className={`progress-line ${isComplete ? "complete" : ""}`} />
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
