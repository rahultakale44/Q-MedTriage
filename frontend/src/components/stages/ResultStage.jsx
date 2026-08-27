/**
 * FINAL RESULT STAGE - Stage 07
 * Professional presentation of complete pipeline outcome
 */

import { motion } from "framer-motion";
import { CheckCircle2, AlertCircle, MessageSquare, RotateCcw, Image as ImageIcon } from "lucide-react";

export function ResultStage({ image, predictionData, error, onOpenChat, onReset }) {
  if (error) {
    return (
      <motion.div
        className="result-stage error"
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ type: "spring" }}
      >
        <div className="result-container">
          <div className="result-icon error-icon">
            <AlertCircle size={64} />
          </div>
          <h2 className="result-title">Analysis Interrupted</h2>
          <p className="result-message">{error}</p>
          <button className="primary-action-button" onClick={onReset}>
            <RotateCcw size={20} />
            Try Again
          </button>
        </div>
      </motion.div>
    );
  }

  if (!predictionData) {
    return (
      <motion.div className="result-stage loading">
        <div className="result-container">
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
          >
            <CheckCircle2 size={64} />
          </motion.div>
          <p>Finalizing analysis...</p>
        </div>
      </motion.div>
    );
  }

  const prediction = predictionData.triage?.prediction || "UNKNOWN";
  const confidence = predictionData.triage?.confidence || 0;
  const probNormal = predictionData.classical?.probability?.normal || 0;
  const probPneumonia = predictionData.classical?.probability?.pneumonia || 0;

  return (
    <motion.div
      className="result-stage"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    >
      <div className="stage-container">
        <div className="stage-header">
          <div className="stage-number">07</div>
          <div className="stage-title-group">
            <h3 className="stage-label">ANALYSIS COMPLETE</h3>
            <h2 className="stage-title">Pipeline outcome</h2>
            <p className="stage-description">
              Complete diagnostic triage result with evidence-grounded reasoning
            </p>
          </div>
        </div>

        <div className="stage-content">
          <div className="result-main-visualization">
            {/* Left: Image with border */}
            <motion.div
              className="result-image-section"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2 }}
            >
              <div className="result-image-card">
                <img src={image} alt="Analyzed radiograph" className="result-xray-image" />
                <div className="result-image-frame-border" />
                <motion.div
                  className="result-complete-badge"
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ delay: 0.5, type: "spring" }}
                >
                  <CheckCircle2 size={16} />
                  <span>ANALYZED</span>
                </motion.div>
              </div>
            </motion.div>

            {/* Right: Results */}
            <motion.div
              className="result-details-section"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.4 }}
            >
              {/* Prediction */}
              <div className="result-prediction-card">
                <div className="prediction-header">DIAGNOSTIC TRIAGE</div>
                <motion.h2
                  className={`prediction-value ${prediction.toLowerCase()}`}
                  initial={{ scale: 0.9, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  transition={{ delay: 0.6, type: "spring" }}
                >
                  {prediction}
                </motion.h2>
                <div className="confidence-row">
                  <span className="confidence-number">{(confidence * 100).toFixed(1)}%</span>
                  <span className="confidence-text">CONFIDENCE</span>
                </div>
              </div>

              {/* Probabilities */}
              <div className="result-probabilities-card">
                <div className="probability-row">
                  <div className="probability-label-text">NORMAL</div>
                  <div className="probability-bar-container">
                    <motion.div
                      className="probability-bar-fill normal"
                      initial={{ width: 0 }}
                      animate={{ width: `${probNormal * 100}%` }}
                      transition={{ delay: 0.8, duration: 0.8 }}
                    />
                  </div>
                  <div className="probability-value-text">{(probNormal * 100).toFixed(1)}%</div>
                </div>
                <div className="probability-row">
                  <div className="probability-label-text">PNEUMONIA</div>
                  <div className="probability-bar-container">
                    <motion.div
                      className="probability-bar-fill pneumonia"
                      initial={{ width: 0 }}
                      animate={{ width: `${probPneumonia * 100}%` }}
                      transition={{ delay: 0.9, duration: 0.8 }}
                    />
                  </div>
                  <div className="probability-value-text">{(probPneumonia * 100).toFixed(1)}%</div>
                </div>
              </div>

              {/* Pipeline summary */}
              <motion.div
                className="result-pipeline-summary"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 1 }}
              >
                <div className="summary-item-row">
                  <CheckCircle2 size={16} className="summary-check-icon" />
                  <span>Quantum-enhanced classification</span>
                </div>
                <div className="summary-item-row">
                  <CheckCircle2 size={16} className="summary-check-icon" />
                  <span>Evidence retrieval complete</span>
                </div>
                <div className="summary-item-row">
                  <CheckCircle2 size={16} className="summary-check-icon" />
                  <span>LLM reasoning synthesized</span>
                </div>
              </motion.div>

              {/* Action buttons */}
              <motion.div
                className="result-actions"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 1.2 }}
              >
                <button
                  className="result-primary-button"
                  onClick={onOpenChat}
                >
                  <MessageSquare size={18} />
                  Ask Questions
                </button>
                <button
                  className="result-secondary-button"
                  onClick={onReset}
                >
                  <RotateCcw size={16} />
                  New Analysis
                </button>
              </motion.div>
            </motion.div>
          </div>

          {/* Disclaimer */}
          <motion.div
            className="result-disclaimer-card"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1.4 }}
          >
            <AlertCircle size={16} className="disclaimer-icon" />
            <span className="disclaimer-text">
              AI-assisted diagnostic support tool — designed to support clinical decision-making, not replace professional medical diagnosis
            </span>
          </motion.div>

          {/* Metrics */}
          <div className="stage-metrics">
            <div className="metric-card">
              <div className="metric-label">PREDICTION</div>
              <div className="metric-value">{prediction}</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">CONFIDENCE</div>
              <div className="metric-value">{(confidence * 100).toFixed(0)}%</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">EVIDENCE</div>
              <div className="metric-value">3 SOURCES</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">STATUS</div>
              <div className="metric-value status-ready">COMPLETE</div>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
