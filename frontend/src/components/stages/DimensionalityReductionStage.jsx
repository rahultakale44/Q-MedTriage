/**
 * DIMENSIONALITY REDUCTION (PCA) STAGE
 * Reference-based redesign: Balanced, premium UI
 */

import { useMemo } from "react";
import { motion } from "framer-motion";
import { ArrowRight, Layers, TrendingDown, Maximize2 } from "lucide-react";

export function DimensionalityReductionStage() {
  // Generate dense particle cloud for high-dimensional space
  const particles = useMemo(() => {
    return Array.from({ length: 120 }).map(() => {
      // More particles distributed across larger area for richer visualization
      const baseX = (Math.random() - 0.5) * 240; // -120 to +120
      const baseY = (Math.random() - 0.5) * 180; // -90 to +90
      const baseZ = (Math.random() - 0.5) * 100; // depth illusion
      
      // Subtle floating motion
      const floatX = (Math.random() - 0.5) * 8;
      const floatY = (Math.random() - 0.5) * 8;
      
      return {
        baseX,
        baseY,
        baseZ,
        floatX,
        floatY,
        delay: Math.random() * 2,
        duration: 4 + Math.random() * 2,
        size: 3 + Math.random() * 3, // varying sizes
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
        {/* Header Section */}
        <div className="stage-header">
          <div className="stage-number">04</div>
          <div className="stage-title-group">
            <h3 className="stage-label">DIMENSIONALITY REDUCTION</h3>
            <h2 className="stage-title">Compress intelligence</h2>
            <p className="stage-description">
              PCA projection reducing 2048D features to compact 4D representation
            </p>
          </div>
        </div>

        <div className="stage-content">
          {/* Main PCA Visualization - Three Sections */}
          <div className="pca-main-visualization">
            
            {/* LEFT PANEL: High-Dimensional Space */}
            <motion.div
              className="pca-panel pca-high-dimensional-panel"
              initial={{ opacity: 0, x: -30 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2, duration: 0.6 }}
            >
              <div className="pca-panel-header">
                <h4 className="pca-panel-title">2048D HIGH-DIMENSIONAL SPACE</h4>
              </div>
              <div className="pca-panel-content">
                <div className="high-dimensional-visualization">
                  {/* Grid background for structure */}
                  <div className="dimension-grid">
                    {[...Array(12)].map((_, i) => (
                      <div key={`h-${i}`} className="grid-line horizontal" style={{ top: `${(i + 1) * 8.33}%` }} />
                    ))}
                    {[...Array(12)].map((_, i) => (
                      <div key={`v-${i}`} className="grid-line vertical" style={{ left: `${(i + 1) * 8.33}%` }} />
                    ))}
                  </div>
                  
                  {/* Dense particle cloud */}
                  <div className="particle-cloud-container">
                    {particles.map((particle, i) => (
                      <motion.div
                        key={i}
                        className="dimension-particle-dot"
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
                          opacity: [0, 0.7, 0.7, 0.7],
                        }}
                        transition={{
                          duration: particle.duration,
                          delay: particle.delay,
                          repeat: Infinity,
                          ease: "easeInOut",
                        }}
                        style={{
                          width: `${particle.size}px`,
                          height: `${particle.size}px`,
                        }}
                      />
                    ))}
                  </div>

                  {/* Feature density indicator */}
                  <div className="feature-density-label">
                    Dense feature space
                  </div>
                </div>
              </div>
            </motion.div>

            {/* CENTER: PCA Transformation */}
            <motion.div
              className="pca-transform-section"
              initial={{ scale: 0, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ delay: 0.8, duration: 0.5, type: "spring", stiffness: 200 }}
            >
              <div className="transform-icon-container">
                <ArrowRight size={32} className="transform-arrow-icon" />
              </div>
              <div className="transform-label-group">
                <div className="transform-label">PCA</div>
                <div className="transform-sublabel">TRANSFORM</div>
              </div>
            </motion.div>

            {/* RIGHT PANEL: 4D Compact Space */}
            <motion.div
              className="pca-panel pca-compact-panel"
              initial={{ opacity: 0, x: 30 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 1.2, duration: 0.6 }}
            >
              <div className="pca-panel-header">
                <h4 className="pca-panel-title">4D COMPACT SPACE</h4>
              </div>
              <div className="pca-panel-content">
                <div className="compact-components-grid">
                  {[0, 1, 2, 3].map((i) => (
                    <motion.div
                      key={i}
                      className="compact-component-card"
                      initial={{ scale: 0, opacity: 0 }}
                      animate={{ scale: 1, opacity: 1 }}
                      transition={{
                        delay: 1.4 + i * 0.1,
                        duration: 0.4,
                        type: "spring",
                        stiffness: 200,
                      }}
                    >
                      <div className="component-visualization">
                        {/* Cross/axis indicator */}
                        <div className="component-axis horizontal"></div>
                        <div className="component-axis vertical"></div>
                        {/* Center point */}
                        <motion.div
                          className="component-center-point"
                          animate={{
                            boxShadow: [
                              "0 0 8px rgba(0, 230, 255, 0.6)",
                              "0 0 16px rgba(0, 230, 255, 1)",
                              "0 0 8px rgba(0, 230, 255, 0.6)",
                            ],
                          }}
                          transition={{
                            duration: 2,
                            repeat: Infinity,
                            delay: i * 0.2,
                          }}
                        />
                      </div>
                      <div className="component-label">Q{i}</div>
                    </motion.div>
                  ))}
                </div>
              </div>
            </motion.div>
          </div>

          {/* Bottom Statistics Section */}
          <motion.div
            className="pca-statistics-section"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 1.8 }}
          >
            <div className="pca-stat-card">
              <Maximize2 size={24} className="stat-icon-pca" />
              <div className="stat-content-pca">
                <div className="stat-label-pca">INPUT DIMENSION</div>
                <div className="stat-value-pca">2048D</div>
              </div>
            </div>
            <div className="pca-stat-card">
              <TrendingDown size={24} className="stat-icon-pca" />
              <div className="stat-content-pca">
                <div className="stat-label-pca">OUTPUT DIMENSION</div>
                <div className="stat-value-pca">4D</div>
              </div>
            </div>
            <div className="pca-stat-card">
              <Layers size={24} className="stat-icon-pca" />
              <div className="stat-content-pca">
                <div className="stat-label-pca">EXPLAINED VARIANCE</div>
                <div className="stat-value-pca">89%</div>
              </div>
            </div>
          </motion.div>

          {/* Explanation Panel */}
          <motion.div
            className="pca-explanation-panel"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 2.0 }}
          >
            <div className="explanation-icon-pca">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="12" cy="12" r="10"/>
                <path d="M12 16v-4M12 8h.01"/>
              </svg>
            </div>
            <div className="explanation-content-pca">
              <h4 className="explanation-title-pca">What this means</h4>
              <p className="explanation-text-pca">
                Principal Component Analysis (PCA) compresses the 2048-dimensional feature representation into 
                just 4 meaningful components while preserving 89% of the diagnostic information. This reduces 
                computational complexity and focuses on the most important patterns for classification.
              </p>
            </div>
          </motion.div>
        </div>
      </div>
    </motion.div>
  );
}
