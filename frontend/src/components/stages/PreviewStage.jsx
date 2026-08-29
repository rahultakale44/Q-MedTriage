/**
 * IMAGE PREVIEW AND CONFIRMATION STAGE
 */

import { CheckCircle2, Play, RotateCcw } from "lucide-react";
import { motion } from "framer-motion";

export function PreviewStage({ image, onStartAnalysis, onReset }) {
  return (
    <motion.div
      className="preview-stage"
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 1.05 }}
      transition={{ duration: 0.4 }}
    >
      <div className="preview-container">
        <div className="preview-header">
          <div className="status-indicator">
            <CheckCircle2 size={20} />
            <span>IMAGE READY</span>
          </div>
          <h2>Image Uploaded Successfully</h2>
          <p className="preview-subtitle">Chest X-ray validation will occur during analysis</p>
        </div>

        <div className="preview-image-wrapper">
          <motion.div
            className="preview-image-frame"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.2, duration: 0.5 }}
          >
            <img src={image} alt="Uploaded medical image" className="preview-image" />
            <div className="image-overlay">
              <div className="corner-marker top-left" />
              <div className="corner-marker top-right" />
              <div className="corner-marker bottom-left" />
              <div className="corner-marker bottom-right" />
            </div>
          </motion.div>
        </div>

        <motion.div
          className="preview-actions"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4, duration: 0.4 }}
        >
          <button className="primary-action-button" onClick={onStartAnalysis}>
            <Play size={20} />
            Begin Analysis
          </button>
          <button className="secondary-action-button" onClick={onReset}>
            <RotateCcw size={16} />
            Choose Different Image
          </button>
        </motion.div>

        <div className="preview-metadata">
          <div className="metadata-item">
            <span className="metadata-label">STATUS</span>
            <span className="metadata-value">Ready for Analysis</span>
          </div>
          <div className="metadata-item">
            <span className="metadata-label">PIPELINE</span>
            <span className="metadata-value">CNN → PCA → QSVM → RAG</span>
          </div>
          <div className="metadata-item">
            <span className="metadata-label">ANALYSIS TIME</span>
            <span className="metadata-value">~15-20 seconds</span>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
