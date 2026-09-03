/**
 * LANDING INFO SECTIONS
 * Premium immersive AI research product experience
 */

import { motion, useInView } from "framer-motion";
import { useRef, useState, useEffect } from "react";
import {
  Brain,
  Shield,
  Zap,
  Cpu,
  Activity,
  Database,
  Sparkles,
  FileText,
  Play,
  ArrowRight,
  CheckCircle2,
  Atom,
  Layers,
  TrendingUp,
  Upload,
  Eye,
  Boxes,
  Target,
} from "lucide-react";

/**
 * SECTION 1: System Architecture Visualization
 */
export function AboutSection() {
  const [hoveredNode, setHoveredNode] = useState(null);

  const systemNodes = [
    {
      id: "input",
      icon: <FileText size={28} />,
      label: "Chest X-Ray",
      description: "Medical image input",
      x: 50,
      y: 10,
    },
    {
      id: "cv",
      icon: <Brain size={28} />,
      label: "Computer Vision",
      description: "ResNet50 deep feature extraction",
      x: 50,
      y: 30,
    },
    {
      id: "pca",
      icon: <Layers size={28} />,
      label: "PCA Reduction",
      description: "2048D → 4D compression",
      x: 50,
      y: 50,
    },
    {
      id: "classical",
      icon: <Cpu size={28} />,
      label: "Classical SVM",
      description: "Primary stable classifier",
      x: 30,
      y: 70,
      primary: true,
    },
    {
      id: "quantum",
      icon: <Atom size={28} />,
      label: "Quantum ML",
      description: "Experimental research layer",
      x: 70,
      y: 70,
      quantum: true,
    },
    {
      id: "intelligence",
      icon: <Database size={28} />,
      label: "Intelligence",
      description: "RAG evidence retrieval",
      x: 50,
      y: 90,
    },
  ];

  const connections = [
    { from: "input", to: "cv" },
    { from: "cv", to: "pca" },
    { from: "pca", to: "classical" },
    { from: "pca", to: "quantum" },
    { from: "classical", to: "intelligence" },
    { from: "quantum", to: "intelligence" },
  ];

  return (
    <section className="landing-section about-section">
      <div className="orb orb-1"></div>
      <div className="orb orb-2"></div>
      <div className="orb orb-3"></div>
      <div className="section-container">
        <motion.div
          className="section-header"
          initial={{ opacity: 0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-100px" }}
          transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
        >
          <div className="section-eyebrow">
            <span className="eyebrow-line" />
            SYSTEM ARCHITECTURE
          </div>
          <h2 className="hero-style-heading">
            Medical intelligence,
            <br />
            <span>structured</span> for
            <br />
            <strong>decision support.</strong>
          </h2>
          <motion.p 
            className="section-lead"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            Q-MedTriage combines computer vision, dimensionality reduction, classical and quantum
            machine learning into one continuous AI-assisted triage pipeline.
          </motion.p>
        </motion.div>

        <div className="system-visualization">
          <svg className="system-connections" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid meet">
            {connections.map((conn, i) => {
              const fromNode = systemNodes.find(n => n.id === conn.from);
              const toNode = systemNodes.find(n => n.id === conn.to);
              return (
                <motion.line
                  key={i}
                  x1={fromNode.x}
                  y1={fromNode.y}
                  x2={toNode.x}
                  y2={toNode.y}
                  stroke={toNode.quantum ? "rgba(183, 148, 246, 0.3)" : "rgba(0, 255, 255, 0.3)"}
                  strokeWidth="0.2"
                  strokeDasharray="2 2"
                  initial={{ pathLength: 0, opacity: 0 }}
                  whileInView={{ pathLength: 1, opacity: 1 }}
                  viewport={{ once: true }}
                  transition={{ duration: 1, delay: i * 0.1 }}
                />
              );
            })}
          </svg>

          {systemNodes.map((node, i) => (
            <motion.div
              key={node.id}
              className={`system-node ${node.primary ? 'primary' : ''} ${node.quantum ? 'quantum' : ''}`}
              style={{ left: `${node.x}%`, top: `${node.y}%` }}
              initial={{ opacity: 0, scale: 0.8 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: i * 0.1 }}
              onMouseEnter={() => setHoveredNode(node.id)}
              onMouseLeave={() => setHoveredNode(null)}
            >
              <div className="node-icon">{node.icon}</div>
              <div className="node-label">{node.label}</div>
              {hoveredNode === node.id && (
                <motion.div
                  className="node-tooltip"
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0 }}
                >
                  {node.description}
                </motion.div>
              )}
            </motion.div>
          ))}
        </div>

        <motion.div
          className="research-notice"
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.8 }}
        >
          <Shield size={20} />
          <div>
            <strong>Research Prototype</strong>
            <span>
              Classical SVM remains the primary stable prediction pipeline.
              Quantum machine learning is an experimental research component exploring
              alternative kernel-based classification methods.
            </span>
          </div>
        </motion.div>
      </div>
    </section>
  );
}

/**
 * SECTION 2: Immersive Process Journey
 */
export function WorkflowSection() {
  const [activeStep, setActiveStep] = useState(0);
  const sectionRef = useRef(null);

  const steps = [
    {
      number: "01",
      icon: <Upload />,
      title: "Upload Chest X-Ray",
      description: "Single image or batch of up to 50 radiographs",
      visual: "upload",
    },
    {
      number: "02",
      icon: <Shield />,
      title: "Safety & Validation",
      description: "CLIP-based validation ensures only chest X-rays proceed",
      visual: "shield",
    },
    {
      number: "03",
      icon: <Brain />,
      title: "Visual Feature Extraction",
      description: "ResNet50 CNN extracts 2048-dimensional visual features",
      visual: "features",
    },
    {
      number: "04",
      icon: <Layers />,
      title: "PCA Feature Compression",
      description: "Dimensionality reduced to optimal 4D representation",
      visual: "compress",
    },
    {
      number: "05",
      icon: <Cpu />,
      title: "Classification",
      description: "Primary SVM classifier generates prediction",
      visual: "classify",
    },
    {
      number: "06",
      icon: <Database />,
      title: "Intelligence & Evidence",
      description: "RAG retrieves relevant medical knowledge",
      visual: "evidence",
    },
    {
      number: "07",
      icon: <CheckCircle2 />,
      title: "Decision Support",
      description: "Comprehensive analysis ready for review",
      visual: "result",
    },
  ];

  useEffect(() => {
    if (!sectionRef.current) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const scrollProgress = entry.intersectionRatio;
            const stepIndex = Math.min(
              Math.floor(scrollProgress * steps.length),
              steps.length - 1
            );
            setActiveStep(stepIndex);
          }
        });
      },
      { threshold: Array.from({ length: 100 }, (_, i) => i / 100) }
    );

    observer.observe(sectionRef.current);
    return () => observer.disconnect();
  }, [steps.length]);

  return (
    <section className="landing-section workflow-section" ref={sectionRef}>
      <div className="section-container">
        <motion.div
          className="section-header"
          initial={{ opacity: 0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-100px" }}
          transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
        >
          <div className="section-eyebrow">
            <span className="eyebrow-line" />
            THE PIPELINE
          </div>
          <h2 className="hero-style-heading">
            What happens
            <br />
            after <span>Start</span>
            <br />
            <strong>Triage?</strong>
          </h2>
        </motion.div>

        <div className="workflow-journey">
          <div className="journey-steps">
            {steps.map((step, index) => (
              <div
                key={step.number}
                className={`journey-step-indicator ${index <= activeStep ? 'active' : ''}`}
                onClick={() => setActiveStep(index)}
              >
                {step.number}
              </div>
            ))}
          </div>

          <div className="journey-content">
            {steps.map((step, index) => (
              <motion.div
                key={step.number}
                className={`journey-panel ${index === activeStep ? 'active' : ''}`}
                initial={{ opacity: 0, x: 50 }}
                animate={{
                  opacity: index === activeStep ? 1 : 0,
                  x: index === activeStep ? 0 : 50,
                }}
                transition={{ duration: 0.5 }}
              >
                <div className="panel-visual">
                  <StepVisual type={step.visual} />
                </div>
                <div className="panel-text">
                  <div className="panel-icon">{step.icon}</div>
                  <h3>{step.title}</h3>
                  <p>{step.description}</p>
                  <div className="panel-number">{step.number}</div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

function StepVisual({ type }) {
  return (
    <div className={`step-visual ${type}`}>
      {type === 'upload' && <DataFlowAnimation dots={12} />}
      {type === 'shield' && <ShieldAnimation />}
      {type === 'features' && <FeatureGridAnimation />}
      {type === 'compress' && <CompressionAnimation />}
      {type === 'classify' && <BoundaryAnimation />}
      {type === 'evidence' && <NetworkAnimation />}
      {type === 'result' && <PulseAnimation />}
    </div>
  );
}

function DataFlowAnimation({ dots }) {
  return (
    <div className="data-flow">
      {Array.from({ length: dots }).map((_, i) => (
        <motion.div
          key={i}
          className="flow-dot"
          initial={{ y: -20, opacity: 0 }}
          animate={{ y: 100, opacity: [0, 1, 0] }}
          transition={{
            duration: 2,
            repeat: Infinity,
            delay: i * 0.15,
          }}
        />
      ))}
    </div>
  );
}

function ShieldAnimation() {
  return (
    <motion.div
      className="shield-ring"
      animate={{ rotate: 360 }}
      transition={{ duration: 8, repeat: Infinity, ease: "linear" }}
    >
      <Shield size={48} />
    </motion.div>
  );
}

function FeatureGridAnimation() {
  return (
    <div className="feature-grid">
      {Array.from({ length: 16 }).map((_, i) => (
        <motion.div
          key={i}
          className="grid-cell"
          animate={{ opacity: [0.2, 1, 0.2] }}
          transition={{
            duration: 2,
            repeat: Infinity,
            delay: i * 0.1,
          }}
        />
      ))}
    </div>
  );
}

function CompressionAnimation() {
  return (
    <div className="compression-viz">
      <motion.div className="compress-from" initial={{ width: 200 }} animate={{ width: 50 }} transition={{ duration: 2, repeat: Infinity, repeatType: "reverse" }}>
        <span>2048D</span>
      </motion.div>
      <ArrowRight className="compress-arrow" />
      <motion.div className="compress-to" initial={{ width: 50 }} animate={{ width: 50 }}>
        <span>4D</span>
      </motion.div>
    </div>
  );
}

function BoundaryAnimation() {
  return (
    <svg className="boundary-viz" viewBox="0 0 100 100">
      <motion.line
        x1="10"
        y1="90"
        x2="90"
        y2="10"
        stroke="#00ffff"
        strokeWidth="2"
        initial={{ pathLength: 0 }}
        animate={{ pathLength: 1 }}
        transition={{ duration: 2, repeat: Infinity, repeatType: "reverse" }}
      />
      <circle cx="30" cy="70" r="4" fill="#00ffff" opacity="0.6" />
      <circle cx="25" cy="75" r="4" fill="#00ffff" opacity="0.6" />
      <circle cx="70" cy="30" r="4" fill="#b794f6" opacity="0.6" />
      <circle cx="75" cy="25" r="4" fill="#b794f6" opacity="0.6" />
    </svg>
  );
}

function NetworkAnimation() {
  return (
    <div className="network-viz">
      {Array.from({ length: 6 }).map((_, i) => (
        <motion.div
          key={i}
          className="network-node"
          style={{
            left: `${20 + (i % 3) * 30}%`,
            top: `${30 + Math.floor(i / 3) * 40}%`,
          }}
          animate={{ scale: [1, 1.2, 1] }}
          transition={{
            duration: 2,
            repeat: Infinity,
            delay: i * 0.2,
          }}
        />
      ))}
    </div>
  );
}

function PulseAnimation() {
  return (
    <motion.div
      className="pulse-circle"
      animate={{ scale: [1, 1.5, 1], opacity: [1, 0.3, 1] }}
      transition={{ duration: 2, repeat: Infinity }}
    >
      <CheckCircle2 size={48} />
    </motion.div>
  );
}

/**
 * SECTION 3: Feature Transformation Visualization
 */
export function PipelineArchitectureSection() {
  return (
    <section className="landing-section architecture-section">
      <div className="section-container">
        <motion.div
          className="section-header"
          initial={{ opacity: 0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-100px" }}
          transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
        >
          <div className="section-eyebrow">
            <span className="eyebrow-line" />
            FEATURE TRANSFORMATION
          </div>
          <h2 className="hero-style-heading">
            From image
            <br />
            to <span>decision</span>
            <br />
            <strong>boundary.</strong>
          </h2>
          <motion.p 
            className="section-lead"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            Conceptual visualization of feature-space transformation
          </motion.p>
        </motion.div>

        <div className="feature-transformation">
          <div className="transform-stage">
            <FileText size={48} />
            <h4>Chest X-Ray Image</h4>
            <div className="visual-placeholder image-viz">
              <div className="pixel-grid">
                {Array.from({ length: 64 }).map((_, i) => (
                  <motion.div
                    key={i}
                    className="pixel"
                    animate={{ opacity: [0.3, 0.8, 0.3] }}
                    transition={{
                      duration: 2,
                      repeat: Infinity,
                      delay: i * 0.02,
                    }}
                  />
                ))}
              </div>
            </div>
          </div>

          <motion.div
            className="transform-arrow"
            animate={{ x: [0, 10, 0] }}
            transition={{ duration: 2, repeat: Infinity }}
          >
            <ArrowRight size={32} />
            <span>ResNet50</span>
          </motion.div>

          <div className="transform-stage">
            <Brain size={48} />
            <h4>2048-D Feature Space</h4>
            <div className="visual-placeholder feature-space-viz">
              {Array.from({ length: 100 }).map((_, i) => (
                <motion.div
                  key={i}
                  className="feature-dot"
                  style={{
                    left: `${Math.random() * 100}%`,
                    top: `${Math.random() * 100}%`,
                  }}
                  animate={{
                    scale: [0.5, 1.5, 0.5],
                    opacity: [0.3, 1, 0.3],
                  }}
                  transition={{
                    duration: 3,
                    repeat: Infinity,
                    delay: i * 0.03,
                  }}
                />
              ))}
            </div>
          </div>

          <motion.div
            className="transform-arrow compress"
            animate={{ scale: [1, 0.9, 1] }}
            transition={{ duration: 2, repeat: Infinity }}
          >
            <Layers size={32} />
            <span>PCA</span>
          </motion.div>

          <div className="transform-stage">
            <Target size={48} />
            <h4>4-D PCA Representation</h4>
            <div className="visual-placeholder pca-viz">
              <motion.div
                className="dimension-reduction"
                animate={{ width: ["100%", "30%", "100%"] }}
                transition={{ duration: 4, repeat: Infinity }}
              >
                <span>Dimensionality Compression</span>
              </motion.div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

/**
 * SECTION 4: Immersive Quantum ML Visualization
 */
export function QuantumExplanationSection() {
  return (
    <section className="landing-section quantum-section">
      <div className="quantum-immersive">
        <div className="quantum-background">
          {Array.from({ length: 20 }).map((_, i) => (
            <motion.div
              key={i}
              className="quantum-particle"
              style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
              }}
              animate={{
                y: [0, -30, 0],
                opacity: [0.2, 0.8, 0.2],
                scale: [1, 1.5, 1],
              }}
              transition={{
                duration: 4 + Math.random() * 2,
                repeat: Infinity,
                delay: i * 0.2,
              }}
            />
          ))}
        </div>

        <div className="section-container">
          <motion.div
            className="quantum-content"
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
          >
            <div className="quantum-text">
              <div className="section-eyebrow quantum-eyebrow">
                <span className="eyebrow-line" />
                EXPERIMENTAL RESEARCH LAYER
              </div>
              <h2 className="hero-style-heading">
                Why explore
                <br />
                <span>Quantum</span> Machine
                <br />
                <strong>Learning?</strong>
              </h2>
              <motion.p
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6, delay: 0.2 }}
              >
                The medical image is first processed using conventional AI—ResNet extracts visual
                features, and PCA reduces the high-dimensional representation. The reduced features
                can then be encoded into a quantum feature space.
              </motion.p>
              <motion.p
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6, delay: 0.3 }}
              >
                A quantum kernel measures similarity between feature representations. This is a
                research exploration to understand alternative kernel representations, not a claim
                of quantum advantage or production readiness.
              </motion.p>

              <motion.div 
                className="quantum-disclaimer"
                initial={{ opacity: 0, x: -20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6, delay: 0.4 }}
              >
                <Atom size={18} />
                <span>Experimental research layer—evaluated alongside primary classical pipeline</span>
              </motion.div>
            </div>

            <div className="quantum-pipeline-viz">
              <motion.div className="quantum-stage" whileHover={{ scale: 1.05 }}>
                <div className="stage-label">CLASSICAL FEATURE SPACE</div>
                <Layers size={32} />
                <span>4-D PCA Features</span>
              </motion.div>

              <div className="quantum-flow-arrow">↓</div>

              <motion.div className="quantum-stage highlight" whileHover={{ scale: 1.05 }}>
                <div className="stage-label">QUANTUM ENCODING</div>
                <Zap size={32} />
                <span>Feature Encoding</span>
              </motion.div>

              <div className="quantum-flow-arrow">↓</div>

              <motion.div className="quantum-stage highlight" whileHover={{ scale: 1.05 }}>
                <div className="stage-label">QUANTUM STATE</div>
                <Atom size={32} />
                <span>Quantum Feature Map</span>
                <div className="orbital-viz">
                  <motion.div
                    className="orbital"
                    animate={{ rotate: 360 }}
                    transition={{ duration: 8, repeat: Infinity, ease: "linear" }}
                  />
                  <motion.div
                    className="orbital"
                    style={{ transform: "rotate(60deg)" }}
                    animate={{ rotate: 420 }}
                    transition={{ duration: 8, repeat: Infinity, ease: "linear" }}
                  />
                  <motion.div
                    className="orbital"
                    style={{ transform: "rotate(120deg)" }}
                    animate={{ rotate: 480 }}
                    transition={{ duration: 8, repeat: Infinity, ease: "linear" }}
                  />
                </div>
              </motion.div>

              <div className="quantum-flow-arrow">↓</div>

              <motion.div className="quantum-stage" whileHover={{ scale: 1.05 }}>
                <div className="stage-label">SIMILARITY</div>
                <Activity size={32} />
                <span>Quantum Kernel</span>
              </motion.div>

              <div className="quantum-flow-arrow">↓</div>

              <motion.div className="quantum-stage result" whileHover={{ scale: 1.05 }}>
                <div className="stage-label">EXPERIMENT</div>
                <Sparkles size={32} />
                <span>QSVM Research</span>
              </motion.div>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}

/**
 * SECTION 5: Interactive Split-Screen Comparison
 */
export function ComparisonSection() {
  const [hoveredSide, setHoveredSide] = useState(null);

  return (
    <section className="landing-section comparison-section">
      <div className="section-container">
        <motion.div
          className="section-header"
          initial={{ opacity: 0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-100px" }}
          transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
        >
          <div className="section-eyebrow">
            <span className="eyebrow-line" />
            DUAL APPROACH
          </div>
          <h2 className="hero-style-heading">
            Classical
            <br />
            <span>vs</span>
            <br />
            <strong>Quantum.</strong>
          </h2>
        </motion.div>

        <div className="split-comparison">
          <motion.div
            className={`comparison-side classical ${hoveredSide === 'classical' ? 'expanded' : ''} ${hoveredSide === 'quantum' ? 'compressed' : ''}`}
            onMouseEnter={() => setHoveredSide('classical')}
            onMouseLeave={() => setHoveredSide(null)}
            initial={{ opacity: 0, x: -50 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <div className="side-content">
              <div className="side-status primary">
                <CheckCircle2 size={16} />
                PRIMARY / STABLE
              </div>
              <div className="side-icon">
                <Cpu size={64} />
              </div>
              <h3>Classical AI</h3>
              <p className="side-description">Primary prediction pipeline</p>

              <div className="side-visual">
                <svg viewBox="0 0 100 100" className="feature-space">
                  <motion.line
                    x1="10"
                    y1="90"
                    x2="90"
                    y2="10"
                    stroke="#00ffff"
                    strokeWidth="2"
                    initial={{ pathLength: 0 }}
                    animate={{ pathLength: 1 }}
                    transition={{ duration: 2, repeat: Infinity, repeatType: "reverse" }}
                  />
                  <text x="50" y="15" fill="#00ffff" fontSize="8" textAnchor="middle">
                    SVM Boundary
                  </text>
                  {Array.from({ length: 8 }).map((_, i) => (
                    <circle
                      key={i}
                      cx={20 + Math.random() * 30}
                      cy={60 + Math.random() * 30}
                      r="3"
                      fill="#00ffff"
                      opacity="0.6"
                    />
                  ))}
                  {Array.from({ length: 8 }).map((_, i) => (
                    <circle
                      key={i}
                      cx={60 + Math.random() * 30}
                      cy={15 + Math.random() * 30}
                      r="3"
                      fill="#00ffff"
                      opacity="0.3"
                    />
                  ))}
                </svg>
              </div>

              <div className="side-features">
                <div className="feature-item">
                  <CheckCircle2 size={14} />
                  <span>ResNet50 features</span>
                </div>
                <div className="feature-item">
                  <CheckCircle2 size={14} />
                  <span>PCA reduction</span>
                </div>
                <div className="feature-item">
                  <CheckCircle2 size={14} />
                  <span>Classical SVM</span>
                </div>
                <div className="feature-item">
                  <CheckCircle2 size={14} />
                  <span>Current operational classifier</span>
                </div>
              </div>
            </div>
          </motion.div>

          <div className="comparison-divider">
            <div className="divider-line" />
            <div className="divider-label">VS</div>
          </div>

          <motion.div
            className={`comparison-side quantum ${hoveredSide === 'quantum' ? 'expanded' : ''} ${hoveredSide === 'classical' ? 'compressed' : ''}`}
            onMouseEnter={() => setHoveredSide('quantum')}
            onMouseLeave={() => setHoveredSide(null)}
            initial={{ opacity: 0, x: 50 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <div className="side-content">
              <div className="side-status experimental">
                <Atom size={16} />
                EXPERIMENTAL
              </div>
              <div className="side-icon">
                <Atom size={64} />
              </div>
              <h3>Quantum ML</h3>
              <p className="side-description">Experimental research layer</p>

              <div className="side-visual quantum-visual">
                <motion.div
                  className="quantum-orbit orbit-1"
                  animate={{ rotate: 360 }}
                  transition={{ duration: 10, repeat: Infinity, ease: "linear" }}
                />
                <motion.div
                  className="quantum-orbit orbit-2"
                  animate={{ rotate: -360 }}
                  transition={{ duration: 15, repeat: Infinity, ease: "linear" }}
                />
                <motion.div
                  className="quantum-orbit orbit-3"
                  animate={{ rotate: 360 }}
                  transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
                />
                <div className="quantum-core">
                  <Atom size={32} />
                </div>
              </div>

              <div className="side-features">
                <div className="feature-item">
                  <Atom size={14} />
                  <span>PCA feature encoding</span>
                </div>
                <div className="feature-item">
                  <Atom size={14} />
                  <span>Quantum feature maps</span>
                </div>
                <div className="feature-item">
                  <Atom size={14} />
                  <span>Quantum kernel evaluation</span>
                </div>
                <div className="feature-item">
                  <Atom size={14} />
                  <span>Research comparison vs classical</span>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}

/**
 * SECTION 6: Network Intelligence Visualization
 */
export function IntelligenceSection() {
  const nodes = [
    { id: 'output', label: 'Model Output', x: 50, y: 20 },
    { id: 'kb1', label: 'Medical KB', x: 20, y: 45 },
    { id: 'kb2', label: 'Evidence', x: 80, y: 45 },
    { id: 'kb3', label: 'Context', x: 35, y: 60 },
    { id: 'kb4', label: 'Research', x: 65, y: 60 },
    { id: 'synthesis', label: 'Decision Support', x: 50, y: 85 },
  ];

  const connections = [
    { from: 'output', to: 'kb1' },
    { from: 'output', to: 'kb2' },
    { from: 'output', to: 'kb3' },
    { from: 'output', to: 'kb4' },
    { from: 'kb1', to: 'synthesis' },
    { from: 'kb2', to: 'synthesis' },
    { from: 'kb3', to: 'synthesis' },
    { from: 'kb4', to: 'synthesis' },
  ];

  return (
    <section className="landing-section intelligence-section">
      <div className="section-container">
        <motion.div
          className="section-header"
          initial={{ opacity: 0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-100px" }}
          transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
        >
          <div className="section-eyebrow">
            <span className="eyebrow-line" />
            CONTEXTUAL INTELLIGENCE
          </div>
          <h2 className="hero-style-heading">
            Intelligence
            <br />
            <span>&</span> Evidence
            <br />
            <strong>Layer.</strong>
          </h2>
          <motion.p 
            className="section-lead"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            RAG retrieves medical knowledge to contextualize predictions with evidence-grounded explanations
          </motion.p>
        </motion.div>

        <div className="intelligence-network">
          <svg className="network-connections" viewBox="0 0 100 100">
            {connections.map((conn, i) => {
              const fromNode = nodes.find(n => n.id === conn.from);
              const toNode = nodes.find(n => n.id === conn.to);
              return (
                <motion.line
                  key={i}
                  x1={fromNode.x}
                  y1={fromNode.y}
                  x2={toNode.x}
                  y2={toNode.y}
                  stroke="rgba(0, 255, 255, 0.3)"
                  strokeWidth="0.3"
                  initial={{ pathLength: 0, opacity: 0 }}
                  whileInView={{ pathLength: 1, opacity: 1 }}
                  viewport={{ once: true }}
                  transition={{ duration: 1.5, delay: i * 0.1 }}
                />
              );
            })}
          </svg>

          {nodes.map((node, i) => (
            <motion.div
              key={node.id}
              className={`network-node ${node.id === 'output' ? 'source' : ''} ${node.id === 'synthesis' ? 'result' : ''}`}
              style={{ left: `${node.x}%`, top: `${node.y}%` }}
              initial={{ opacity: 0, scale: 0 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: i * 0.1 }}
            >
              <motion.div
                className="node-pulse"
                animate={{
                  scale: [1, 1.5, 1],
                  opacity: [0.5, 0, 0.5],
                }}
                transition={{
                  duration: 2,
                  repeat: Infinity,
                  delay: i * 0.3,
                }}
              />
              <div className="node-core">
                {node.id === 'output' && <Activity size={20} />}
                {node.id.startsWith('kb') && <Database size={16} />}
                {node.id === 'synthesis' && <Sparkles size={20} />}
              </div>
              <span className="node-label">{node.label}</span>
            </motion.div>
          ))}
        </div>

        <motion.div
          className="intelligence-note"
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 1 }}
        >
          <Shield size={20} />
          <div>
            <strong>Research Prototype</strong>
            <span>
              Decision support and contextual evidence for research purposes.
              Not intended for clinical diagnosis.
            </span>
          </div>
        </motion.div>
      </div>
    </section>
  );
}

/**
 * SECTION 7: Cinematic Final CTA
 */
export function CTASection({ onStartTriage }) {
  return (
    <section className="landing-section cta-section">
      <div className="cta-background">
        <div className="cta-grid">
          {Array.from({ length: 100 }).map((_, i) => (
            <motion.div
              key={i}
              className="grid-line"
              animate={{
                opacity: [0.1, 0.3, 0.1],
              }}
              transition={{
                duration: 3,
                repeat: Infinity,
                delay: i * 0.02,
              }}
            />
          ))}
        </div>
        <motion.div
          className="scan-line"
          animate={{ y: ["0%", "100%"] }}
          transition={{ duration: 3, repeat: Infinity, ease: "linear" }}
        />
      </div>

      <div className="section-container">
        <motion.div
          className="cta-content"
          initial={{ opacity: 0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
        >
          <motion.div
            className="cta-icon-circle"
            animate={{
              rotate: [0, 360],
              scale: [1, 1.05, 1],
            }}
            transition={{
              rotate: { duration: 20, repeat: Infinity, ease: "linear" },
              scale: { duration: 2, repeat: Infinity },
            }}
          >
            <Eye size={48} />
          </motion.div>

          <motion.h2 
            className="hero-style-heading cta-heading"
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
          >
            Ready to
            <br />
            <span>enter</span> the
            <br />
            <strong>system?</strong>
          </motion.h2>
          
          <div className="cta-pipeline-preview">
            <motion.div
              className="pipeline-stage"
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.2 }}
            >
              <FileText size={24} />
              <span>CHEST X-RAY</span>
            </motion.div>
            
            <ArrowRight className="pipeline-arrow" />
            
            <motion.div
              className="pipeline-stage"
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.4 }}
            >
              <Brain size={24} />
              <span>AI ANALYSIS</span>
            </motion.div>
            
            <ArrowRight className="pipeline-arrow" />
            
            <motion.div
              className="pipeline-stage"
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.6 }}
            >
              <Database size={24} />
              <span>EVIDENCE</span>
            </motion.div>
            
            <ArrowRight className="pipeline-arrow" />
            
            <motion.div
              className="pipeline-stage"
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.8 }}
            >
              <Sparkles size={24} />
              <span>INSIGHT</span>
            </motion.div>
          </div>

          <motion.button
            className="cta-button"
            onClick={onStartTriage}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <Play size={20} />
            <span>START TRIAGE</span>
            <ArrowRight size={20} />
          </motion.button>

          <p className="cta-subtitle">
            Enter the complete AI-assisted triage pipeline
          </p>
        </motion.div>
      </div>
    </section>
  );
}
