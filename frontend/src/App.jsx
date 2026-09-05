/**
 * Q-MEDTRIAGE - STATE-DRIVEN APPLICATION
 * 
 * Professional medical AI triage system with state-driven pipeline
 */

import React from "react";
import { AnimatePresence, motion } from "framer-motion";
import {
  ArrowDown,
  ChevronRight,
  Microscope,
  Play,
} from "lucide-react";
import { useAnalysisPipeline, STAGES } from "./hooks/useAnalysisPipeline";
import {
  ChatInterface,
  PipelineProgress,
  UploadStage,
  PreviewStage,
  ValidatingStage,
  ScanningStage,
  PreprocessingStage,
  FeatureExtractionStage,
  DimensionalityReductionStage,
  QuantumProcessingStage,
  EvidenceRetrievalStage,
  ReasoningStage,
  ResultStage,
  AnalysisModeSelection,
  BulkUploadStage,
  BulkProcessingStage,
  BulkResultsStage,
} from "./components";
import "./App.css";
import "./stages.css";
import "./bulk-analysis.css";

function App() {
  const {
    currentStage,
    completedStages,
    uploadedImage,
    bulkFiles,
    bulkResults,
    isBulkProcessing,
    bulkError,
    predictionResult,
    predictionError,
    validationError,
    startTriage,
    selectMode,
    handleImageUpload,
    startAnalysis,
    handleBulkUpload,
    backToModeSelection,
    resetPipeline,
    openChat,
  } = useAnalysisPipeline();

  const showProgress = currentStage !== STAGES.LANDING && 
                       currentStage !== STAGES.MODE_SELECTION &&
                       currentStage !== STAGES.UPLOAD && 
                       currentStage !== STAGES.PREVIEW &&
                       currentStage !== STAGES.VALIDATING &&
                       currentStage !== STAGES.BULK_UPLOAD &&
                       currentStage !== STAGES.BULK_PROCESSING &&
                       currentStage !== STAGES.BULK_RESULTS &&
                       currentStage !== STAGES.CHAT;

  return (
    <div className="qmed-app redesigned">
      <div className="noise" />

      {/* Pipeline Progress Indicator */}
      {showProgress && (
        <PipelineProgress
          currentStage={currentStage}
          completedStages={completedStages}
        />
      )}

      {/* Main Content */}
      <AnimatePresence mode="wait">
        {/* LANDING / HERO */}
        {currentStage === STAGES.LANDING && (
          <HeroSection
            key="hero"
            onStartTriage={startTriage}
          />
        )}

        {/* MODE SELECTION */}
        {currentStage === STAGES.MODE_SELECTION && (
          <AnalysisModeSelection
            key="mode-selection"
            onSelectMode={selectMode}
          />
        )}

        {/* UPLOAD (Single Mode) */}
        {currentStage === STAGES.UPLOAD && (
          <UploadStage 
            key="upload" 
            onImageUpload={handleImageUpload} 
            onBack={backToModeSelection}
          />
        )}

        {/* PREVIEW */}
        {currentStage === STAGES.PREVIEW && (
          <PreviewStage
            key="preview"
            image={uploadedImage}
            onStartAnalysis={startAnalysis}
            onReset={resetPipeline}
          />
        )}

        {/* VALIDATING */}
        {currentStage === STAGES.VALIDATING && (
          <ValidatingStage key="validating" />
        )}

        {/* BULK UPLOAD */}
        {currentStage === STAGES.BULK_UPLOAD && (
          <BulkUploadStage
            key="bulk-upload"
            onImagesUpload={handleBulkUpload}
            onBack={backToModeSelection}
          />
        )}

        {/* BULK PROCESSING */}
        {currentStage === STAGES.BULK_PROCESSING && (
          <BulkProcessingStage
            key="bulk-processing"
            totalImages={bulkFiles.length}
            completedImages={isBulkProcessing ? 0 : bulkFiles.length}
          />
        )}

        {/* BULK RESULTS */}
        {currentStage === STAGES.BULK_RESULTS && bulkResults && (
          <BulkResultsStage
            key="bulk-results"
            batchResults={bulkResults}
            uploadedFiles={bulkFiles}
            onReset={resetPipeline}
          />
        )}

        {/* SCANNING */}
        {currentStage === STAGES.SCANNING && (
          <ScanningStage key="scanning" image={uploadedImage} />
        )}

        {/* PREPROCESSING */}
        {currentStage === STAGES.PREPROCESSING && (
          <PreprocessingStage key="preprocessing" image={uploadedImage} />
        )}

        {/* FEATURE EXTRACTION */}
        {currentStage === STAGES.FEATURE_EXTRACTION && (
          <FeatureExtractionStage key="features" image={uploadedImage} />
        )}

        {/* DIMENSIONALITY REDUCTION */}
        {currentStage === STAGES.DIMENSIONALITY_REDUCTION && (
          <DimensionalityReductionStage key="pca" />
        )}

        {/* QUANTUM PROCESSING */}
        {currentStage === STAGES.QUANTUM_PROCESSING && (
          <QuantumProcessingStage key="quantum" />
        )}

        {/* EVIDENCE RETRIEVAL */}
        {currentStage === STAGES.EVIDENCE_RETRIEVAL && (
          <EvidenceRetrievalStage key="evidence" predictionData={predictionResult} />
        )}

        {/* REASONING */}
        {currentStage === STAGES.REASONING && (
          <ReasoningStage key="reasoning" predictionData={predictionResult} />
        )}

        {/* RESULT */}
        {currentStage === STAGES.RESULT && (
          <ResultStage
            key="result"
            image={uploadedImage}
            predictionData={predictionResult}
            error={predictionError}
            validationError={validationError}
            onOpenChat={openChat}
            onReset={resetPipeline}
          />
        )}

        {/* CHAT / Q&A */}
        {currentStage === STAGES.CHAT && (
          <ChatInterface
            key="chat"
            predictionData={predictionResult}
            image={uploadedImage}
            onClose={() => resetPipeline()}
          />
        )}
      </AnimatePresence>

      {/* Footer */}
      {currentStage === STAGES.LANDING && (
        <footer>
          <span>Q-MEDTRIAGE</span>
          <span>QUANTUM MEDICAL INTELLIGENCE</span>
          <span>RESEARCH PROTOTYPE • 2026</span>
        </footer>
      )}
    </div>
  );
}

/**
 * HERO / LANDING SECTION
 */
function HeroSection({ onStartTriage }) {
  return (
    <>
      <section className="hero">
        {/* Compact Header */}
        <header className="hero-header">
          <div className="hero-header-content">
            <div className="brand">
              <div className="brand-mark">
                <Microscope size={20} />
              </div>
              <div>
                <div className="brand-name">Q-MEDTRIAGE</div>
                <div className="brand-sub">QUANTUM MEDICAL INTELLIGENCE</div>
              </div>
            </div>
            
            <div className="system-status">
              <span className="status-dot"></span>
              <span className="status-text">SYSTEM READY</span>
            </div>
          </div>
        </header>

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
            Q-MedTriage combines visual intelligence, dimensionality reduction,
            quantum classification and evidence retrieval into one continuous
            triage pipeline.
          </p>

          <div className="hero-actions">
            <button className="primary-btn" onClick={onStartTriage}>
              <Play size={16} />
              Start Triage
            </button>

            <button
              className="secondary-btn"
              onClick={() => {
                document.querySelector(".landing-what-is")?.scrollIntoView({ 
                  behavior: "smooth"
                });
              }}
            >
              Explore System
              <ChevronRight size={16} />
            </button>
          </div>

          <div className="hero-metrics">
            <span>CNN</span>
            <span>PCA-4D</span>
            <span>SVM</span>
            <span>QML</span>
            <span>RAG</span>
          </div>
        </div>

        <HeroCore />

        <div className="scroll-hint">
          <ArrowDown size={14} />
          <span>SCROLL TO EXPLORE</span>
        </div>
      </section>

      <LandingContent onStartTriage={onStartTriage} />
    </>
  );
}

/**
 * HERO CORE ANIMATION - Orbital rings with pipeline nodes
 */
function HeroCore() {
  return (
    <div className="hero-core">
      {/* Processing pipeline nodes */}
      <div className="pipeline-node node-1">
        <div className="node-dot" />
        <span>CHEST X-RAY</span>
      </div>
      
      <div className="pipeline-node node-2">
        <div className="node-dot" />
        <span>AI ANALYSIS</span>
      </div>
      
      <div className="pipeline-node node-3">
        <div className="node-dot" />
        <span>EVIDENCE</span>
      </div>
      
      <div className="pipeline-node node-4">
        <div className="node-dot" />
        <span>INSIGHT</span>
      </div>

      {/* Connection lines */}
      <svg className="pipeline-connections" viewBox="0 0 500 500">
        <path className="connect-line line-1" d="M 250 250 L 250 80" />
        <path className="connect-line line-2" d="M 250 250 L 420 250" />
        <path className="connect-line line-3" d="M 250 250 L 250 420" />
        <path className="connect-line line-4" d="M 250 250 L 80 250" />
        
        {/* Animated signal particles */}
        <circle className="signal-particle" r="3" fill="#00e5ff">
          <animateMotion dur="3s" repeatCount="indefinite">
            <mpath href="#path-1" />
          </animateMotion>
        </circle>
        
        <defs>
          <path id="path-1" d="M 250 80 L 250 250 L 420 250 L 250 250 L 250 420 L 250 250 L 80 250 L 250 250" />
        </defs>
      </svg>

      {/* Orbital rings in background */}
      <div className="orbit-ring ring-1" />
      <div className="orbit-ring ring-2" />
      <div className="orbit-ring ring-3" />
    </div>
  );
}

/**
 * LANDING CONTENT - Premium AI research product experience
 */
function LandingContent({ onStartTriage }) {
  const [activeWorkflowStep, setActiveWorkflowStep] = React.useState(0);
  const [hoveredPath, setHoveredPath] = React.useState(null);

  React.useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const step = parseInt(entry.target.dataset.workflowstep);
            if (!isNaN(step)) {
              setActiveWorkflowStep(step);
            }
          }
        });
      },
      { threshold: 0.6 }
    );

    document.querySelectorAll('[data-workflowstep]').forEach((el) => {
      observer.observe(el);
    });

    return () => observer.disconnect();
  }, []);

  return (
    <div className="landing-content-redesign">
      {/* Unified continuous background */}
      <div className="unified-background">
        <div className="bg-particle-system">
          {[...Array(60)].map((_, i) => (
            <div
              key={i}
              className="bg-particle"
              style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
                animationDelay: `${Math.random() * -30}s`,
                animationDuration: `${20 + Math.random() * 30}s`,
              }}
            />
          ))}
        </div>
        <div className="bg-grid-system" />
        <div className="bg-radial-field top" />
        <div className="bg-radial-field bottom" />
        <div className="bg-scan-line" />
      </div>

      {/* SECTION: SYSTEM ARCHITECTURE - Compact horizontal flow */}
      <section className="architecture-section">
        <div className="section-container-wide">
          <div className="section-intro">
            <div className="label-tech">SYSTEM ARCHITECTURE</div>
            <h2>Medical intelligence structured for decision support</h2>
            <p>Integrated pipeline combining computer vision, dimensionality reduction, dual classification pathways, and evidence-based reasoning.</p>
          </div>

          <div className="architecture-map-horizontal">
            <svg className="arch-connections" viewBox="0 0 1200 400" preserveAspectRatio="xMidYMid meet">
              {/* Main flow path */}
              <path d="M 100 200 L 300 200" className="flow-path" />
              <path d="M 300 200 L 500 200" className="flow-path" />
              <path d="M 500 200 L 650 200" className="flow-path" />
              
              {/* Branch to dual pathways */}
              <path d="M 650 200 L 750 150" className="flow-path branch" />
              <path d="M 650 200 L 750 250" className="flow-path branch" />
              
              {/* Convergence */}
              <path d="M 900 150 L 1000 200" className="flow-path" />
              <path d="M 900 250 L 1000 200" className="flow-path" />
              <path d="M 1000 200 L 1100 200" className="flow-path" />
              
              {/* Animated flow particles */}
              {[...Array(3)].map((_, i) => (
                <circle key={i} r="4" fill="#00e5ff" className="flow-particle">
                  <animateMotion
                    dur="8s"
                    repeatCount="indefinite"
                    begin={`${i * 2.6}s`}
                  >
                    <mpath href="#main-flow" />
                  </animateMotion>
                </circle>
              ))}
              
              <defs>
                <path id="main-flow" d="M 100 200 L 300 200 L 500 200 L 650 200 L 750 150 L 900 150 L 1000 200 L 1100 200" />
              </defs>
            </svg>

            {/* Architecture nodes */}
            <div className="arch-node" style={{ left: '8%', top: '50%' }}>
              <div className="arch-node-visual">
                <div className="node-icon-frame" />
              </div>
              <div className="arch-node-label">CHEST X-RAY</div>
              <div className="arch-node-meta">Medical image</div>
            </div>

            <div className="arch-node" style={{ left: '25%', top: '50%' }}>
              <div className="arch-node-visual processing">
                <div className="node-icon-layers">
                  {[...Array(5)].map((_, i) => (
                    <div key={i} className="layer" style={{ '--delay': `${i * 0.1}s` }} />
                  ))}
                </div>
              </div>
              <div className="arch-node-label">RESNET50</div>
              <div className="arch-node-meta">Visual features</div>
            </div>

            <div className="arch-node highlight" style={{ left: '42%', top: '50%' }}>
              <div className="arch-node-visual feature-dense">
                <div className="dense-representation">
                  {[...Array(20)].map((_, i) => (
                    <div key={i} className="feature-point" style={{ '--index': i }} />
                  ))}
                </div>
              </div>
              <div className="arch-node-label">2048-D SPACE</div>
              <div className="arch-node-meta">High-dimensional</div>
            </div>

            <div className="arch-node transform" style={{ left: '58%', top: '50%' }}>
              <div className="arch-node-visual compress">
                <div className="compress-indicator">
                  <span className="from">2048</span>
                  <span className="arrow">→</span>
                  <span className="to">4</span>
                </div>
              </div>
              <div className="arch-node-label">PCA</div>
              <div className="arch-node-meta">Dimensionality reduction</div>
            </div>

            <div 
              className="arch-node pathway-classical" 
              style={{ left: '75%', top: '30%' }}
              onMouseEnter={() => setHoveredPath('classical')}
              onMouseLeave={() => setHoveredPath(null)}
            >
              <div className="arch-node-visual svm">
                <div className="svm-visual-mini">
                  <div className="svm-line" />
                  <div className="svm-points">
                    {[...Array(6)].map((_, i) => (
                      <div key={i} className="svm-point" />
                    ))}
                  </div>
                </div>
              </div>
              <div className="arch-node-label">CLASSICAL SVM</div>
              <div className="arch-node-meta">Primary baseline</div>
              <div className="pathway-badge">PRIMARY</div>
            </div>

            <div 
              className="arch-node pathway-quantum" 
              style={{ left: '75%', top: '70%' }}
              onMouseEnter={() => setHoveredPath('quantum')}
              onMouseLeave={() => setHoveredPath(null)}
            >
              <div className="arch-node-visual quantum">
                <div className="quantum-visual-mini">
                  <div className="q-orbit" />
                  <div className="q-center" />
                </div>
              </div>
              <div className="arch-node-label">QUANTUM QSVC</div>
              <div className="arch-node-meta">Experimental</div>
              <div className="pathway-badge">RESEARCH</div>
            </div>

            <div className="arch-node evidence" style={{ left: '91.5%', top: '50%' }}>
              <div className="arch-node-visual network">
                <div className="network-visual">
                  {[...Array(4)].map((_, i) => (
                    <div key={i} className="network-node" style={{ '--index': i }} />
                  ))}
                </div>
              </div>
              <div className="arch-node-label">EVIDENCE + CONTEXT</div>
              <div className="arch-node-meta">RAG intelligence</div>
            </div>
          </div>
        </div>
      </section>

      {/* SECTION: WORKFLOW - Horizontal cinematic progression */}
      <section className="workflow-section">
        <div className="section-container-wide">
          <div className="section-intro">
            <div className="label-tech">ANALYSIS WORKFLOW</div>
            <h2>From image to insight</h2>
          </div>

          <div className="workflow-horizontal">
            {[
              { 
                key: 'upload',
                label: 'UPLOAD',
                title: 'Medical image input',
                desc: 'Single or batch chest X-ray analysis'
              },
              { 
                key: 'validate',
                label: 'VALIDATE',
                title: 'Safety verification',
                desc: 'Ensure appropriate image type'
              },
              { 
                key: 'extract',
                label: 'EXTRACT',
                title: 'Visual features',
                desc: 'ResNet50 → 2048-D representation'
              },
              { 
                key: 'reduce',
                label: 'REDUCE',
                title: 'Compress to 4-D',
                desc: 'PCA dimensionality reduction'
              },
              { 
                key: 'classify',
                label: 'CLASSIFY',
                title: 'Dual pathways',
                desc: 'Classical SVM + Quantum QSVC'
              },
              { 
                key: 'retrieve',
                label: 'EVIDENCE',
                title: 'Context retrieval',
                desc: 'Knowledge base integration'
              },
              { 
                key: 'support',
                label: 'SUPPORT',
                title: 'Decision output',
                desc: 'Structured research support'
              },
            ].map((step, index) => (
              <div
                key={step.key}
                className={`workflow-step ${activeWorkflowStep === index ? 'active' : ''}`}
                data-workflowstep={index}
              >
                <div className="workflow-step-visual">
                  {step.key === 'upload' && (
                    <div className="visual-upload">
                      <div className="upload-frame-icon" />
                      <div className="upload-indicator-line" />
                    </div>
                  )}
                  {step.key === 'validate' && (
                    <div className="visual-validate">
                      <div className="validate-circle" />
                      <div className="validate-check" />
                    </div>
                  )}
                  {step.key === 'extract' && (
                    <div className="visual-extract">
                      <div className="extract-core" />
                      {[...Array(16)].map((_, i) => (
                        <div key={i} className="extract-ray" style={{ '--index': i }} />
                      ))}
                    </div>
                  )}
                  {step.key === 'reduce' && (
                    <div className="visual-reduce">
                      <div className="reduce-cloud">
                        {[...Array(30)].map((_, i) => (
                          <div key={i} className="reduce-dot" />
                        ))}
                      </div>
                      <div className="reduce-compact">
                        <div className="compact-box" />
                      </div>
                    </div>
                  )}
                  {step.key === 'classify' && (
                    <div className="visual-classify">
                      <div className="classify-split-icon" />
                    </div>
                  )}
                  {step.key === 'retrieve' && (
                    <div className="visual-retrieve">
                      <div className="retrieve-center" />
                      {[...Array(4)].map((_, i) => (
                        <div key={i} className="retrieve-node" style={{ '--index': i }} />
                      ))}
                    </div>
                  )}
                  {step.key === 'support' && (
                    <div className="visual-support">
                      <div className="support-panel">
                        <div className="panel-line" />
                        <div className="panel-line" />
                        <div className="panel-line" />
                      </div>
                    </div>
                  )}
                </div>
                <div className="workflow-step-num">{String(index + 1).padStart(2, '0')}</div>
                <div className="workflow-step-label">{step.label}</div>
                <div className="workflow-step-content">
                  <h4>{step.title}</h4>
                  <p>{step.desc}</p>
                </div>
                {index < 6 && <div className="workflow-connector" />}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* SECTION: FEATURE TRANSFORMATION - Large visual composition */}
      <section className="transformation-section">
        <div className="section-container-wide">
          <div className="section-intro">
            <div className="label-tech">FEATURE ENGINEERING</div>
            <h2>From pixels to structured intelligence</h2>
            <div className="tech-note">Conceptual feature-space visualization</div>
          </div>

          <div className="transformation-large">
            {/* Left: X-Ray representation */}
            <div className="transform-panel input-panel">
              <div className="panel-visual">
                <div className="xray-representation">
                  <div className="xray-frame-large">
                    {/* Stylized chest X-ray grid */}
                    <div className="chest-grid">
                      {[...Array(12)].map((_, row) => (
                        [...Array(8)].map((_, col) => (
                          <div 
                            key={`${row}-${col}`}
                            className="grid-cell"
                            style={{
                              opacity: 0.1 + Math.random() * 0.4,
                              animationDelay: `${(row + col) * 0.05}s`
                            }}
                          />
                        ))
                      ))}
                    </div>
                    {/* Anatomical overlay suggestion */}
                    <div className="anatomy-overlay">
                      <div className="lung-region left" />
                      <div className="lung-region right" />
                    </div>
                  </div>
                </div>
              </div>
              <div className="panel-label">MEDICAL IMAGE</div>
              <div className="panel-meta">Chest X-ray input</div>
            </div>

            {/* Center: Neural network transformation */}
            <div className="transform-process">
              <div className="process-label">RESNET50</div>
              <div className="neural-flow">
                {[...Array(5)].map((_, i) => (
                  <div key={i} className="neural-layer" style={{ '--index': i }}>
                    {[...Array(8)].map((_, j) => (
                      <div key={j} className="neural-node" />
                    ))}
                  </div>
                ))}
              </div>
              <div className="flow-arrow-large">
                <div className="arrow-line" />
                <div className="arrow-head" />
              </div>
            </div>

            {/* Right: High-dimensional space */}
            <div className="transform-panel feature-panel">
              <div className="panel-visual">
                <div className="feature-space-3d">
                  {[...Array(200)].map((_, i) => (
                    <div
                      key={i}
                      className="feature-particle"
                      style={{
                        left: `${Math.random() * 100}%`,
                        top: `${Math.random() * 100}%`,
                        animationDelay: `${Math.random() * 3}s`,
                        animationDuration: `${2 + Math.random() * 2}s`,
                      }}
                    />
                  ))}
                </div>
              </div>
              <div className="panel-label">2048-D FEATURES</div>
              <div className="panel-meta">High-dimensional space</div>
            </div>

            {/* Bottom: PCA compression */}
            <div className="transform-compress">
              <div className="compress-flow">
                <div className="compress-label">PCA COMPRESSION</div>
                <div className="compress-visual-large">
                  <div className="compress-from-cloud">
                    {[...Array(80)].map((_, i) => (
                      <div key={i} className="cloud-particle" />
                    ))}
                  </div>
                  <div className="compress-arrow-animated">
                    <div className="arrow-shaft" />
                  </div>
                  <div className="compress-to-compact">
                    <div className="compact-axes">
                      <div className="axis pc1">PC1</div>
                      <div className="axis pc2">PC2</div>
                      <div className="axis pc3">PC3</div>
                      <div className="axis pc4">PC4</div>
                    </div>
                  </div>
                </div>
                <div className="dimension-stat">
                  <span>2048 dimensions</span>
                  <span className="arrow-text">→</span>
                  <span className="highlight">4 principal components</span>
                </div>
              </div>
            </div>
          </div>

          <div className="transformation-explanation">
            <p>Principal Component Analysis preserves maximal variance while reducing dimensionality, creating an efficient representation for classification algorithms.</p>
          </div>
        </div>
      </section>

      {/* SECTION: DUAL PATHWAYS - Immersive comparison */}
      <section className="pathways-section">
        <div className="section-container-wide">
          <div className="section-intro">
            <div className="label-tech">CLASSIFICATION PATHWAYS</div>
            <h2>Primary baseline + experimental quantum research</h2>
          </div>

          <div className="pathways-split">
            {/* Classical pathway */}
            <div 
              className={`pathway-panel classical ${hoveredPath === 'classical' ? 'hovered' : ''}`}
              onMouseEnter={() => setHoveredPath('classical')}
              onMouseLeave={() => setHoveredPath(null)}
            >
              <div className="pathway-header">
                <div className="pathway-icon classical-icon-large">
                  <div className="icon-svm-boundary" />
                </div>
                <h3>CLASSICAL MACHINE LEARNING</h3>
                <div className="pathway-status-badge primary">PRIMARY PIPELINE</div>
              </div>

              <div className="pathway-visual-large">
                <div className="classical-feature-space">
                  <div className="feature-space-plane">
                    {/* SVM decision boundary */}
                    <div className="decision-boundary" />
                    
                    {/* Data points */}
                    {[...Array(30)].map((_, i) => {
                      const side = i < 15 ? 'positive' : 'negative';
                      return (
                        <div
                          key={i}
                          className={`data-point-class ${side}`}
                          style={{
                            left: `${side === 'positive' ? 20 + Math.random() * 30 : 55 + Math.random() * 30}%`,
                            top: `${20 + Math.random() * 60}%`,
                            animationDelay: `${i * 0.05}s`,
                          }}
                        />
                      );
                    })}
                  </div>
                </div>
              </div>

              <div className="pathway-description">
                <ul className="pathway-features">
                  <li><span className="check-mark">✓</span> Support Vector Machine classifier</li>
                  <li><span className="check-mark">✓</span> Stable baseline performance</li>
                  <li><span className="check-mark">✓</span> Conventional kernel methods</li>
                  <li><span className="check-mark">✓</span> Primary reference pathway</li>
                </ul>
              </div>

              <div className="pathway-tech-spec">
                <div className="spec-row">
                  <span className="spec-label">INPUT</span>
                  <span className="spec-value">4-D PCA features</span>
                </div>
                <div className="spec-row">
                  <span className="spec-label">METHOD</span>
                  <span className="spec-value">SVM with RBF kernel</span>
                </div>
                <div className="spec-row">
                  <span className="spec-label">ROLE</span>
                  <span className="spec-value">Primary classifier</span>
                </div>
              </div>
            </div>

            {/* Divider */}
            <div className="pathways-divider">
              <div className="divider-line" />
              <div className="divider-badge">DUAL APPROACH</div>
            </div>

            {/* Quantum pathway */}
            <div 
              className={`pathway-panel quantum ${hoveredPath === 'quantum' ? 'hovered' : ''}`}
              onMouseEnter={() => setHoveredPath('quantum')}
              onMouseLeave={() => setHoveredPath(null)}
            >
              <div className="pathway-header">
                <div className="pathway-icon quantum-icon-large">
                  <div className="quantum-rings">
                    <div className="q-ring ring-a" />
                    <div className="q-ring ring-b" />
                    <div className="q-center-dot" />
                  </div>
                </div>
                <h3>QUANTUM MACHINE LEARNING</h3>
                <div className="pathway-status-badge experimental">EXPERIMENTAL</div>
              </div>

              <div className="pathway-visual-large quantum-env">
                <div className="quantum-feature-space">
                  {/* Quantum state representation */}
                  <div className="quantum-state-visual">
                    {[...Array(4)].map((_, i) => (
                      <div
                        key={i}
                        className="quantum-orbital"
                        style={{
                          '--angle': `${i * 90}deg`,
                          '--delay': `${i * 0.5}s`,
                        }}
                      >
                        <div className="orbital-path" />
                        <div className="qubit-state" />
                      </div>
                    ))}
                    <div className="quantum-center-core" />
                  </div>
                  
                  {/* Quantum feature encoding visualization */}
                  <div className="encoding-indicators">
                    {['q₀', 'q₁', 'q₂', 'q₃'].map((qubit, i) => (
                      <div key={i} className="qubit-indicator" style={{ '--index': i }}>
                        <span>{qubit}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              <div className="pathway-description">
                <ul className="pathway-features">
                  <li><span className="check-mark">✓</span> Quantum Support Vector Classifier</li>
                  <li><span className="check-mark">✓</span> Quantum kernel evaluation</li>
                  <li><span className="check-mark">✓</span> Feature-space exploration</li>
                  <li><span className="check-mark">✓</span> Research pathway</li>
                </ul>
              </div>

              <div className="pathway-tech-spec">
                <div className="spec-row">
                  <span className="spec-label">FRAMEWORK</span>
                  <span className="spec-value">Qiskit</span>
                </div>
                <div className="spec-row">
                  <span className="spec-label">FEATURE MAP</span>
                  <span className="spec-value">ZZFeatureMap</span>
                </div>
                <div className="spec-row">
                  <span className="spec-label">SIMULATOR</span>
                  <span className="spec-value">Statevector</span>
                </div>
              </div>

              <div className="pathway-disclaimer">
                <strong>Experimental research layer</strong>
                <p>Evaluated alongside classical baseline — not a replacement</p>
              </div>
            </div>
          </div>

          <div className="pathways-note">
            Both pathways operate on the same compact 4-D PCA representation using different feature-space reasoning approaches.
          </div>
        </div>
      </section>

      {/* SECTION: EVIDENCE INTELLIGENCE - Knowledge network */}
      <section className="evidence-section">
        <div className="section-container-wide">
          <div className="section-intro">
            <div className="label-tech">EVIDENCE LAYER</div>
            <h2>Context and knowledge integration</h2>
          </div>

          <div className="evidence-network-large">
            <div className="network-center">
              <div className="center-node prediction-node">
                <div className="node-core-large" />
                <div className="node-label-large">MODEL OUTPUT</div>
              </div>
            </div>

            {/* Evidence nodes */}
            {[
              { label: 'MEDICAL KNOWLEDGE', angle: 0, distance: 180 },
              { label: 'EVIDENCE BASE', angle: 90, distance: 180 },
              { label: 'CONTEXT DATA', angle: 180, distance: 180 },
              { label: 'REFERENCES', angle: 270, distance: 180 },
            ].map((node, i) => (
              <div
                key={i}
                className="evidence-node-large"
                style={{
                  '--angle': `${node.angle}deg`,
                  '--distance': `${node.distance}px`,
                  '--delay': `${i * 0.2}s`,
                }}
              >
                <div className="evidence-node-core" />
                <div className="evidence-node-label">{node.label}</div>
                <svg className="connection-line" viewBox="0 0 200 200">
                  <line x1="100" y1="100" x2="100" y2="20" className="evidence-connection" />
                </svg>
              </div>
            ))}

            {/* Secondary context nodes */}
            {[...Array(8)].map((_, i) => (
              <div
                key={i}
                className="context-node-small"
                style={{
                  '--angle': `${i * 45 + 22.5}deg`,
                  '--distance': '280px',
                  '--delay': `${i * 0.15}s`,
                }}
              >
                <div className="context-dot" />
              </div>
            ))}

            {/* Synthesis flow */}
            <div className="synthesis-flow">
              <div className="flow-stage stage-1">
                <div className="stage-label">RETRIEVAL</div>
              </div>
              <div className="flow-arrow-synthesis" />
              <div className="flow-stage stage-2">
                <div className="stage-label">INTERPRETATION</div>
              </div>
              <div className="flow-arrow-synthesis" />
              <div className="flow-stage stage-3">
                <div className="stage-label">DECISION SUPPORT</div>
              </div>
            </div>
          </div>

          <div className="evidence-explanation">
            <p>Retrieval-augmented generation integrates model outputs with contextual medical knowledge, providing structured evidence-based decision support for research applications.</p>
          </div>
        </div>
      </section>

      {/* SECTION: FINAL CTA - Cinematic conclusion */}
      <section className="final-cta-section">
        <div className="cta-atmosphere-layer" />
        <div className="section-container-wide">
          <div className="cta-main">
            <h2 className="cta-headline-large">Ready to enter the system?</h2>
            
            <div className="cta-pipeline-visual">
              <div className="pipeline-flow-line" />
              {[
                { label: 'CHEST X-RAY', icon: 'frame' },
                { label: 'AI ANALYSIS', icon: 'brain' },
                { label: 'EVIDENCE', icon: 'network' },
                { label: 'INSIGHTS', icon: 'output' },
              ].map((stage, i) => (
                <div key={i} className="cta-stage" style={{ '--index': i }}>
                  <div className={`cta-stage-icon icon-${stage.icon}`}>
                    <div className="icon-shape" />
                  </div>
                  <div className="cta-stage-label">{stage.label}</div>
                </div>
              ))}
            </div>

            <button className="cta-button-large" onClick={onStartTriage}>
              <Play size={24} />
              <span>Start Triage</span>
            </button>

            <div className="cta-disclaimer-text">
              Research prototype • Not for clinical diagnosis
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

export default App;
