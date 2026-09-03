/**
 * ANALYSIS MODE SELECTION
 * Choose between single image or bulk analysis
 */

import { motion } from "framer-motion";
import { Image as ImageIcon, Layers, Microscope } from "lucide-react";

export function AnalysisModeSelection({ onSelectMode }) {
  return (
    <motion.div
      className="mode-selection-stage"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.5 }}
    >
      {/* Animated Background */}
      <div className="mode-bg-animation">
        <div className="mode-particle"></div>
        <div className="mode-particle"></div>
        <div className="mode-particle"></div>
        <div className="mode-particle"></div>
        <div className="mode-particle"></div>
        <div className="mode-grid"></div>
      </div>

      <div className="mode-selection-container">
        {/* Q-MedTriage Branding */}
        <motion.div 
          className="mode-branding"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          <div className="brand-icon">
            <Microscope size={24} />
          </div>
          <div className="brand-text">
            <h2 className="brand-name">Q-MEDTRIAGE</h2>
            <span className="brand-tagline">QUANTUM MEDICAL INTELLIGENCE</span>
          </div>
        </motion.div>

        <div className="mode-selection-header">
          <h1>Begin Your Analysis</h1>
          <p>Choose your analysis mode for AI-assisted chest X-ray triage</p>
        </div>

        <div className="mode-cards-grid">
          {/* Single Analysis Mode */}
          <motion.div
            className="mode-card"
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={() => onSelectMode("single")}
          >
            <div className="mode-icon single">
              <ImageIcon size={40} />
            </div>
            <h3 className="mode-title">Single Analysis</h3>
            <p className="mode-description">
              Detailed individual chest X-ray analysis with complete diagnostic pipeline
            </p>
            <div className="mode-features">
              <div className="mode-feature">
                <span className="feature-dot"></span>
                <span>Comprehensive AI analysis</span>
              </div>
              <div className="mode-feature">
                <span className="feature-dot"></span>
                <span>Q-MedTriage Intelligence</span>
              </div>
              <div className="mode-feature">
                <span className="feature-dot"></span>
                <span>Evidence-grounded reasoning</span>
              </div>
            </div>
            <button className="mode-select-button">
              Select Single Image
            </button>
          </motion.div>

          {/* Bulk Analysis Mode */}
          <motion.div
            className="mode-card bulk"
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={() => onSelectMode("bulk")}
          >
            <div className="mode-icon bulk">
              <Layers size={40} />
            </div>
            <h3 className="mode-title">Bulk Analysis</h3>
            <p className="mode-description">
              Process up to 50 chest X-rays simultaneously with independent AI results
            </p>
            <div className="mode-features">
              <div className="mode-feature">
                <span className="feature-dot"></span>
                <span>Batch processing (max 50)</span>
              </div>
              <div className="mode-feature">
                <span className="feature-dot"></span>
                <span>Independent validation per image</span>
              </div>
              <div className="mode-feature">
                <span className="feature-dot"></span>
                <span>Context-aware Q&A per result</span>
              </div>
            </div>
            <button className="mode-select-button bulk">
              Select Multiple Images
            </button>
          </motion.div>
        </div>

        <div className="mode-info">
          <div className="info-item">
            <span className="info-label">SUPPORTED</span>
            <span className="info-value">Chest X-rays, radiographs</span>
          </div>
          <div className="info-item">
            <span className="info-label">FORMATS</span>
            <span className="info-value">PNG / JPG / JPEG / WEBP</span>
          </div>
          <div className="info-item">
            <span className="info-label">PRIVACY</span>
            <span className="info-value">Images processed securely</span>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
