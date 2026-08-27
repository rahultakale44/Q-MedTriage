/**
 * IMAGE SCANNING STAGE - Stage 00
 * Professional compact dashboard showing the uploaded medical image ready for analysis
 */

import { motion } from "framer-motion";
import { CheckCircle2, Image as ImageIcon } from "lucide-react";

export function ScanningStage({ image }) {
  // Extract image dimensions if available
  const imageObj = new Image();
  imageObj.src = image;

  return (
    <motion.div
      className="scanning-stage"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.3 }}
    >
      <div className="stage-container">
        <div className="stage-header">
          <div className="stage-number">00</div>
          <div className="stage-title-group">
            <h3 className="stage-label">IMAGE ACQUISITION</h3>
            <h2 className="stage-title">Medical image received</h2>
            <p className="stage-description">
              Chest radiograph successfully loaded and prepared for analysis pipeline
            </p>
          </div>
        </div>

        <div className="stage-content">
          <div className="scan-visualization">
            {/* Main image container */}
            <motion.div
              className="scan-image-container"
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ delay: 0.2, duration: 0.5 }}
            >
              <img src={image} alt="Chest X-ray" className="scan-image" />
              
              {/* Corner markers for professional framing */}
              <div className="scan-corner-marker top-left" />
              <div className="scan-corner-marker top-right" />
              <div className="scan-corner-marker bottom-left" />
              <div className="scan-corner-marker bottom-right" />
              
              {/* Scan line animation */}
              <motion.div
                className="scan-line-horizontal"
                initial={{ top: "0%" }}
                animate={{ top: "100%" }}
                transition={{
                  duration: 2,
                  repeat: 2,
                  ease: "linear",
                }}
              />
              
              {/* Ready indicator */}
              <motion.div
                className="scan-ready-badge"
                initial={{ scale: 0, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ delay: 1.5, type: "spring" }}
              >
                <CheckCircle2 size={16} />
                <span>READY</span>
              </motion.div>
            </motion.div>

            {/* Status indicators */}
            <div className="scan-status-grid">
              <motion.div
                className="scan-status-item"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4 }}
              >
                <ImageIcon size={20} className="status-icon" />
                <div className="status-content">
                  <div className="status-label">FORMAT</div>
                  <div className="status-value">DICOM / PNG</div>
                </div>
              </motion.div>

              <motion.div
                className="scan-status-item"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.6 }}
              >
                <CheckCircle2 size={20} className="status-icon success" />
                <div className="status-content">
                  <div className="status-label">QUALITY</div>
                  <div className="status-value">ACCEPTABLE</div>
                </div>
              </motion.div>

              <motion.div
                className="scan-status-item"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.8 }}
              >
                <CheckCircle2 size={20} className="status-icon success" />
                <div className="status-content">
                  <div className="status-label">PIPELINE</div>
                  <div className="status-value">INITIALIZED</div>
                </div>
              </motion.div>
            </div>
          </div>

          <div className="stage-metrics">
            <div className="metric-card">
              <div className="metric-label">MODALITY</div>
              <div className="metric-value">CHEST X-RAY</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">VIEW</div>
              <div className="metric-value">PA / AP</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">STATUS</div>
              <div className="metric-value status-ready">ACQUIRED</div>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
