/**
 * BULK PROCESSING STAGE
 * Shows progress while batch analysis is running
 */

import { motion } from "framer-motion";
import { Loader, Activity } from "lucide-react";

export function BulkProcessingStage({ totalImages, completedImages }) {
  const progress = totalImages > 0 ? (completedImages / totalImages) * 100 : 0;

  return (
    <motion.div
      className="bulk-processing-stage"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    >
      <div className="processing-container">
        <motion.div
          className="processing-icon"
          animate={{ rotate: 360 }}
          transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
        >
          <Activity size={64} />
        </motion.div>

        <h2 className="processing-title">Q-MEDTRIAGE PIPELINE RUNNING</h2>
        <p className="processing-subtitle">Processing your chest X-ray batch</p>

        <div className="processing-progress">
          <div className="progress-bar-container">
            <motion.div
              className="progress-bar-fill"
              initial={{ width: 0 }}
              animate={{ width: `${progress}%` }}
              transition={{ duration: 0.3 }}
            />
          </div>
          <div className="progress-text">
            {completedImages} / {totalImages} images processed
          </div>
        </div>

        <div className="processing-stages">
          <div className="stage-item">
            <Loader size={16} className="stage-spinner" />
            <span>Validating Chest X-rays</span>
          </div>
          <div className="stage-item">
            <Loader size={16} className="stage-spinner" />
            <span>Running AI Inference</span>
          </div>
          <div className="stage-item">
            <Loader size={16} className="stage-spinner" />
            <span>Generating Results</span>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
