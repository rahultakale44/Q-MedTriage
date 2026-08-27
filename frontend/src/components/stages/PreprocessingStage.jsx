/**
 * PREPROCESSING STAGE - Stage 01
 * Clear visualization of image transformation pipeline
 */

import { CheckCircle2, ArrowRight } from "lucide-react";
import { motion } from "framer-motion";

const PREPROCESSING_STEPS = [
  { id: "resize", label: "RESIZE 224×224", delay: 0.3 },
  { id: "normalize", label: "NORMALIZE PIXEL VALUES", delay: 0.5 },
  { id: "convert", label: "CHANNEL ALIGNMENT", delay: 0.7 },
  { id: "ready", label: "MODEL INPUT READY", delay: 0.9 },
];

export function PreprocessingStage({ image }) {
  return (
    <motion.div
      className="preprocessing-stage"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.3 }}
    >
      <div className="stage-container">
        <div className="stage-header">
          <div className="stage-number">01</div>
          <div className="stage-title-group">
            <h3 className="stage-label">PREPROCESSING</h3>
            <h2 className="stage-title">Standardize input</h2>
            <p className="stage-description">
              Normalizing radiograph format and pixel values for deep learning model compatibility
            </p>
          </div>
        </div>

        <div className="stage-content">
          {/* Main transformation flow */}
          <div className="preprocessing-visualization">
            <div className="preprocessing-flow-container">
              {/* Raw Image */}
              <motion.div
                className="preprocessing-image-card"
                initial={{ opacity: 0, x: -30 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.2 }}
              >
                <div className="card-label">RAW IMAGE</div>
                <div className="card-image-wrapper">
                  <img src={image} alt="Raw radiograph" className="card-image" />
                  <div className="image-info">Original</div>
                </div>
              </motion.div>

              {/* Arrow */}
              <motion.div
                className="flow-arrow-icon"
                initial={{ scaleX: 0, opacity: 0 }}
                animate={{ scaleX: 1, opacity: 1 }}
                transition={{ delay: 0.5, duration: 0.4 }}
              >
                <ArrowRight size={28} />
              </motion.div>

              {/* Processing */}
              <motion.div
                className="preprocessing-image-card processing"
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.7 }}
              >
                <div className="card-label">PROCESSING</div>
                <div className="card-image-wrapper">
                  <img src={image} alt="Processing" className="card-image" />
                  <motion.div
                    className="processing-scan-overlay"
                    animate={{
                      backgroundPosition: ["0% 0%", "200% 0%"],
                    }}
                    transition={{
                      duration: 1.5,
                      repeat: Infinity,
                      ease: "linear",
                    }}
                  />
                </div>
              </motion.div>

              {/* Arrow */}
              <motion.div
                className="flow-arrow-icon"
                initial={{ scaleX: 0, opacity: 0 }}
                animate={{ scaleX: 1, opacity: 1 }}
                transition={{ delay: 0.9, duration: 0.4 }}
              >
                <ArrowRight size={28} />
              </motion.div>

              {/* Model Input */}
              <motion.div
                className="preprocessing-image-card output"
                initial={{ opacity: 0, x: 30 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 1.1 }}
              >
                <div className="card-label">MODEL INPUT</div>
                <div className="card-image-wrapper">
                  <img src={image} alt="Normalized" className="card-image normalized" />
                  <div className="image-info">224×224</div>
                  <motion.div
                    className="ready-check-badge"
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ delay: 1.5, type: "spring" }}
                  >
                    <CheckCircle2 size={20} />
                  </motion.div>
                </div>
              </motion.div>
            </div>

            {/* Processing steps list */}
            <div className="preprocessing-steps-list">
              {PREPROCESSING_STEPS.map((step) => (
                <motion.div
                  key={step.id}
                  className="preprocessing-step-item"
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: step.delay }}
                >
                  <motion.div
                    className="step-check-icon"
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ delay: step.delay + 0.15, type: "spring" }}
                  >
                    <CheckCircle2 size={16} />
                  </motion.div>
                  <span className="step-text">{step.label}</span>
                  <motion.div
                    className="step-progress-bar"
                    initial={{ scaleX: 0 }}
                    animate={{ scaleX: 1 }}
                    transition={{ delay: step.delay, duration: 0.4 }}
                  />
                </motion.div>
              ))}
            </div>
          </div>

          <div className="stage-metrics">
            <div className="metric-card">
              <div className="metric-label">INPUT SIZE</div>
              <div className="metric-value">VARIABLE</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">OUTPUT SIZE</div>
              <div className="metric-value">224×224</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">CHANNELS</div>
              <div className="metric-value">RGB</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">STATUS</div>
              <div className="metric-value status-ready">NORMALIZED</div>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
