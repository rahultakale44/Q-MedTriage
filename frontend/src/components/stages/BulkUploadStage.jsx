/**
 * BULK UPLOAD STAGE
 * Upload multiple chest X-rays for batch analysis
 */

import { useState, useRef } from "react";
import { Upload, X, AlertCircle, CheckCircle, Microscope } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { validateImageFile } from "../../services/api";

const MAX_IMAGES = 50;

export function BulkUploadStage({ onImagesUpload, onBack }) {
  const [selectedFiles, setSelectedFiles] = useState([]);
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

    if (e.dataTransfer.files) {
      handleFiles(Array.from(e.dataTransfer.files));
    }
  };

  const handleChange = (e) => {
    e.preventDefault();
    setError(null);
    
    if (e.target.files) {
      handleFiles(Array.from(e.target.files));
    }
  };

  const handleFiles = (files) => {
    // Check total count
    const totalCount = selectedFiles.length + files.length;
    if (totalCount > MAX_IMAGES) {
      setError(`Maximum ${MAX_IMAGES} images allowed. You selected ${totalCount} images.`);
      return;
    }

    // Validate each file
    const validFiles = [];
    for (const file of files) {
      const validation = validateImageFile(file);
      if (!validation.valid) {
        setError(validation.errors[0]);
        return;
      }
      validFiles.push(file);
    }

    setSelectedFiles([...selectedFiles, ...validFiles]);
  };

  const removeFile = (index) => {
    setSelectedFiles(selectedFiles.filter((_, i) => i !== index));
    setError(null);
  };

  const clearAll = () => {
    setSelectedFiles([]);
    setError(null);
  };

  const handleBrowseClick = () => {
    fileInputRef.current?.click();
  };

  const handleStartAnalysis = () => {
    if (selectedFiles.length > 0) {
      onImagesUpload(selectedFiles);
    }
  };

  return (
    <motion.div
      className="bulk-upload-stage"
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

      <div className="bulk-upload-container">
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

        <div className="bulk-upload-header">
          <h1>Bulk Analysis</h1>
          <p>Upload up to {MAX_IMAGES} chest X-rays for simultaneous AI analysis</p>
        </div>

        {selectedFiles.length === 0 ? (
          <>
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
                    <button type="button" className="upload-button" onClick={(e) => { e.stopPropagation(); setError(null); }}>
                      Try Again
                    </button>
                  </>
                ) : (
                  <>
                    <Upload size={48} className="upload-icon" />
                    <p className="dropzone-primary">Drop multiple images here</p>
                    <p className="dropzone-or">or</p>
                    <button type="button" className="upload-button">
                      <Upload size={16} />
                      Browse Files
                    </button>
                    <p className="dropzone-formats">Select up to {MAX_IMAGES} chest X-ray images</p>
                  </>
                )}
              </div>

              <input
                ref={fileInputRef}
                type="file"
                accept="image/png,image/jpeg,image/jpg,image/webp"
                multiple
                onChange={handleChange}
                style={{ display: "none" }}
              />
            </div>

            <button className="back-button" onClick={onBack}>
              ← Back to Mode Selection
            </button>
          </>
        ) : (
          <>
            <div className="selected-files-header">
              <div className="files-count">
                <CheckCircle size={20} />
                <span>{selectedFiles.length} / {MAX_IMAGES} Images Selected</span>
              </div>
              <div className="files-actions">
                <button className="start-bulk-button-top" onClick={handleStartAnalysis}>
                  Start Bulk Triage ({selectedFiles.length} Images)
                </button>
                <button className="add-more-button" onClick={handleBrowseClick}>
                  + Add More
                </button>
                <button className="clear-button" onClick={clearAll}>
                  Clear All
                </button>
              </div>
            </div>

            {error && (
              <div className="error-banner">
                <AlertCircle size={16} />
                <span>{error}</span>
              </div>
            )}

            <div className="selected-files-grid">
              <AnimatePresence>
                {selectedFiles.map((file, index) => (
                  <motion.div
                    key={`${file.name}-${index}`}
                    className="file-preview-card"
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    exit={{ opacity: 0, scale: 0.9 }}
                    transition={{ duration: 0.2 }}
                  >
                    <div className="file-preview-image">
                      <img src={URL.createObjectURL(file)} alt={file.name} />
                    </div>
                    <div className="file-preview-info">
                      <p className="file-name">{file.name}</p>
                      <p className="file-size">{(file.size / 1024).toFixed(1)} KB</p>
                    </div>
                    <button
                      className="file-remove-button"
                      onClick={() => removeFile(index)}
                    >
                      <X size={16} />
                    </button>
                  </motion.div>
                ))}
              </AnimatePresence>
            </div>

            <input
              ref={fileInputRef}
              type="file"
              accept="image/png,image/jpeg,image/jpg,image/webp"
              multiple
              onChange={handleChange}
              style={{ display: "none" }}
            />

            <div className="bulk-actions-bottom">
              <button className="back-button-secondary" onClick={onBack}>
                Back
              </button>
            </div>
          </>
        )}
      </div>
    </motion.div>
  );
}
