/**
 * AI REASONING STAGE - Stage 06
 * LLM synthesis: Prediction + Evidence → Grounded Explanation
 */

import { motion } from "framer-motion";
import { Sparkles, ArrowDown, Brain } from "lucide-react";

export function ReasoningStage({ predictionData }) {
  const prediction = predictionData?.triage?.prediction || "ANALYZING";
  const confidence = predictionData?.triage?.confidence || 0;
  const evidenceCount = predictionData?.evidence?.results?.length || 3;

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
            <h3 className="stage-label">CLINICAL REASONING</h3>
            <h2 className="stage-title">Synthesize explanation</h2>
            <p className="stage-description">
              Large language model generating evidence-grounded clinical reasoning from prediction and retrieved knowledge
            </p>
          </div>
        </div>

        <div className="stage-content">
          <div className="reasoning-synthesis-visualization">
            {/* Input 1: Model Prediction */}
            <motion.div
              className="reasoning-input-card"
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
            >
              <div className="input-card-label">MODEL PREDICTION</div>
              <div className="input-card-value">
                {prediction} · {(confidence * 100).toFixed(1)}% confidence
              </div>
            </motion.div>

            <motion.div
              className="reasoning-arrow-down"
              initial={{ opacity: 0, scaleY: 0 }}
              animate={{ opacity: 1, scaleY: 1 }}
              transition={{ delay: 0.4 }}
            >
              <ArrowDown size={20} />
            </motion.div>

            {/* Input 2: Retrieved Evidence */}
            <motion.div
              className="reasoning-input-card"
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
            >
              <div className="input-card-label">RETRIEVED EVIDENCE</div>
              <div className="input-card-value">
                {evidenceCount} medical knowledge sources
              </div>
            </motion.div>

            <motion.div
              className="reasoning-arrow-down"
              initial={{ opacity: 0, scaleY: 0 }}
              animate={{ opacity: 1, scaleY: 1 }}
              transition={{ delay: 0.7 }}
            >
              <ArrowDown size={20} />
            </motion.div>

            {/* LLM Synthesizer */}
            <motion.div
              className="reasoning-llm-card"
              initial={{ scale: 0, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ delay: 0.9, type: "spring", stiffness: 200 }}
            >
              <div className="llm-icon-container">
                <Brain size={32} />
                <Sparkles size={20} className="llm-sparkle" />
              </div>
              <div className="llm-model-label">LARGE LANGUAGE MODEL</div>
              <div className="llm-model-name">Gemini</div>
              <motion.div
                className="llm-processing-indicator"
                animate={{ opacity: [0.4, 1, 0.4] }}
                transition={{ duration: 2, repeat: Infinity }}
              >
                Synthesizing reasoning...
              </motion.div>
            </motion.div>

            <motion.div
              className="reasoning-arrow-down"
              initial={{ opacity: 0, scaleY: 0 }}
              animate={{ opacity: 1, scaleY: 1 }}
              transition={{ delay: 1.2 }}
            >
              <ArrowDown size={20} />
            </motion.div>

            {/* Output: Grounded Explanation */}
            <motion.div
              className="reasoning-output-card"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 1.4 }}
            >
              <div className="output-card-label">GROUNDED EXPLANATION</div>
              <motion.div
                className="output-card-content"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 1.7 }}
              >
                {predictionData?.reasoning?.explanation || 
                  "Evidence-based clinical reasoning integrating model prediction with retrieved medical knowledge to provide contextualized diagnostic support."}
              </motion.div>
            </motion.div>
          </div>

          <div className="stage-metrics">
            <div className="metric-card">
              <div className="metric-label">MODEL</div>
              <div className="metric-value">GEMINI</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">SOURCES</div>
              <div className="metric-value">{evidenceCount}</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">TYPE</div>
              <div className="metric-value">GROUNDED</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">STATUS</div>
              <div className="metric-value status-ready">SYNTHESIZED</div>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
