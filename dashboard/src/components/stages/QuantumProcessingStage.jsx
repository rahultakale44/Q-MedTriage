/**
 * QUANTUM PROCESSING STAGE
 */

import { motion } from "framer-motion";

const QUBITS = ["Q0", "Q1", "Q2", "Q3"];
const GATES = ["H", "RY", "RZ"];

export function QuantumProcessingStage() {
  return (
    <motion.div
      className="quantum-stage"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    >
      <div className="stage-container">
        <div className="stage-header">
          <div className="stage-number">04</div>
          <div className="stage-title-group">
            <h3 className="stage-label">QUANTUM CLASSIFICATION</h3>
            <h2 className="stage-title">Enter the quantum core</h2>
            <p className="stage-description">
              4-qubit quantum circuit processing features through superposition
            </p>
          </div>
        </div>

        <div className="stage-content">
          <div className="quantum-visualization">
            <div className="quantum-circuit">
              {QUBITS.map((qubit, qIdx) => (
                <div key={qubit} className="qubit-wire">
                  <div className="qubit-label">{qubit}</div>
                  <div className="wire-line" />
                  
                  <motion.div
                    className="qubit-state"
                    animate={{
                      boxShadow: [
                        "0 0 0px rgba(0,230,255,0)",
                        "0 0 20px rgba(0,230,255,0.8)",
                        "0 0 0px rgba(0,230,255,0)",
                      ],
                    }}
                    transition={{
                      duration: 1.5,
                      repeat: Infinity,
                      delay: qIdx * 0.2,
                    }}
                  >
                    |0⟩
                  </motion.div>

                  {GATES.map((gate, gIdx) => (
                    <motion.div
                      key={`${qubit}-${gate}`}
                      className="quantum-gate"
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      transition={{ delay: 0.5 + gIdx * 0.3, type: "spring" }}
                    >
                      {gate}
                    </motion.div>
                  ))}

                  {qIdx < 3 && (
                    <motion.div
                      className="entanglement-line"
                      initial={{ scaleY: 0 }}
                      animate={{ scaleY: 1 }}
                      transition={{ delay: 1.5 }}
                    />
                  )}

                  <motion.div
                    className="measurement"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 2 }}
                  >
                    M
                  </motion.div>
                </div>
              ))}
            </div>

            <div className="quantum-status">
              <motion.div
                className="status-item"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.3 }}
              >
                <div className="status-dot pulsing" />
                <span>CIRCUIT INITIALIZED</span>
              </motion.div>
              <motion.div
                className="status-item"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.8 }}
              >
                <div className="status-dot pulsing" />
                <span>ENCODING FEATURES</span>
              </motion.div>
              <motion.div
                className="status-item"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 1.3 }}
              >
                <div className="status-dot pulsing" />
                <span>MEASURING STATE</span>
              </motion.div>
            </div>
          </div>

          <div className="stage-metrics">
            <div className="metric-card">
              <div className="metric-label">QUBITS</div>
              <div className="metric-value">4</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">BACKEND</div>
              <div className="metric-value">QASM</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">SHOTS</div>
              <div className="metric-value">1024</div>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
