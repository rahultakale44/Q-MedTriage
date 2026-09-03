/**
 * PROFESSIONAL IMAGE UPLOAD STAGE
 */

import { useState, useRef } from "react";
import { Upload, Image as ImageIcon, AlertCircle, Microscope } from "lucide-react";
import { motion } from "framer-motion";
import { validateImageFile } from "../../services/api";

export function UploadStage({ onImageUpload, onBack }) {
  const [dragActive, setDragActive] = useState(false);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    setError(null);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e) => {
    e.preventDefault();
    setError(null);
    
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleFile = (file) => {
    const validation = validateImageFile(file);
    
    if (!validation.valid) {
      setError(validation.errors[0]);
      return;
    }

    onImageUpload(file);
  };

  const handleBrowseClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <motion.div
      className="upload-stage"
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

      <div className="upload-container">
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

        <div className="upload-header">
          <h1>Begin Your Analysis</h1>
          <p>Upload a medical image for AI-assisted triage and evidence-grounded analysis</p>
        </div>

        <div
          className={`upload-dropzone ${dragActive ? "active" : ""} ${error ? "error" : ""}`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          onClick={handleBrowseClick}
        >
          <div className="dropzone-content">
            {error ? (
              <>
                <AlertCircle size={48} className="upload-icon error-icon" />
                <p className="error-message">{error}</p>
                <button type="button" className="upload-button" onClick={() => setError(null)}>
                  Try Again
                </button>
              </>
            ) : (
              <>
                <ImageIcon size={48} className="upload-icon" />
                <p className="dropzone-primary">Drop medical image here</p>
                <p className="dropzone-or">or</p>
                <button type="button" className="upload-button">
                  <Upload size={16} />
                  Browse Files
                </button>
                <p className="dropzone-formats">PNG / JPG / JPEG / WEBP</p>
              </>
            )}
          </div>

          <input
            ref={fileInputRef}
            type="file"
            accept="image/png,image/jpeg,image/jpg,image/webp"
            onChange={handleChange}
            style={{ display: "none" }}
          />
        </div>

        <div className="upload-info">
          <div className="info-item">
            <span className="info-label">SUPPORTED</span>
            <span className="info-value">Chest X-rays, radiographs</span>
          </div>
          <div className="info-item">
            <span className="info-label">MAX SIZE</span>
            <span className="info-value">10MB</span>
          </div>
          <div className="info-item">
            <span className="info-label">PRIVACY</span>
            <span className="info-value">Images processed securely</span>
          </div>
        </div>

        {onBack && (
          <button className="back-button" onClick={onBack}>
            ← Back to Mode Selection
          </button>
        )}
      </div>
    </motion.div>
  );
}
