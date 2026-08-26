/**
 * IMAGE SCANNING ANIMATION STAGE
 */

import { Activity } from "lucide-react";
import { motion } from "framer-motion";

export function ScanningStage({ image }) {
  return (
    <motion.div
      className="scanning-stage"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.3 }}
    >
      <div className="scanning-container">
        <div className="scanning-header">
          <div className="scanning-status">
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
            >
              <Activity size={20} />
            </motion.div>
            <span>ANALYSIS INITIALIZED</span>
          </div>
          <h2>Scanning Medical Image</h2>
        </div>

        <div className="scanning-image-wrapper">
          <div className="scanning-image-frame">
            <img src={image} alt="Scanning X-ray" className="scanning-image" />
            
            {/* Animated scan line */}
            <motion.div
              className="scan-line"
              initial={{ top: "0%" }}
              animate={{ top: "100%" }}
              transition={{
                duration: 2,
                repeat: Infinity,
                ease: "linear",
              }}
            />

            {/* Analysis markers */}
            <motion.div
              className="analysis-marker marker-1"
              initial={{ opacity: 0, scale: 0 }}
              animate={{ opacity: [0, 1, 1, 0], scale: [0, 1, 1, 0] }}
              transition={{
                duration: 3,
                repeat: Infinity,
                times: [0, 0.2, 0.8, 1],
              }}
            />
            <motion.div
              className="analysis-marker marker-2"
              initial={{ opacity: 0, scale: 0 }}
              animate={{ opacity: [0, 1, 1, 0], scale: [0, 1, 1, 0] }}
              transition={{
                duration: 3,
                repeat: Infinity,
                delay: 0.5,
                times: [0, 0.2, 0.8, 1],
              }}
            />
            <motion.div
              className="analysis-marker marker-3"
              initial={{ opacity: 0, scale: 0 }}
              animate={{ opacity: [0, 1, 1, 0], scale: [0, 1, 1, 0] }}
              transition={{
                duration: 3,
                repeat: Infinity,
                delay: 1,
                times: [0, 0.2, 0.8, 1],
              }}
            />

            {/* Grid overlay */}
            <div className="scanning-grid" />
          </div>
        </div>

        <div className="scanning-indicators">
          <motion.div
            className="indicator"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 }}
          >
            <div className="indicator-dot pulsing" />
            <span>IMAGE SIGNAL DETECTED</span>
          </motion.div>
          <motion.div
            className="indicator"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.6 }}
          >
            <div className="indicator-dot pulsing" />
            <span>ANALYZING PIXEL DATA</span>
          </motion.div>
          <motion.div
            className="indicator"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.9 }}
          >
            <div className="indicator-dot pulsing" />
            <span>IDENTIFYING DIAGNOSTIC REGIONS</span>
          </motion.div>
        </div>
      </div>
    </motion.div>
  );
}
