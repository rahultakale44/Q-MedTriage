/**
 * VALIDATING STAGE - Validation Gate
 * Shows while chest X-ray validation is in progress
 */

import { motion } from "framer-motion";
import { Shield, CheckCircle2 } from "lucide-react";

export function ValidatingStage() {
  return (
    <motion.div
      className="stage validating-stage"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    >
      <div className="stage-container">
        <div className="stage-header">
          <div className="stage-number">00</div>
          <div className="stage-title-group">
            <h3 className="stage-label">VALIDATION GATE</h3>
            <h2 className="stage-title">Verifying chest X-ray</h2>
            <p className="stage-description">
              Validating that uploaded image is a valid chest radiograph
            </p>
          </div>
        </div>

        <div className="stage-content">
          <div className="validation-visualization">
            <motion.div
              className="validation-shield"
              animate={{
                scale: [1, 1.05, 1],
                opacity: [0.7, 1, 0.7],
              }}
              transition={{
                duration: 2,
                repeat: Infinity,
                ease: "easeInOut",
              }}
            >
              <Shield size={80} strokeWidth={1.5} />
            </motion.div>

            <div className="validation-status">
              <motion.div
                className="validation-step"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.2 }}
              >
                <CheckCircle2 size={16} />
                <span>Loading image...</span>
              </motion.div>
              
              <motion.div
                className="validation-step"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.4 }}
              >
                <motion.div
                  className="validation-spinner"
                  animate={{ rotate: 360 }}
                  transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                >
                  <div className="spinner-dot" />
                </motion.div>
                <span>Running chest X-ray validation...</span>
              </motion.div>
            </div>
          </div>

          <div className="stage-metrics">
            <div className="metric-card">
              <div className="metric-label">VALIDATION</div>
              <div className="metric-value status-processing">IN PROGRESS</div>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
