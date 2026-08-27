/**
 * FEATURE EXTRACTION STAGE - Stage 03
 * Compact Professional Design: Dark theme, information-dense layout
 */

import { motion } from "framer-motion";
import { ArrowRight, Network, Layers, Activity, Box } from "lucide-react";

export function FeatureExtractionStage({ image }) {
  const convLayers = [
    { id: 1, filters: 64, width: 70, height: 140 },
    { id: 2, filters: 256, width: 60, height: 120 },
    { id: 3, filters: 512, width: 52, height: 100 },
    { id: 4, filters: 1024, width: 44, height: 80 },
    { id: 5, filters: 2048, width: 36, height: 60 },
  ];

  return (
    <motion.div
      className="feature-stage"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    >
      <div className="stage-container">
        {/* Header Section */}
        <div className="stage-header">
          <div className="stage-number">03</div>
          <div className="stage-title-group">
            <h3 className="stage-label">FEATURE EXTRACTION</h3>
            <h2 className="stage-title">Extract deep visual features</h2>
            <p className="stage-description">
              Convolutional neural network extracts high-level visual patterns from the preprocessed chest radiograph.
            </p>
          </div>
        </div>

        <div className="stage-content">
          {/* Main Feature Pipeline Container */}
          <div className="feature-pipeline-container">
            
            {/* Main Three-Section Pipeline */}
            <div className="feature-main-pipeline">
              
              {/* LEFT: Model Input */}
              <motion.div
                className="feature-panel-compact"
                initial={{ opacity: 0, y: 15 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
              >
                <div className="panel-header-compact">
                  <h4 className="panel-title-compact">MODEL INPUT</h4>
                  <p className="panel-subtitle-compact">Preprocessed Chest Radiograph</p>
                </div>
                <div className="panel-content-compact">
                  <div className="input-image-container">
                    <img src={image} alt="Chest X-ray" className="input-xray-image" />
                    <div className="corner-frame">
                      <div className="corner-accent tl"></div>
                      <div className="corner-accent tr"></div>
                      <div className="corner-accent bl"></div>
                      <div className="corner-accent br"></div>
                    </div>
                  </div>
                </div>
              </motion.div>

              {/* Arrow 1 */}
              <motion.div
                className="pipeline-arrow"
                initial={{ scaleX: 0 }}
                animate={{ scaleX: 1 }}
                transition={{ delay: 0.5, duration: 0.3 }}
              >
                <ArrowRight size={24} />
              </motion.div>

              {/* CENTER: Feature Extraction Process */}
              <motion.div
                className="feature-panel-compact feature-process-container"
                initial={{ opacity: 0, y: 15 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.6 }}
              >
                <div className="panel-header-compact">
                  <h4 className="panel-title-compact">FEATURE EXTRACTION PROCESS</h4>
                  <p className="panel-subtitle-compact">ResNet-50 Deep Convolutional Network</p>
                </div>
                <div className="panel-content-compact">
                  <div className="cnn-architecture">
                    {convLayers.map((layer, index) => (
                      <motion.div
                        key={layer.id}
                        className="conv-stage"
                        initial={{ opacity: 0, scale: 0.85 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ delay: 0.8 + index * 0.1, duration: 0.3 }}
                      >
                        <div className="conv-feature-map">
                          <div
                            className="feature-map-stack"
                            style={{
                              width: `${layer.width}px`,
                              height: `${layer.height}px`,
                            }}
                          >
                            {/* Create stacked layers effect */}
                            {[...Array(4)].map((_, i) => (
                              <div
                                key={i}
                                className="feature-map-layer"
                                style={{
                                  width: `${layer.width}px`,
                                  height: `${layer.height}px`,
                                  transform: `translateZ(${i * 2}px) translateX(${i * 1.5}px) translateY(${i * -1.5}px)`,
                                  zIndex: 10 - i,
                                  bottom: 0,
                                  left: 0,
                                }}
                              />
                            ))}
                          </div>
                        </div>
                        <div className="conv-stage-info">
                          <div className="conv-stage-name">CONV {layer.id}</div>
                          <div className="conv-stage-filters">{layer.filters} Filters</div>
                        </div>
                      </motion.div>
                    ))}
                  </div>
                  
                  {/* Description Strip */}
                  <motion.div
                    className="cnn-description-strip"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 1.5 }}
                  >
                    <Box size={18} className="cnn-desc-icon" />
                    <div className="cnn-desc-content">
                      <div className="cnn-desc-title">Feature Maps</div>
                      <div className="cnn-desc-text">
                        Hierarchical feature learning from low-level to high-level patterns
                      </div>
                    </div>
                  </motion.div>
                </div>
              </motion.div>

              {/* Arrow 2 */}
              <motion.div
                className="pipeline-arrow"
                initial={{ scaleX: 0 }}
                animate={{ scaleX: 1 }}
                transition={{ delay: 1.6, duration: 0.3 }}
              >
                <ArrowRight size={24} />
              </motion.div>

              {/* RIGHT: Extracted Feature Representation */}
              <motion.div
                className="feature-panel-compact"
                initial={{ opacity: 0, y: 15 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 1.8 }}
              >
                <div className="panel-header-compact">
                  <h4 className="panel-title-compact">EXTRACTED FEATURE REPRESENTATION</h4>
                  <p className="panel-subtitle-compact">High-Dimensional Feature Vector</p>
                </div>
                <div className="panel-content-compact">
                  <div className="feature-vector-container">
                    <div className="vector-display">
                      {[...Array(16)].map((_, i) => (
                        <motion.div
                          key={i}
                          className="vector-dot-compact"
                          initial={{ opacity: 0, scale: 0 }}
                          animate={{ opacity: 1, scale: 1 }}
                          transition={{ delay: 2 + i * 0.02 }}
                          style={{ animationDelay: `${i * 0.15}s` }}
                        />
                      ))}
                      <div className="vector-ellipsis">•••</div>
                    </div>
                    <div className="vector-dimension">2048D</div>
                    <div className="vector-label">Feature Vector</div>
                    <p className="vector-description">
                      Numerical representation capturing important patterns and structures from the image.
                    </p>
                  </div>
                </div>
              </motion.div>
            </div>
          </div>

          {/* Metrics Bar */}
          <motion.div
            className="metrics-bar"
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 2.2 }}
          >
            <div className="metric-item">
              <Network size={22} className="metric-icon-compact" />
              <div className="metric-details">
                <div className="metric-label-compact">MODEL</div>
                <div className="metric-value-compact">ResNet-50</div>
              </div>
            </div>
            <div className="metric-item">
              <Layers size={22} className="metric-icon-compact" />
              <div className="metric-details">
                <div className="metric-label-compact">FEATURE DIMENSION</div>
                <div className="metric-value-compact">2048D</div>
              </div>
            </div>
            <div className="metric-item">
              <Layers size={22} className="metric-icon-compact" />
              <div className="metric-details">
                <div className="metric-label-compact">LAYERS UTILIZED</div>
                <div className="metric-value-compact">49</div>
              </div>
            </div>
            <div className="metric-item">
              <Activity size={22} className="metric-icon-compact" />
              <div className="metric-details">
                <div className="metric-label-compact">ACTIVATION FUNCTION</div>
                <div className="metric-value-compact">ReLU</div>
              </div>
            </div>
          </motion.div>

          {/* Explanation Panel */}
          <motion.div
            className="explanation-compact"
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 2.4 }}
          >
            <div className="explanation-icon-compact">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="12" cy="12" r="10"/>
                <path d="M12 16v-4M12 8h.01"/>
              </svg>
            </div>
            <div className="explanation-text-container">
              <h4 className="explanation-heading">What this means</h4>
              <p className="explanation-paragraph">
                The deep learning model analyzes the image at multiple levels and extracts rich visual patterns such as 
                edges, textures, shapes, and anatomical structures. These patterns are converted into a 2048-dimensional 
                feature vector for further analysis in the next stages.
              </p>
            </div>
          </motion.div>
        </div>
      </div>
    </motion.div>
  );
}
