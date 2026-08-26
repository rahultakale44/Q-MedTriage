/**
 * DIMENSIONALITY REDUCTION (PCA) STAGE
 */

import { useMemo } from "react";
import { motion } from "framer-motion";

export function DimensionalityReductionStage() {
  // Generate stable random positions for particles
  const particles = useMemo(() => {
    return Array.from({ length: 80 }).map(() => ({
      startX: (Math.random() - 0.5) * 300,
      startY: (Math.random() - 0.5) * 200,
      endX: (Math.random() - 0.5) * 30,
      endY: (Math.random() - 0.5) * 30,
    }));
  }, []);

  return (
    <motion.div
      className="dimensionality-stage"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    >
      <div className="stage-container">
        <div className="stage-header">
          <div className="stage-number">03</div>
          <div className="stage-title-group">
            <h3 className="stage-label">DIMENSIONALITY REDUCTION</h3>
            <h2 className="stage-title">Compress intelligence</h2>
            <p className="stage-description">
              PCA projection reducing 2048D features to compact 4D representation
            </p>
          </div>
        </div>

        <div className="stage-content">
          <div className="pca-visualization">
            <div className="dimension-cloud high">
              <div className="dimension-label">2048D HIGH-DIMENSIONAL SPACE</div>
              {particles.map((particle, i) => (
                <motion.div
                  key={i}
                  className="dimension-particle"
                  initial={{
                    x: particle.startX,
                    y: particle.startY,
                  }}
                  animate={{
                    x: particle.endX,
                    y: particle.endY,
                    opacity: [1, 0.3],
                  }}
                  transition={{
                    duration: 2,
                    delay: i * 0.01,
                  }}
                />
              ))}
            </div>

            <motion.div className="pca-arrow" initial={{ scaleX: 0 }} animate={{ scaleX: 1 }} transition={{ delay: 1, duration: 0.5 }}>
              <span>PCA TRANSFORM</span>
            </motion.div>

            <div className="dimension-cloud low">
              <div className="dimension-label">4D COMPACT SPACE</div>
              <motion.div
                className="compact-representation"
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: 1.5, type: "spring" }}
              >
                {[0, 1, 2, 3].map((i) => (
                  <motion.div
                    key={i}
                    className="compact-dimension"
                    animate={{
                      opacity: [0.6, 1, 0.6],
                    }}
                    transition={{
                      duration: 1,
                      repeat: Infinity,
                      delay: i * 0.2,
                    }}
                  >
                    Q{i}
                  </motion.div>
                ))}
              </motion.div>
            </div>
          </div>

          <div className="stage-metrics">
            <div className="metric-card">
              <div className="metric-label">INPUT</div>
              <div className="metric-value">2048D</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">OUTPUT</div>
              <div className="metric-value">4D</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">VARIANCE</div>
              <div className="metric-value">89%</div>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
