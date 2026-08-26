/**
 * AI REASONING (LLM) STAGE
 */

import { motion } from "framer-motion";
import { Sparkles, ArrowDown } from "lucide-react";

export function ReasoningStage({ predictionData }) {
  const prediction = predictionData?.triage?.prediction || "ANALYZING";
  const confidence = predictionData?.triage?.confidence || 0;

  return (
    <motion.div
      className="reasoning-stage"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    >
      <div className="stage-container">
        <div className="stage-header">
          <div className="stage-number">06</div>
          <div className="stage-title-group">
            <h3 className="stage-label">AI REASONING</h3>
            <h2 className="stage-title">Connect the dots</h2>
            <p className="stage-description">
              LLM synthesizing model prediction with retrieved evidence for grounded explanation
            </p>
          </div>
        </div>

        <div className="stage-content">
          <div className="reasoning-visualization">
            <div className="reasoning-flow">
              <motion.div
                className="reasoning-source"
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
              >
                <div className="source-label">MODEL PREDICTION</div>
                <div className="source-content">
                  {prediction} · {(confidence * 100).toFixed(1)}%
                </div>
              </motion.div>

              <ArrowDown size={24} className="reasoning-arrow" />

              <motion.div
                className="reasoning-source"
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 }}
              >
                <div className="source-label">RETRIEVED EVIDENCE</div>
                <div className="source-content">3 sources</div>
              </motion.div>

              <ArrowDown size={24} className="reasoning-arrow" />

              <motion.div
                className="reasoning-llm"
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: 0.8, type: "spring" }}
              >
                <Sparkles size={32} />
                <div className="llm-label">LARGE LANGUAGE MODEL</div>
                <motion.div
                  className="llm-activity"
                  animate={{ opacity: [0.3, 1, 0.3] }}
                  transition={{ duration: 2, repeat: Infinity }}
                >
                  Synthesizing...
                </motion.div>
              </motion.div>

              <ArrowDown size={24} className="reasoning-arrow" />

              <motion.div
                className="reasoning-output"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 1.2 }}
              >
                <div className="output-label">GROUNDED EXPLANATION</div>
                <motion.div
                  className="output-content"
                  initial={{ height: 0 }}
                  animate={{ height: "auto" }}
                  transition={{ delay: 1.5, duration: 0.5 }}
                >
                  {predictionData?.reasoning?.explanation || 
                    "Generating evidence-based clinical reasoning..."}
                </motion.div>
              </motion.div>
            </div>
          </div>

          <div className="stage-metrics">
            <div className="metric-card">
              <div className="metric-label">MODEL</div>
              <div className="metric-value">GPT-4</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">SOURCES</div>
              <div className="metric-value">3</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">TYPE</div>
              <div className="metric-value">GROUNDED</div>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
