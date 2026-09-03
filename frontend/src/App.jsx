/**
 * Q-MEDTRIAGE - STATE-DRIVEN APPLICATION
 * 
 * Professional medical AI triage system with state-driven pipeline
 */

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
import "./landing-info.css";
import {
  AboutSection,
  WorkflowSection,
  PipelineArchitectureSection,
  QuantumExplanationSection,
  ComparisonSection,
  IntelligenceSection,
  CTASection,
} from "./components/LandingInfo";

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
          <>
            <HeroSection
              key="hero"
              onStartTriage={startTriage}
            />
            <AboutSection key="about" />
            <WorkflowSection key="workflow" />
            <PipelineArchitectureSection key="architecture" />
            <QuantumExplanationSection key="quantum" />
            <ComparisonSection key="comparison" />
            <IntelligenceSection key="intelligence" />
            <CTASection key="cta" onStartTriage={startTriage} />
          </>
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
              document.querySelector(".hero")?.scrollIntoView({ 
                behavior: "smooth",
                block: "end"
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
  );
}

/**
 * HERO CORE ANIMATION
 */
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

export default App;
