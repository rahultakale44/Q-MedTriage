/**
 * EVIDENCE RETRIEVAL STAGE - Stage 05
 * Semantic search visualization with real RAG data
 */

import { motion } from "framer-motion";
import { Database, FileText, ArrowDown } from "lucide-react";

export function EvidenceRetrievalStage({ predictionData }) {
  // Use real evidence if available, otherwise show placeholders
  const evidence = predictionData?.evidence?.results || [
    { id: 1, title: "Clinical diagnostic criteria", relevance: 0.92 },
    { id: 2, title: "Imaging pattern analysis", relevance: 0.87 },
    { id: 3, title: "Evidence-based guidelines", relevance: 0.81 },
  ];

  return (
    <motion.div
      className="evidence-stage"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    >
      <div className="stage-container">
        <div className="stage-header">
          <div className="stage-number">05</div>
          <div className="stage-title-group">
            <h3 className="stage-label">EVIDENCE RETRIEVAL</h3>
            <h2 className="stage-title">Semantic knowledge search</h2>
            <p className="stage-description">
              Vector database retrieval identifying relevant medical knowledge for prediction context
            </p>
          </div>
        </div>

        <div className="stage-content">
          <div className="evidence-retrieval-visualization">
            {/* Database source */}
            <motion.div
              className="evidence-database-card"
              initial={{ scale: 0, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ type: "spring", delay: 0.2, stiffness: 200 }}
            >
              <Database size={40} className="database-icon" />
              <div className="database-title">VECTOR DATABASE</div>
              <div className="database-details">
                <div className="database-detail-item">
                  <span className="detail-label">ENGINE</span>
                  <span className="detail-value">FAISS</span>
                </div>
                <div className="database-detail-item">
                  <span className="detail-label">EMBEDDINGS</span>
                  <span className="detail-value">384D</span>
                </div>
                <div className="database-detail-item">
                  <span className="detail-label">DOCUMENTS</span>
                  <span className="detail-value">22</span>
                </div>
              </div>
            </motion.div>

            {/* Retrieval flow */}
            <motion.div
              className="retrieval-flow-indicator"
              initial={{ opacity: 0, scaleY: 0 }}
              animate={{ opacity: 1, scaleY: 1 }}
              transition={{ delay: 0.5, duration: 0.4 }}
            >
              <ArrowDown size={24} />
              <div className="flow-label-text">SEMANTIC QUERY</div>
            </motion.div>

            {/* Retrieved evidence cards */}
            <div className="evidence-results-container">
              <div className="results-header">RETRIEVED EVIDENCE</div>
              <div className="evidence-cards-list">
                {evidence.slice(0, 3).map((item, index) => {
                  const relevance = typeof item.relevance === 'number' 
                    ? item.relevance 
                    : parseFloat(item.relevance) || 0.85;
                  const relevancePercent = relevance < 1 ? relevance * 100 : relevance;

                  return (
                    <motion.div
                      key={item.id || index}
                      className="evidence-result-card"
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 0.8 + index * 0.15 }}
                    >
                      <FileText size={18} className="evidence-card-icon" />
                      <div className="evidence-card-content">
                        <div className="evidence-card-title">{item.title}</div>
                        <div className="evidence-card-meta">
                          <span className="relevance-score">
                            {relevancePercent.toFixed(0)}% match
                          </span>
                          <span className="evidence-source">Medical Knowledge</span>
                        </div>
                      </div>
                      <motion.div
                        className="evidence-check-icon"
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        transition={{ delay: 1 + index * 0.15, type: "spring" }}
                      >
                        ✓
                      </motion.div>
                    </motion.div>
                  );
                })}
              </div>
            </div>
          </div>

          <div className="stage-metrics">
            <div className="metric-card">
              <div className="metric-label">METHOD</div>
              <div className="metric-value">FAISS</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">RETRIEVED</div>
              <div className="metric-value">{evidence.length}</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">TOP MATCH</div>
              <div className="metric-value">
                {((evidence[0]?.relevance || 0.92) * 100).toFixed(0)}%
              </div>
            </div>
            <div className="metric-card">
              <div className="metric-label">STATUS</div>
              <div className="metric-value status-ready">COMPLETE</div>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
