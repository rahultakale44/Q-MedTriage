/**
 * FINAL RESULT REVEAL STAGE
 */

import { motion } from "framer-motion";
import { CheckCircle2, AlertCircle, MessageSquare, RotateCcw } from "lucide-react";

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
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ type: "spring", duration: 0.6 }}
    >
      <motion.div
        className="result-container"
        initial={{ y: 20 }}
        animate={{ y: 0 }}
        transition={{ delay: 0.2 }}
      >
        <motion.div
          className="result-badge"
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.3, type: "spring" }}
        >
          <CheckCircle2 size={24} />
          <span>ANALYSIS COMPLETE</span>
        </motion.div>

        <motion.div
          className="result-image"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
        >
          <img src={image} alt="Analyzed X-ray" />
          <div className="image-border" />
        </motion.div>

        <motion.div
          className="result-prediction"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
        >
          <h2 className={`prediction-label ${prediction.toLowerCase()}`}>
            {prediction}
          </h2>
          <div className="confidence-display">
            <span className="confidence-value">{(confidence * 100).toFixed(1)}%</span>
            <span className="confidence-label">CONFIDENCE</span>
          </div>
        </motion.div>

        <motion.div
          className="result-probabilities"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
        >
          <div className="probability-item">
            <div className="probability-label">NORMAL</div>
            <div className="probability-bar">
              <motion.div
                className="probability-fill normal"
                initial={{ width: 0 }}
                animate={{ width: `${probNormal * 100}%` }}
                transition={{ delay: 0.8, duration: 0.8 }}
              />
            </div>
            <div className="probability-value">{(probNormal * 100).toFixed(1)}%</div>
          </div>
          <div className="probability-item">
            <div className="probability-label">PNEUMONIA</div>
            <div className="probability-bar">
              <motion.div
                className="probability-fill pneumonia"
                initial={{ width: 0 }}
                animate={{ width: `${probPneumonia * 100}%` }}
                transition={{ delay: 0.9, duration: 0.8 }}
              />
            </div>
            <div className="probability-value">{(probPneumonia * 100).toFixed(1)}%</div>
          </div>
        </motion.div>

        <motion.div
          className="result-summary"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1 }}
        >
          <div className="summary-item">
            <CheckCircle2 size={16} />
            <span>Evidence retrieved</span>
          </div>
          <div className="summary-item">
            <CheckCircle2 size={16} />
            <span>Model prediction</span>
          </div>
          <div className="summary-item">
            <CheckCircle2 size={16} />
            <span>Grounded reasoning</span>
          </div>
        </motion.div>

        <motion.button
          className="primary-action-button large"
          onClick={onOpenChat}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.2 }}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <MessageSquare size={20} />
          Let's Analyse
        </motion.button>

        <motion.button
          className="secondary-action-button"
          onClick={onReset}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.4 }}
        >
          <RotateCcw size={16} />
          Analyze Another Image
        </motion.button>

        <motion.div
          className="result-disclaimer"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.5 }}
        >
          <AlertCircle size={14} />
          <span>
            AI-assisted triage — designed to support clinical decision-making, not replace medical diagnosis
          </span>
        </motion.div>
      </motion.div>
    </motion.div>
  );
}
