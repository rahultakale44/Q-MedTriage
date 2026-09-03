/**
 * BULK RESULTS STAGE
 * Display batch analysis summary and individual result cards
 */

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { CheckCircle, XCircle, AlertCircle, MessageSquare, RotateCcw } from "lucide-react";
import { ChatInterface } from "../ChatInterface";

export function BulkResultsStage({ batchResults, uploadedFiles, onReset }) {
  const [selectedResult, setSelectedResult] = useState(null);
  const [chatOpen, setChatOpen] = useState(false);

  const { batch_summary, results } = batchResults;

  const openChat = (result) => {
    setSelectedResult(result);
    setChatOpen(true);
  };

  const closeChat = () => {
    setChatOpen(false);
    setSelectedResult(null);
  };

  // Create prediction data for chat context
  const createChatContext = (result) => {
    if (!result.success) return null;

    return {
      triage: {
        prediction: result.prediction,
        confidence: result.confidence,
        priority: result.prediction === "PNEUMONIA" ? "HIGH" : "ROUTINE",
      },
      classical: {
        probability: {
          normal: result.probabilities.NORMAL,
          pneumonia: result.probabilities.PNEUMONIA,
        },
      },
      raw: {
        classifier: result.model_type,
      },
    };
  };

  return (
    <>
      <motion.div
        className="bulk-results-stage"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
      >
        <div className="bulk-results-container">
          {/* Batch Summary */}
          <motion.div
            className="batch-summary"
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            <h2 className="summary-title">BATCH ANALYSIS COMPLETE</h2>
            
            <div className="summary-metrics">
              <div className="metric">
                <div className="metric-value">{batch_summary.total_images}</div>
                <div className="metric-label">Images Submitted</div>
              </div>
              <div className="metric success">
                <div className="metric-value">{batch_summary.successful}</div>
                <div className="metric-label">Successfully Analysed</div>
              </div>
              {batch_summary.rejected > 0 && (
                <div className="metric rejected">
                  <div className="metric-value">{batch_summary.rejected}</div>
                  <div className="metric-label">Rejected by Validation</div>
                </div>
              )}
              {batch_summary.failed > 0 && (
                <div className="metric failed">
                  <div className="metric-value">{batch_summary.failed}</div>
                  <div className="metric-label">Processing Failed</div>
                </div>
              )}
            </div>
          </motion.div>

          {/* Individual Results Grid */}
          <div className="results-grid">
            {results.map((result, index) => {
              // Get the corresponding file for image preview
              const file = uploadedFiles[index];
              const imageUrl = file ? URL.createObjectURL(file) : null;

              return (
                <motion.div
                  key={result.image_id}
                  className={`result-card ${result.status}`}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.3 + index * 0.05 }}
                >
                  {/* Image Preview */}
                  <div className="result-image-container">
                    {imageUrl && (
                      <img
                        src={imageUrl}
                        alt={result.filename}
                        className="result-image"
                      />
                    )}
                    <div className="image-overlay">
                      {result.success && (
                        <CheckCircle size={24} className="status-icon success" />
                      )}
                      {result.status === "rejected" && (
                        <XCircle size={24} className="status-icon rejected" />
                      )}
                      {result.status === "failed" && (
                        <AlertCircle size={24} className="status-icon failed" />
                      )}
                    </div>
                  </div>

                  {/* Result Info */}
                  <div className="result-info">
                    <p className="result-filename">{result.filename}</p>

                    {result.success ? (
                      <>
                        <div className={`result-prediction ${result.prediction.toLowerCase()}`}>
                          {result.prediction}
                        </div>
                        <div className="result-confidence">
                          Confidence: {(result.confidence * 100).toFixed(1)}%
                        </div>
                        <div className="result-probabilities">
                          <div className="prob-bar">
                            <span className="prob-label">NORMAL</span>
                            <div className="prob-bar-fill-container">
                              <div
                                className="prob-bar-fill normal"
                                style={{ width: `${result.probabilities.NORMAL * 100}%` }}
                              />
                            </div>
                            <span className="prob-value">
                              {(result.probabilities.NORMAL * 100).toFixed(1)}%
                            </span>
                          </div>
                          <div className="prob-bar">
                            <span className="prob-label">PNEUMONIA</span>
                            <div className="prob-bar-fill-container">
                              <div
                                className="prob-bar-fill pneumonia"
                                style={{ width: `${result.probabilities.PNEUMONIA * 100}%` }}
                              />
                            </div>
                            <span className="prob-value">
                              {(result.probabilities.PNEUMONIA * 100).toFixed(1)}%
                            </span>
                          </div>
                        </div>

                        <button
                          className="ask-intelligence-button"
                          onClick={() => openChat(result)}
                        >
                          <MessageSquare size={16} />
                          Ask Q-MedTriage
                        </button>
                      </>
                    ) : (
                      <>
                        <div className="result-status-text">
                          {result.status === "rejected" ? "IMAGE REJECTED" : "PROCESSING FAILED"}
                        </div>
                        <div className="result-error-message">
                          {result.reason || result.error || "Unable to process image"}
                        </div>
                        {result.detected_type && (
                          <div className="result-detected-type">
                            Detected: {result.detected_type}
                          </div>
                        )}
                      </>
                    )}
                  </div>
                </motion.div>
              );
            })}
          </div>

          {/* Actions */}
          <div className="bulk-results-actions">
            <button className="new-analysis-button" onClick={onReset}>
              <RotateCcw size={16} />
              New Analysis
            </button>
          </div>
        </div>
      </motion.div>

      {/* Chat Modal */}
      <AnimatePresence>
        {chatOpen && selectedResult && (
          <ChatInterface
            predictionData={createChatContext(selectedResult)}
            image={null}
            onClose={closeChat}
            resultContext={{
              filename: selectedResult.filename,
              prediction: selectedResult.prediction,
              confidence: selectedResult.confidence,
            }}
          />
        )}
      </AnimatePresence>
    </>
  );
}
