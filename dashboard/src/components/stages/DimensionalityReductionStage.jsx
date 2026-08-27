/**
 * DIMENSIONALITY REDUCTION (PCA) STAGE
 */

import { useMemo } from "react";
import { motion } from "framer-motion";

export function DimensionalityReductionStage() {
  // Generate stable, contained positions for particles
  // Particles stay within a controlled boundary: max ±100px horizontally, ±80px vertically
  const particles = useMemo(() => {
    return Array.from({ length: 80 }).map(() => {
      // Initial positions within bounded area
      const baseX = (Math.random() - 0.5) * 160; // -80 to +80
      const baseY = (Math.random() - 0.5) * 120; // -60 to +60
      
      // Subtle floating motion: very small offsets
      const floatX = (Math.random() - 0.5) * 12; // ±6px
      const floatY = (Math.random() - 0.5) * 12; // ±6px
      
      return {
        baseX,
        baseY,
        floatX,
        floatY,
        delay: Math.random() * 2, // stagger animation start
        duration: 3 + Math.random() * 2, // 3-5s duration
      };
    });
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
              <div className="particle-container">
                {particles.map((particle, i) => (
                  <motion.div
                    key={i}
                    className="dimension-particle"
                    initial={{
                      x: particle.baseX,
                      y: particle.baseY,
                      opacity: 0,
                    }}
                    animate={{
                      x: [
                        particle.baseX,
                        particle.baseX + particle.floatX,
                        particle.baseX,
                      ],
                      y: [
                        particle.baseY,
                        particle.baseY + particle.floatY,
                        particle.baseY,
                      ],
                      opacity: [0, 0.8, 0.8, 0.8],
                    }}
                    transition={{
                      duration: particle.duration,
                      delay: particle.delay,
                      repeat: Infinity,
                      ease: "easeInOut",
                    }}
                  />
                ))}
              </div>
            </div>

            <motion.div 
              className="pca-arrow" 
              initial={{ scaleX: 0, opacity: 0 }} 
              animate={{ scaleX: 1, opacity: 1 }} 
              transition={{ delay: 0.8, duration: 0.6, ease: "easeOut" }}
            >
              <span>PCA TRANSFORM</span>
            </motion.div>

            <div className="dimension-cloud low">
              <div className="dimension-label">4D COMPACT SPACE</div>
              <motion.div
                className="compact-representation"
                initial={{ scale: 0, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ delay: 1.2, duration: 0.5, ease: "easeOut" }}
              >
                {[0, 1, 2, 3].map((i) => (
                  <motion.div
                    key={i}
                    className="compact-dimension"
                    initial={{ scale: 0, opacity: 0 }}
                    animate={{ 
                      scale: 1, 
                      opacity: 1,
                    }}
                    transition={{
                      delay: 1.4 + i * 0.15,
                      duration: 0.4,
                      ease: "easeOut",
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
