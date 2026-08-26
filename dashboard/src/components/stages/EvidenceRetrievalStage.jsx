/**
 * EVIDENCE RETRIEVAL (RAG) STAGE
 */

import { motion } from "framer-motion";
import { Database, FileSearch } from "lucide-react";

const MOCK_EVIDENCE = [
  { id: 1, title: "Clinical diagnostic criteria", relevance: 92 },
  { id: 2, title: "Imaging pattern analysis", relevance: 87 },
  { id: 3, title: "Evidence-based guidelines", relevance: 81 },
];

export function EvidenceRetrievalStage({ predictionData }) {
  const evidence = predictionData?.evidence?.results || MOCK_EVIDENCE;

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
            <h2 className="stage-title">Bring the evidence</h2>
            <p className="stage-description">
              Semantic search retrieving relevant medical knowledge from vector database
            </p>
          </div>
        </div>

        <div className="stage-content">
          <div className="evidence-visualization">
            <motion.div
              className="evidence-database"
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ type: "spring", delay: 0.2 }}
            >
              <Database size={48} />
              <div className="database-label">VECTOR DATABASE</div>
              <div className="database-sublabel">FAISS + Sentence Transformers</div>
            </motion.div>

            <motion.div
              className="evidence-flow"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.5 }}
            >
              <div className="flow-line" />
              <div className="flow-label">SEMANTIC QUERY</div>
            </motion.div>

            <div className="evidence-results">
              {evidence.slice(0, 3).map((item, index) => (
                <motion.div
                  key={item.id || index}
                  className="evidence-card"
                  initial={{ opacity: 0, x: 50 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.8 + index * 0.2 }}
                >
                  <FileSearch size={20} className="evidence-icon" />
                  <div className="evidence-content">
                    <div className="evidence-title">{item.title}</div>
                    <div className="evidence-meta">
                      <span className="evidence-relevance">
                        {Math.round((item.relevance || item.relevance * 100))}% match
                      </span>
                      <span className="evidence-source">Medical Knowledge Base</span>
                    </div>
                  </div>
                  <motion.div
                    className="evidence-indicator"
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ delay: 1 + index * 0.2, type: "spring" }}
                  >
                    ✓
                  </motion.div>
                </motion.div>
              ))}
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
              <div className="metric-label">STATUS</div>
              <div className="metric-value status-ready">COMPLETE</div>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
