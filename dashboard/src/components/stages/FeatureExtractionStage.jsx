/**
 * FEATURE EXTRACTION (CNN) STAGE
 */

import { motion } from "framer-motion";

export function FeatureExtractionStage({ image }) {
  return (
    <motion.div
      className="feature-stage"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    >
      <div className="stage-container">
        <div className="stage-header">
          <div className="stage-number">02</div>
          <div className="stage-title-group">
            <h3 className="stage-label">FEATURE EXTRACTION</h3>
            <h2 className="stage-title">See the patterns</h2>
            <p className="stage-description">
              Pre-trained ResNet50 CNN extracting clinically relevant visual features
            </p>
          </div>
        </div>

        <div className="stage-content">
          <div className="feature-visualization">
            <div className="feature-image-container">
              <img src={image} alt="Feature analysis" className="feature-image" />
              
              {/* Animated feature detection regions */}
              {[1, 2, 3, 4, 5, 6].map((i) => (
                <motion.div
                  key={i}
                  className={`feature-region region-${i}`}
                  initial={{ opacity: 0, scale: 0 }}
                  animate={{ 
                    opacity: [0, 0.8, 0.8, 0],
                    scale: [0.8, 1.1, 1.1, 0.8],
                  }}
                  transition={{
                    duration: 2,
                    repeat: Infinity,
                    delay: i * 0.3,
                  }}
                />
              ))}
            </div>

            <div className="feature-network">
              <div className="network-layers">
                {[8, 12, 16, 12, 8].map((count, layerIdx) => (
                  <div key={layerIdx} className="network-layer">
                    {Array.from({ length: count }).map((_, nodeIdx) => (
                      <motion.div
                        key={nodeIdx}
                        className="network-node"
                        animate={{
                          opacity: [0.3, 1, 0.3],
                          scale: [0.9, 1.1, 0.9],
                        }}
                        transition={{
                          duration: 1.5,
                          repeat: Infinity,
                          delay: (layerIdx * 0.1) + (nodeIdx * 0.05),
                        }}
                      />
                    ))}
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="stage-metrics">
            <div className="metric-card">
              <div className="metric-label">MODEL</div>
              <div className="metric-value">RESNET50</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">FEATURES</div>
              <div className="metric-value">2048D</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">STATUS</div>
              <div className="metric-value status-active">
                <motion.span
                  animate={{ opacity: [1, 0.5, 1] }}
                  transition={{ duration: 1.5, repeat: Infinity }}
                >
                  EXTRACTING
                </motion.span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
