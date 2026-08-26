/**
 * PREPROCESSING VISUALIZATION STAGE
 */

import { CheckCircle2, ArrowRight } from "lucide-react";
import { motion } from "framer-motion";

const PREPROCESSING_STEPS = [
  { id: "resize", label: "RESIZE 224×224", delay: 0 },
  { id: "normalize", label: "NORMALIZE PIXEL VALUES", delay: 0.3 },
  { id: "convert", label: "GRAYSCALE → RGB", delay: 0.6 },
  { id: "align", label: "CHANNEL ALIGNMENT", delay: 0.9 },
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
            <h2 className="stage-title">Clean the signal</h2>
            <p className="stage-description">
              Transforming raw medical image into standardized format for deep learning analysis
            </p>
          </div>
        </div>

        <div className="stage-content">
          <div className="preprocessing-visualization">
            <div className="preprocessing-flow">
              <div className="flow-item">
                <div className="flow-image-container">
                  <img src={image} alt="Raw image" className="flow-image" />
                  <div className="flow-label">RAW IMAGE</div>
                </div>
              </div>

              <ArrowRight size={24} className="flow-arrow" />

              <div className="flow-item">
                <div className="processing-animation">
                  <motion.div
                    className="processing-overlay"
                    animate={{
                      opacity: [0.3, 0.7, 0.3],
                    }}
                    transition={{
                      duration: 1.5,
                      repeat: Infinity,
                    }}
                  />
                  <img src={image} alt="Processing" className="flow-image processing" />
                  <div className="flow-label">PROCESSING</div>
                </div>
              </div>

              <ArrowRight size={24} className="flow-arrow" />

              <div className="flow-item">
                <div className="flow-image-container">
                  <img src={image} alt="Normalized" className="flow-image normalized" />
                  <div className="flow-label">MODEL INPUT</div>
                  <motion.div
                    className="ready-indicator"
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ delay: 1.2, type: "spring" }}
                  >
                    <CheckCircle2 size={16} />
                  </motion.div>
                </div>
              </div>
            </div>

            <div className="preprocessing-steps">
              {PREPROCESSING_STEPS.map((step) => (
                <motion.div
                  key={step.id}
                  className="preprocessing-step"
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: step.delay }}
                >
                  <motion.div
                    className="step-indicator"
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ delay: step.delay + 0.2, type: "spring" }}
                  >
                    <CheckCircle2 size={14} />
                  </motion.div>
                  <span className="step-label">{step.label}</span>
                  <motion.div
                    className="step-bar"
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
              <div className="metric-label">INPUT</div>
              <div className="metric-value">RAW IMAGE</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">OUTPUT</div>
              <div className="metric-value">NORMALIZED</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">STATUS</div>
              <div className="metric-value status-ready">READY</div>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
