/**
 * QUANTUM PROCESSING STAGE
 */

import { useState, useEffect } from "react";
import { motion } from "framer-motion";

const QUBITS = ["Q0", "Q1", "Q2", "Q3"];
const GATES = ["H", "RY", "RZ"];

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
                      boxShadow: activeStep >= 1 ? [
                        "0 0 0px rgba(0,230,255,0)",
                        "0 0 20px rgba(0,230,255,0.8)",
                        "0 0 0px rgba(0,230,255,0)",
                      ] : "0 0 0px rgba(0,230,255,0)",
                    }}
                    transition={{
                      duration: 1.5,
                      repeat: activeStep >= 1 && activeStep < 4 ? Infinity : 0,
                      delay: qIdx * 0.2,
                    }}
                  >
                    |0⟩
                  </motion.div>

                  {GATES.map((gate, gIdx) => (
                    <motion.div
                      key={`${qubit}-${gate}`}
                      className="quantum-gate"
                      initial={{ scale: 0, opacity: 0 }}
                      animate={{ 
                        scale: activeStep >= 2 ? 1 : 0,
                        opacity: activeStep >= 2 ? 1 : 0,
                      }}
                      transition={{ delay: 0.2 + gIdx * 0.2 + qIdx * 0.1, type: "spring" }}
                    >
                      {gate}
                    </motion.div>
                  ))}

                  {qIdx < 3 && (
                    <motion.div
                      className="entanglement-line"
                      initial={{ scaleY: 0, opacity: 0 }}
                      animate={{ 
                        scaleY: activeStep >= 2 ? 1 : 0,
                        opacity: activeStep >= 2 ? 1 : 0,
                      }}
                      transition={{ delay: 1 + qIdx * 0.2 }}
                    />
                  )}

                  <motion.div
                    className="measurement"
                    initial={{ opacity: 0, scale: 0 }}
                    animate={{ 
                      opacity: activeStep >= 3 ? 1 : 0,
                      scale: activeStep >= 3 ? 1 : 0,
                    }}
                    transition={{ delay: qIdx * 0.15, type: "spring" }}
                  >
                    M
                  </motion.div>
                </div>
              ))}
            </div>

            <div className="quantum-status">
              {QUANTUM_STEPS.slice(0, activeStep + 1).map((step, index) => (
                <motion.div
                  key={step.id}
                  className="status-item"
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.2 }}
                >
                  <div className={`status-dot ${index === activeStep ? 'pulsing' : 'complete'}`} />
                  <span>{step.label}</span>
                </motion.div>
              ))}
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
