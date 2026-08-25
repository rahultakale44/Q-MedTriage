import { useEffect, useMemo, useRef, useState } from "react";
import {
  Activity,
  ArrowDown,
  BrainCircuit,
  CheckCircle2,
  ChevronRight,
  Cpu,
  Database,
  FileSearch,
  Image as ImageIcon,
  Layers3,
  Microscope,
  Play,
  ScanLine,
  Sparkles,
  Upload,
  Waves,
} from "lucide-react";
import { motion, useScroll, useSpring, useTransform } from "framer-motion";
import { DEMO_ANALYSIS } from "./data/demoData";
import "./App.css";

const stages = [
  {
    id: "input",
    label: "INPUT",
    title: "The image enters.",
    description:
      "A chest X-ray becomes the first signal in the Q-MedTriage intelligence pipeline. " +
      "The raw medical image is uploaded and prepared for analysis.",
    icon: Upload,
  },
  {
    id: "preprocess",
    label: "PREPROCESS",
    title: "Clean the signal.",
    description:
      "The raw image is transformed into a standardized format. Resizing, normalization, " +
      "and noise reduction prepare the image for deep learning feature extraction.",
    icon: ScanLine,
  },
  {
    id: "cnn",
    label: "VISION",
    title: "See the patterns.",
    description:
      "A pre-trained convolutional neural network extracts clinically relevant visual features. " +
      "The network identifies patterns learned from thousands of medical images.",
    icon: BrainCircuit,
  },
  {
    id: "pca",
    label: "REDUCTION",
    title: "Compress intelligence.",
    description:
      "High-dimensional CNN features are projected into a compact representation using PCA. " +
      "This compression retains essential information while reducing dimensionality for quantum processing.",
    icon: Layers3,
  },
  {
    id: "quantum",
    label: "QUANTUM",
    title: "Enter the quantum core.",
    description:
      "The compact feature representation is encoded into a quantum circuit. " +
      "Quantum gates process the data through superposition and entanglement for classification.",
    icon: Waves,
  },
  {
    id: "evidence",
    label: "EVIDENCE",
    title: "Bring the evidence.",
    description:
      "Relevant medical knowledge is retrieved from a vector database using semantic search. " +
      "Evidence grounds the model's prediction in established clinical understanding.",
    icon: FileSearch,
  },
  {
    id: "reason",
    label: "REASONING",
    title: "Connect the dots.",
    description:
      "A large language model synthesizes the model prediction with retrieved evidence. " +
      "The raw classification becomes an interpretable, grounded explanation.",
    icon: Sparkles,
  },
  {
    id: "triage",
    label: "TRIAGE",
    title: "Actionable intelligence.",
    description:
      "The final system output combines model confidence, evidence sources, and priority assessment. " +
      "This AI-assisted triage supports clinical decision-making, not replacement.",
    icon: Activity,
  },
];

function App() {
  const [activeStage, setActiveStage] = useState(0);
  const [autoRun, setAutoRun] = useState(false);
  const [image, setImage] = useState(null);
  const [analysisStarted, setAnalysisStarted] = useState(false);

  const fileInputRef = useRef(null);

  const { scrollYProgress } = useScroll();

  const smoothProgress = useSpring(scrollYProgress, {
    stiffness: 90,
    damping: 24,
    mass: 0.35,
  });

  const progressWidth = useTransform(
    smoothProgress,
    [0, 1],
    ["0%", "100%"]
  );

  /* ---------------------------------------------------------
     UPDATE ACTIVE PIPELINE STAGE WHILE SCROLLING
  --------------------------------------------------------- */

  useEffect(() => {
    const handleScroll = () => {
      const max =
        document.documentElement.scrollHeight - window.innerHeight;

      if (max <= 0) return;

      const percentage = window.scrollY / max;

      const index = Math.min(
        stages.length - 1,
        Math.max(0, Math.floor(percentage * stages.length))
      );

      setActiveStage(index);
    };

    window.addEventListener("scroll", handleScroll, {
      passive: true,
    });

    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, []);

  /* ---------------------------------------------------------
     AUTO RUN
  --------------------------------------------------------- */

  useEffect(() => {
    if (!autoRun) return;

    const timer = setInterval(() => {
      setActiveStage((current) => {
        const next = current + 1;

        if (next >= stages.length) {
          setAutoRun(false);
          return current;
        }

        const target = document.getElementById(
          `scene-${next}`
        );

        target?.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });

        return next;
      });
    }, 3200);

    return () => clearInterval(timer);
  }, [autoRun]);

  /* ---------------------------------------------------------
     START TRIAGE
  --------------------------------------------------------- */

  const startExperience = () => {
    setAnalysisStarted(true);
    setAutoRun(true);

    setTimeout(() => {
      document
        .getElementById("scene-0")
        ?.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
    }, 100);
  };

  /* ---------------------------------------------------------
     IMAGE UPLOAD
  --------------------------------------------------------- */

  const handleUpload = (event) => {
    const file = event.target.files?.[0];

    if (!file) return;

    const url = URL.createObjectURL(file);

    setImage(url);
    setAnalysisStarted(true);

    setTimeout(() => {
      document
        .getElementById("scene-1")
        ?.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });

      setAutoRun(true);
    }, 500);
  };

  /* ---------------------------------------------------------
     NAVIGATION
  --------------------------------------------------------- */

  const jumpTo = (index) => {
    document
      .getElementById(`scene-${index}`)
      ?.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
  };

  return (
    <div className="qmed-app">
      <div className="noise" />

      {/* =====================================================
          TOP NAVIGATION
      ===================================================== */}

      <header className="topbar">
        <div className="brand">
          <div className="brand-mark">
            <Activity size={20} />
          </div>

          <div>
            <div className="brand-name">
              Q-MEDTRIAGE
            </div>

            <div className="brand-sub">
              QUANTUM MEDICAL INTELLIGENCE
            </div>
          </div>
        </div>

        <nav className="nav-links">
          {[
            "OVERVIEW",
            "PIPELINE",
            "QUANTUM",
            "EVIDENCE",
            "TRIAGE",
          ].map((item, index) => {
            const targetStages = [0, 2, 4, 5, 7];

            return (
              <button
                key={item}
                onClick={() =>
                  jumpTo(targetStages[index])
                }
                className={
                  activeStage >= targetStages[index]
                    ? "nav-active"
                    : ""
                }
              >
                {item}
              </button>
            );
          })}
        </nav>

        <div className="system-status">
          <span className="status-dot" />
          SYSTEM ONLINE
        </div>
      </header>

      {/* =====================================================
          TOP PROGRESS
      ===================================================== */}

      <motion.div
        className="top-progress"
        style={{
          width: progressWidth,
        }}
      />

      {/* =====================================================
          STAGE DOT NAVIGATION
      ===================================================== */}

      <aside className="stage-dots">
        {stages.map((stage, index) => (
          <button
            key={stage.id}
            className={
              index === activeStage
                ? "dot-active"
                : ""
            }
            onClick={() => jumpTo(index)}
            title={stage.label}
          >
            <span />
            <small>{stage.label}</small>
          </button>
        ))}
      </aside>

      {/* =====================================================
          HERO
      ===================================================== */}

      <section className="hero">
        <div className="hero-grid" />

        <div className="hero-content">
          <div className="eyebrow">
            <span />
            NEXT-GENERATION MEDICAL AI
          </div>

          <h1>
            See deeper.
            <br />
            <span>Diagnose</span>
            <br />
            <strong>smarter.</strong>
          </h1>

          <p>
            Q-MedTriage combines visual intelligence,
            dimensionality reduction, quantum
            classification and evidence retrieval
            into one continuous triage pipeline.
          </p>

          <div className="hero-actions">
            <button
              className="primary-btn"
              onClick={startExperience}
            >
              <Play size={16} />
              START TRIAGE
            </button>

            <button
              className="secondary-btn"
              onClick={() => jumpTo(1)}
            >
              EXPLORE SYSTEM
              <ChevronRight size={16} />
            </button>
          </div>

          <div className="hero-metrics">
            <span>CNN</span>
            <span>PCA-4D</span>
            <span>QML</span>
            <span>RAG</span>
            <span>LLM</span>
          </div>
        </div>

        <HeroCore />

        <div className="scroll-hint">
          <ArrowDown size={14} />
          <span>SCROLL TO ENTER PIPELINE</span>
        </div>
      </section>

      {/* =====================================================
          PIPELINE STORY
      ===================================================== */}

      <section className="story">
        <div className="story-sticky">
          <PipelineCore
            activeStage={activeStage}
            image={image}
            analysisStarted={analysisStarted}
          />

          <div className="live-readout">
            <div className="stage-progress">
              {stages.map((stage, index) => (
                <div
                  key={stage.id}
                  className={`progress-dot ${
                    index <= activeStage ? "completed" : ""
                  }`}
                  title={stage.label}
                />
              ))}
            </div>

            <strong>
              {String(activeStage + 1).padStart(2, "0")} /{" "}
              {String(stages.length).padStart(2, "0")}
            </strong>
          </div>
        </div>

        <div className="story-track">
          {stages.map((stage, index) => {
            const Icon = stage.icon;

            return (
              <article
                className="scene"
                id={`scene-${index}`}
                key={stage.id}
              >
                <div className="scene-copy">
                  <div className="scene-number">
                    {String(index + 1).padStart(2, "0")}
                  </div>

                  <div className="scene-label">
                    <Icon size={15} />
                    {stage.label}
                  </div>

                  <h2>{stage.title}</h2>

                  <p>{stage.description}</p>

                  {/* Show data flow indicator */}
                  {index > 0 && index < stages.length - 1 && (
                    <div className="stage-flow-indicator">
                      <motion.div
                        className="flow-arrow"
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.5, duration: 0.6 }}
                      >
                        <ChevronRight size={12} />
                        <span>DATA FLOWS TO {stages[index + 1].label}</span>
                      </motion.div>
                    </div>
                  )}

                  <SceneDetails
                    stage={stage.id}
                    image={image}
                    fileInputRef={fileInputRef}
                    handleUpload={handleUpload}
                  />
                </div>
              </article>
            );
          })}
        </div>
      </section>

      {/* =====================================================
          FINAL SYSTEM
      ===================================================== */}

      <section className="final-system">
        <div className="eyebrow">
          <span />
          THE COMPLETE INTELLIGENCE LOOP
        </div>

        <h2>
          From pixels
          <br />
          <span>to priority.</span>
        </h2>

        <div className="system-chain">
          {[
            ["01", "IMAGE", ImageIcon],
            ["02", "CNN", BrainCircuit],
            ["03", "PCA-4D", Layers3],
            ["04", "QUANTUM", Waves],
            ["05", "RAG", Database],
            ["06", "LLM", Sparkles],
            ["07", "TRIAGE", Activity],
          ].map(([number, label, Icon], index) => (
            <div
              className="chain-node"
              key={label}
            >
              <div className="chain-icon">
                <Icon size={19} />
              </div>

              <span>{number}</span>

              <strong>{label}</strong>

              {index !== 6 && (
                <div className="chain-line">
                  <ChevronRight size={15} />
                </div>
              )}
            </div>
          ))}
        </div>

        <div className="final-note">
          <CheckCircle2 size={18} />

          <span>
            AI-assisted triage — designed to support
            clinical decision making, not replace
            medical diagnosis.
          </span>
        </div>
      </section>

      {/* =====================================================
          FOOTER
      ===================================================== */}

      <footer>
        <span>Q-MEDTRIAGE</span>
        <span>QUANTUM MEDICAL INTELLIGENCE</span>
        <span>HACKATHON PROTOTYPE • 2026</span>
      </footer>

      {/* =====================================================
          AUTO RUN
      ===================================================== */}

      <button
        className={`auto-run ${
          autoRun ? "running" : ""
        }`}
        onClick={() =>
          setAutoRun((value) => !value)
        }
      >
        <span className="auto-dot" />

        {autoRun
          ? "AUTO RUNNING"
          : "AUTO RUN"}
      </button>

      {/* =====================================================
          HIDDEN FILE INPUT
      ===================================================== */}

      <input
        ref={fileInputRef}
        type="file"
        accept="image/png,image/jpeg,image/jpg,image/webp"
        hidden
        onChange={handleUpload}
      />
    </div>
  );
}

/* ===========================================================
   HERO CORE
=========================================================== */

function HeroCore() {
  return (
    <div className="hero-core">
      <div className="orbit orbit-one" />
      <div className="orbit orbit-two" />
      <div className="orbit orbit-three" />

      <motion.div
        className="core-pulse"
        animate={{
          scale: [1, 1.08, 1],
          opacity: [0.7, 1, 0.7],
        }}
        transition={{
          duration: 2.5,
          repeat: Infinity,
        }}
      >
        <Microscope size={45} />

        <span>Q-MED</span>

        <small>ANALYTICS CORE</small>
      </motion.div>

      <div className="floating-card card-one">
        <span>IMAGE SIGNAL</span>
        <strong>READY</strong>
      </div>

      <div className="floating-card card-two">
        <span>QUANTUM CORE</span>
        <strong>STANDBY</strong>
      </div>
    </div>
  );
}

/* ===========================================================
   PIPELINE CORE
=========================================================== */

function PipelineCore({
  activeStage,
  image,
  analysisStarted,
}) {
  const featureCount = useMemo(() => {
    if (activeStage < 3) {
      return "—";
    }

    return String(DEMO_ANALYSIS.pca.outputDimension).padStart(2, "0");
  }, [activeStage]);

  return (
    <div className="pipeline-visual">
      <div className="pipeline-grid" />

      <div className="pipeline-header">
        <div className="pipeline-header-left">
          <span>Q-MED ENGINE</span>
          {image && (
            <div className="pipeline-image-indicator">
              <div className="image-preview-mini">
                <img src={image} alt="Processing" />
              </div>
              <span>IMAGE IN PIPELINE</span>
            </div>
          )}
        </div>

        <span>
          {analysisStarted
            ? "PROCESSING"
            : "STANDBY"}
        </span>
      </div>

      <div className="pipeline-stage-label">
        <small>CURRENT STAGE</small>

        <strong>
          {stages[activeStage]?.label}
        </strong>
      </div>

      <div className="visual-center">
        {activeStage === 0 && (
          <motion.div
            key="stage-0"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 1.05 }}
            transition={{ duration: 0.4 }}
          >
            <InputVisual image={image} />
          </motion.div>
        )}

        {activeStage === 1 && (
          <motion.div
            key="stage-1"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 1.05 }}
            transition={{ duration: 0.4 }}
          >
            <PreprocessVisual image={image} />
          </motion.div>
        )}

        {activeStage === 2 && (
          <motion.div
            key="stage-2"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 1.05 }}
            transition={{ duration: 0.4 }}
          >
            <CNNVisual image={image} />
          </motion.div>
        )}

        {activeStage === 3 && (
          <motion.div
            key="stage-3"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 1.05 }}
            transition={{ duration: 0.4 }}
          >
            <PCAVisual
              featureCount={featureCount}
            />
          </motion.div>
        )}

        {activeStage === 4 && (
          <motion.div
            key="stage-4"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 1.05 }}
            transition={{ duration: 0.4 }}
          >
            <QuantumVisual />
          </motion.div>
        )}

        {activeStage === 5 && (
          <motion.div
            key="stage-5"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 1.05 }}
            transition={{ duration: 0.4 }}
          >
            <EvidenceVisual />
          </motion.div>
        )}

        {activeStage === 6 && (
          <motion.div
            key="stage-6"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 1.05 }}
            transition={{ duration: 0.4 }}
          >
            <ReasonVisual />
          </motion.div>
        )}

        {activeStage === 7 && (
          <motion.div
            key="stage-7"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 1.05 }}
            transition={{ duration: 0.4 }}
          >
            <TriageVisual />
          </motion.div>
        )}
      </div>

      <div className="pipeline-footer">
        <span>LATENCY {DEMO_ANALYSIS.performance.totalLatency}</span>
        <span>MODEL ONLINE</span>
        <span>SECURE CHANNEL</span>
      </div>
    </div>
  );
}

/* ===========================================================
   INPUT
=========================================================== */

function InputVisual({ image }) {
  return (
    <motion.div
      className="input-visual"
      initial={{
        opacity: 0,
        scale: 0.85,
      }}
      animate={{
        opacity: 1,
        scale: 1,
      }}
    >
      <div className="xray-frame">
        {image ? (
          <img
            src={image}
            alt="Uploaded medical image"
          />
        ) : (
          <FakeXray />
        )}

        <motion.div
          className="scan-line"
          animate={{
            top: ["5%", "95%", "5%"],
          }}
          transition={{
            duration: 3,
            repeat: Infinity,
            ease: "linear",
          }}
        />
      </div>

      <div className="signal-chip">
        <Activity size={13} />
        IMAGE SIGNAL DETECTED
      </div>
    </motion.div>
  );
}

/* ===========================================================
   FAKE X-RAY
=========================================================== */

function FakeXray() {
  return (
    <div className="fake-xray">
      <div className="lung left" />
      <div className="lung right" />
      <div className="spine" />

      <div className="rib rib-1" />
      <div className="rib rib-2" />
      <div className="rib rib-3" />
      <div className="rib rib-4" />
      <div className="rib rib-5" />
      <div className="rib rib-6" />
    </div>
  );
}

/* ===========================================================
   PREPROCESS
=========================================================== */

function PreprocessVisual({ image }) {
  return (
    <motion.div
      className="process-visual"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
    >
      <div className="processing-image">
        {image ? (
          <img
            src={image}
            alt="Preprocessing X-ray"
            className="processing-xray-image"
          />
        ) : (
          <FakeXray />
        )}

        <motion.div
          className="processing-grid"
          animate={{
            opacity: [0.2, 0.8, 0.2],
          }}
          transition={{
            duration: 1.5,
            repeat: Infinity,
          }}
        />
      </div>

      <div className="process-stream">
        {DEMO_ANALYSIS.preprocessing.steps.map((step, i) => (
          <motion.div
            key={step.name}
            initial={{
              opacity: 0,
              x: 20,
            }}
            animate={{
              opacity: 1,
              x: 0,
            }}
            transition={{
              delay: i * 0.25,
            }}
          >
            <CheckCircle2 size={13} />
            {step.name}
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
}

/* ===========================================================
   CNN
=========================================================== */

function CNNVisual({ image }) {
  const nodes = Array.from({
    length: 18,
  });

  return (
    <div className="cnn-visual">
      <div className="cnn-image">
        {image ? (
          <img
            src={image}
            alt="CNN input X-ray"
            className="cnn-xray-image"
          />
        ) : (
          <FakeXray />
        )}
      </div>

      <div className="cnn-network">
        {nodes.map((_, i) => (
          <motion.div
            className="network-node"
            key={i}
            animate={{
              opacity: [
                0.25,
                1,
                0.25,
              ],
              scale: [
                0.8,
                1.1,
                0.8,
              ],
            }}
            transition={{
              duration: 1.4,
              repeat: Infinity,
              delay: i * 0.08,
            }}
          />
        ))}
      </div>

      <div className="cnn-output">
        <strong>{DEMO_ANALYSIS.cnn.featureDimension}</strong>
        <span>FEATURES</span>
      </div>
    </div>
  );
}

/* ===========================================================
   PCA
=========================================================== */

function PCAVisual({ featureCount }) {
  return (
    <div className="pca-visual">
      <div className="dimension-label top">
        {DEMO_ANALYSIS.pca.inputDimension}D
      </div>

      <div className="particle-field">
        {Array.from({
          length: 65,
        }).map((_, i) => (
          <motion.span
            key={i}
            className="particle"
            initial={{
              x:
                (i % 13) * 26 -
                156,
              y:
                Math.floor(i / 13) *
                  24 -
                60,
            }}
            animate={{
              x:
                ((i % 4) * 34 -
                  51) *
                activePcaPhase(i),

              y:
                (Math.floor(i / 4) *
                  30 -
                  45) *
                activePcaPhase(i),
            }}
            transition={{
              duration: 2,
              repeat: Infinity,
              repeatType:
                "reverse",
              delay:
                i * 0.015,
            }}
          />
        ))}
      </div>

      <div className="pca-axis">
        <span className="axis-x">
          X
        </span>

        <span className="axis-y">
          Y
        </span>

        <span className="axis-z">
          Z
        </span>
      </div>

      <div className="dimension-label bottom">
        {featureCount}D
      </div>

      <div className="pca-center">
        <strong>
          {DEMO_ANALYSIS.pca.inputDimension} → {DEMO_ANALYSIS.pca.outputDimension}
        </strong>

        <span>
          PCA COMPRESSION
        </span>
      </div>
    </div>
  );
}

function activePcaPhase(i) {
  return (
    0.35 +
    (i % 5) * 0.12
  );
}

/* ===========================================================
   QUANTUM
=========================================================== */

function QuantumVisual() {
  const qubits = [
    "Q0",
    "Q1",
    "Q2",
    "Q3",
  ];

  return (
    <div className="quantum-visual">
      <div className="quantum-inputs">
        {DEMO_ANALYSIS.pca.components.map((value, i) => (
          <span key={i}>{value.toFixed(2)}</span>
        ))}
      </div>

      <div className="quantum-circuit">
        {qubits.map(
          (q, row) => (
            <div
              className="qubit-row"
              key={q}
            >
              <span className="qubit-label">
                {q}
              </span>

              <motion.div
                className="qubit"
                animate={{
                  boxShadow: [
                    "0 0 0px rgba(0,230,255,0)",
                    "0 0 30px rgba(0,230,255,.8)",
                    "0 0 0px rgba(0,230,255,0)",
                  ],
                }}
                transition={{
                  duration: 1.8,
                  repeat: Infinity,
                  delay:
                    row * 0.2,
                }}
              >
                |0⟩
              </motion.div>

              <div className="gate">
                H
              </div>

              <div className="gate">
                RY
              </div>

              <div className="gate">
                RZ
              </div>

              <div className="entangle" />
            </div>
          )
        )}
      </div>

      <div className="quantum-result">
        <span>
          MEASUREMENT
        </span>

        <strong>
          {DEMO_ANALYSIS.quantum.measurement.toFixed(3)}
        </strong>
      </div>
    </div>
  );
}

/* ===========================================================
   EVIDENCE
=========================================================== */

function EvidenceVisual() {
  return (
    <div className="evidence-visual">
      <div className="vector-core">
        <Database size={32} />

        <span>
          VECTOR DB
        </span>

        <small>
          SEMANTIC SEARCH
        </small>
      </div>

      <div className="evidence-cards">
        {DEMO_ANALYSIS.evidence.results.map(
          (result, i) => (
            <motion.div
              className="evidence-card"
              key={i}
              initial={{
                opacity: 0,
                x: 50,
              }}
              animate={{
                opacity: 1,
                x: 0,
              }}
              transition={{
                delay:
                  i * 0.25,
              }}
            >
              <FileSearch size={14} />

              <span>
                {result.title}
              </span>

              <small>
                {Math.round(result.relevance * 100)}%
                match
              </small>
            </motion.div>
          )
        )}
      </div>
    </div>
  );
}

/* ===========================================================
   REASONING
=========================================================== */

function ReasonVisual() {
  return (
    <div className="reason-visual">
      <div className="reason-orbit">
        <Sparkles size={34} />
      </div>

      <div className="reason-node n1">
        MODEL
        <strong>
          {(DEMO_ANALYSIS.quantum.confidence * 100).toFixed(1)}%
        </strong>
      </div>

      <div className="reason-node n2">
        EVIDENCE
        <strong>
          {DEMO_ANALYSIS.evidence.results.length} SOURCES
        </strong>
      </div>

      <div className="reason-node n3">
        CONTEXT
        <strong>
          HIGH
        </strong>
      </div>

      <div className="reason-core">
        <Cpu size={30} />

        <span>
          LLM
        </span>

        <small>
          SYNTHESIS
        </small>
      </div>
    </div>
  );
}

/* ===========================================================
   TRIAGE
=========================================================== */

function TriageVisual() {
  const confidence = DEMO_ANALYSIS.triage.confidence;
  const confidencePercent = (confidence * 100).toFixed(1);

  return (
    <motion.div
      className="triage-visual"
      initial={{
        scale: 0.85,
        opacity: 0,
      }}
      animate={{
        scale: 1,
        opacity: 1,
      }}
    >
      <div className="triage-icon">
        <Activity size={30} />
      </div>

      <span className="triage-caption">
        AI-ASSISTED TRIAGE
      </span>

      <h3>
        {DEMO_ANALYSIS.triage.classification}
      </h3>

      <div className="confidence">
        <div className="confidence-top">
          <span>
            CONFIDENCE
          </span>

          <strong>
            {confidencePercent}%
          </strong>
        </div>

        <div className="confidence-bar">
          <motion.div
            initial={{
              width: 0,
            }}
            animate={{
              width: `${confidencePercent}%`,
            }}
            transition={{
              duration: 1.2,
            }}
          />
        </div>
      </div>

      <div className="priority">
        <span>
          PRIORITY
        </span>

        <strong>
          {DEMO_ANALYSIS.triage.priority}
        </strong>
      </div>
    </motion.div>
  );
}

/* ===========================================================
   SCENE DETAILS
=========================================================== */

function SceneDetails({
  stage,
  image,
  fileInputRef,
  handleUpload,
}) {
  if (stage === "input") {
    return (
      <div className="detail-box upload-detail">
        <button
          className="upload-btn"
          onClick={() =>
            fileInputRef.current?.click()
          }
        >
          <Upload size={15} />

          {image
            ? "REPLACE IMAGE"
            : "UPLOAD X-RAY"}
        </button>

        <span>
          PNG / JPG / JPEG
        </span>
      </div>
    );
  }

  if (stage === "preprocess") {
    return (
      <div className="mini-stats">
        <div>
          <span>INPUT</span>
          <strong>
            RAW IMAGE
          </strong>
        </div>

        <div>
          <span>OUTPUT</span>
          <strong>
            NORMALIZED
          </strong>
        </div>
      </div>
    );
  }

  if (stage === "cnn") {
    return (
      <div className="mini-stats">
        <div>
          <span>
            BACKBONE
          </span>

          <strong>
            {DEMO_ANALYSIS.cnn.backbone.toUpperCase()}
          </strong>
        </div>

        <div>
          <span>
            FEATURES
          </span>

          <strong>
            {DEMO_ANALYSIS.cnn.featureDimension}D
          </strong>
        </div>
      </div>
    );
  }

  if (stage === "pca") {
    return (
      <div className="mini-stats">
        <div>
          <span>
            BEFORE
          </span>

          <strong>
            {DEMO_ANALYSIS.pca.inputDimension}D
          </strong>
        </div>

        <div>
          <span>
            AFTER
          </span>

          <strong>
            {DEMO_ANALYSIS.pca.outputDimension}D
          </strong>
        </div>
      </div>
    );
  }

  if (stage === "quantum") {
    return (
      <div className="mini-stats">
        <div>
          <span>
            QUBITS
          </span>

          <strong>
            {DEMO_ANALYSIS.quantum.qubits}
          </strong>
        </div>

        <div>
          <span>
            STATE
          </span>

          <strong>
            ENCODED
          </strong>
        </div>
      </div>
    );
  }

  if (stage === "evidence") {
    return (
      <div className="mini-stats">
        <div>
          <span>
            RETRIEVAL
          </span>

          <strong>
            VECTOR DB
          </strong>
        </div>

        <div>
          <span>
            GROUNDING
          </span>

          <strong>
            ACTIVE
          </strong>
        </div>
      </div>
    );
  }

  if (stage === "reason") {
    return (
      <div className="mini-stats">
        <div>
          <span>
            MODEL
          </span>

          <strong>
            {(DEMO_ANALYSIS.quantum.confidence * 100).toFixed(1)}%
          </strong>
        </div>

        <div>
          <span>
            EVIDENCE
          </span>

          <strong>
            {DEMO_ANALYSIS.evidence.results.length} SOURCES
          </strong>
        </div>
      </div>
    );
  }

  return (
    <div className="triage-warning">
      <CheckCircle2 size={15} />

      AI-assisted decision support.
      Not a medical diagnosis.
    </div>
  );
}

export default App;