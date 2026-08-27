/**
 * QUANTUM PROCESSING STAGE - Stage 04
 * Professional quantum classification visualization
 */

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Zap } from "lucide-react";

const QUBITS = ["Q0", "Q1", "Q2", "Q3"];
const QUANTUM_GATES = ["H", "RY", "RZ", "CX"];

// Quantum processing substeps with timing
const QUANTUM_STEPS = [
  { id: "init", label: "CIRCUIT INITIALIZED", duration: 1500 },
  { id: "encode", label: "ENCODING FEATURES", duration: 2000 },
  { id: "gates", label: "APPLYING QUANTUM GATES", duration: 2000 },
  { id: "measure", label: "MEASURING STATE", duration: 1500 },
  { id: "complete", label: "CLASSIFICATION COMPLETE", duration: 1000 },
];

export function QuantumProcessingStage() {
  const [activeStep, setActiveStep] = useState(0);

  // Progress through quantum substeps
  useEffect(() => {
    if (activeStep >= QUANTUM_STEPS.length) return;

    const timer = setTimeout(() => {
      setActiveStep((prev) => prev + 1);
    }, QUANTUM_STEPS[activeStep].duration);

    return () => clearTimeout(timer);
  }, [activeStep]);

  const isComplete = activeStep >= QUANTUM_STEPS.length - 1;

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
            <h2 className="stage-title">Quantum circuit evaluation</h2>
            <p className="stage-description">
              4-qubit parametrized quantum circuit processing compressed features through superposition
            </p>
          </div>
        </div>

        <div className="stage-content">
          <div className="quantum-main-visualization">
            {/* Quantum Circuit Diagram */}
            <motion.div
              className="quantum-circuit-container"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.2 }}
            >
              <div className="circuit-header">
                <Zap size={20} className="quantum-icon" />
                <span>QUANTUM CIRCUIT</span>
              </div>
              
              <div className="quantum-circuit-diagram">
                {QUBITS.map((qubit, qIdx) => (
                  <div key={qubit} className="qubit-wire-line">
                    <div className="qubit-label-text">{qubit}</div>
                    <div className="wire-horizontal-line" />
                    
                    {/* Initial State */}
                    <motion.div
                      className="qubit-state-box"
                      animate={{
                        boxShadow: activeStep >= 1 ? [
                          "0 0 0px rgba(0,230,255,0)",
                          "0 0 15px rgba(0,230,255,0.6)",
                          "0 0 0px rgba(0,230,255,0)",
                        ] : "0 0 0px rgba(0,230,255,0)",
                      }}
                      transition={{
                        duration: 1.5,
                        repeat: activeStep >= 1 && activeStep < 4 ? Infinity : 0,
                        delay: qIdx * 0.15,
                      }}
                    >
                      |0⟩
                    </motion.div>

                    {/* Quantum Gates */}
                    <div className="gates-container">
                      {QUANTUM_GATES.slice(0, 3).map((gate, gIdx) => (
                        <motion.div
                          key={`${qubit}-${gate}-${gIdx}`}
                          className="quantum-gate-box"
                          initial={{ scale: 0, opacity: 0 }}
                          animate={{ 
                            scale: activeStep >= 2 ? 1 : 0,
                            opacity: activeStep >= 2 ? 1 : 0,
                          }}
                          transition={{ delay: 0.2 + gIdx * 0.15 + qIdx * 0.1, type: "spring", stiffness: 200 }}
                        >
                          {gate}
                        </motion.div>
                      ))}
                    </div>

                    {/* Measurement */}
                    <motion.div
                      className="measurement-box"
                      initial={{ opacity: 0, scale: 0 }}
                      animate={{ 
                        opacity: activeStep >= 3 ? 1 : 0,
                        scale: activeStep >= 3 ? 1 : 0,
                      }}
                      transition={{ delay: qIdx * 0.1, type: "spring" }}
                    >
                      M
                    </motion.div>
                  </div>
                ))}
              </div>
            </motion.div>

            {/* Processing Status */}
            <motion.div
              className="quantum-status-panel"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.4 }}
            >
              <div className="status-panel-header">EXECUTION STATUS</div>
              <div className="quantum-status-list">
                {QUANTUM_STEPS.slice(0, activeStep + 1).map((step, index) => (
                  <motion.div
                    key={step.id}
                    className="quantum-status-item"
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.15 }}
                  >
                    <div className={`status-indicator-dot ${index === activeStep && !isComplete ? '' : 'complete'}`} />
                    <span className="status-text">{step.label}</span>
                  </motion.div>
                ))}
              </div>
            </motion.div>
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
            <div className="metric-card">
              <div className="metric-label">STATUS</div>
              <div className={`metric-value ${isComplete ? 'status-ready' : 'status-active'}`}>
                {isComplete ? 'COMPLETE' : 'PROCESSING'}
              </div>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
