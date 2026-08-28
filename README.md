# Q-MedTriage

**Quantum-Enhanced Medical Image Triage with AI-Powered Explanations**

[![Python 3.14+](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![React 18](https://img.shields.io/badge/react-18-61dafb.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/fastapi-0.104+-009688.svg)](https://fastapi.tiangolo.com/)
[![Qiskit](https://img.shields.io/badge/qiskit-0.45+-6929C4.svg)](https://qiskit.org/)

> **⚠️ IMPORTANT:** This is a research prototype and educational demonstration. Not intended for medical diagnosis or clinical use.

---

##  Overview

Q-MedTriage is an AI-powered medical image triage system that combines classical machine learning, quantum computing, and retrieval-augmented generation (RAG) to classify chest X-rays and provide evidence-grounded medical explanations.

### Key Features

-  Dual Classification Pipeline**: Classical SVM and Quantum SVM classifiers
-  Transfer Learning**: ResNet50-based feature extraction (2048D → 4D PCA)
-  Quantum ML**: Qiskit-powered quantum kernel methods
-  RAG Intelligence Layer**: FAISS + SentenceTransformers + LLM synthesis
-  Interactive UI**: Real-time pipeline visualization with React + Vite
-  Evidence-Grounded**: All medical claims backed by authoritative sources

---

##  Architecture

```
Chest X-Ray Upload
      ↓
┌─────────────────────────┐
│  Image Preprocessing    │  224×224, ImageNet normalization
└─────────────────────────┘
      ↓
┌─────────────────────────┐
│  ResNet50 Features      │  Transfer learning → 2048D
└─────────────────────────┘
      ↓
┌─────────────────────────┐
│  PCA Reduction          │  2048D → 4D (quantum-ready)
└─────────────────────────┘
      ↓
┌─────────────────────────┐
│  Classification         │  Classical SVM OR Quantum SVM
└─────────────────────────┘
      ↓
┌─────────────────────────┐
│  RAG Retrieval          │  FAISS vector search (top-5)
└─────────────────────────┘
      ↓
┌─────────────────────────┐
│  LLM Synthesis          │  Groq (gpt-oss-120b)
└─────────────────────────┘
      ↓
  Prediction + Explanation
```

---

##  Quick Start

### Prerequisites

- **Python 3.14+** (with `venv` support)
- **Node.js 18+** and npm 9+
- **8GB+ RAM** (for ML models)
- **Internet connection** (first run downloads models)

### Backend Setup

```bash
# Clone repository
git clone <repository-url>
cd Q-MedTriage/backend

# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp ../.env.example ../.env
# Edit .env with your API keys (see Configuration section)

# Start backend server
.\.venv\Scripts\python.exe -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```

Backend will be available at: **http://localhost:8000**

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at: **http://localhost:5174**

---

##  Configuration

Create a `.env` file in the project root (use `.env.example` as template):

```bash
# LLM API (Groq or OpenAI-compatible)
XAI_API_KEY=gsk_your_api_key_here
XAI_MODEL=openai/gpt-oss-120b
XAI_MAX_TOKENS=1000
XAI_TEMPERATURE=0.3

# RAG Configuration
EMBEDDING_MODEL=all-MiniLM-L6-v2
RAG_TOP_K=5
VECTOR_DB_PATH=data/knowledge/index
KNOWLEDGE_CORPUS_PATH=data/knowledge/medical_corpus.json

# Intelligence Layer
INTELLIGENCE_ENABLED=true
FALLBACK_TO_PREDICTION_ONLY=true
```

### Getting API Keys

- **Groq API**: Sign up at [console.groq.com](https://console.groq.com) (free tier available)
- Alternative: Use OpenAI-compatible endpoints

---

##  Performance

### Classical SVM
- **Accuracy**: 89-91%
- **Inference Time**: ~50ms
- **Training Time**: <1 second

### Quantum SVM
- **Accuracy**: 88-92% (comparable)
- **Inference Time**: ~6-8 seconds
- **Training Time**: 6-10 minutes
- **Status**: Research prototype (simulated quantum)

### RAG + LLM
- **Retrieval Time**: ~10-20ms (FAISS)
- **LLM Synthesis**: ~1-3 seconds (Groq)
- **Knowledge Base**: 22 curated medical documents

---

##  Testing

```bash
# Run all tests
cd backend
pytest tests/ -v

# Run specific test suite
pytest tests/test_classical_svm.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

---

##  Documentation

Comprehensive technical documentation is available in [`docs/PROJECT_DOCUMENTATION.md`](docs/PROJECT_DOCUMENTATION.md), covering:

- System architecture and pipeline details
- Classical AI layer (ResNet50, PCA, SVM)
- Quantum AI layer (Qiskit, quantum kernels)
- Intelligence layer (RAG, FAISS, LLM)
- Backend API reference
- Frontend architecture
- Setup and deployment
- Medical limitations and disclaimers

---

##  Project Structure

```
Q-MedTriage/
├── frontend/              # React + Vite frontend
│   ├── src/
│   │   ├── components/    # UI components (stages, chat, etc.)
│   │   ├── hooks/         # Custom React hooks
│   │   ├── services/      # API client
│   │   └── data/          # Demo data
│   ├── public/            # Static assets
│   └── package.json
│
├── backend/               # Python backend
│   ├── src/
│   │   ├── api/           # FastAPI application
│   │   ├── inference/     # ML inference pipeline
│   │   ├── quantum/       # Quantum SVM implementation
│   │   ├── rag/           # RAG + LLM synthesis
│   │   ├── vector_db/     # FAISS + embeddings
│   │   └── utils/         # Utilities
│   ├── tests/             # Pytest test suite
│   ├── scripts/           # Diagnostic scripts
│   └── requirements.txt
│
├── data/                  # Datasets (gitignored)
├── models/                # Trained models (gitignored)
├── docs/                  # Documentation
├── notebooks/             # Jupyter notebooks (exploratory)
├── results/               # Training results (gitignored)
│
├── README.md
├── .env.example
└── .gitignore
```

---

##  Technology Stack

### Backend
- **Framework**: FastAPI
- **ML/DL**: PyTorch, scikit-learn, torchvision
- **Quantum**: Qiskit, Qiskit Machine Learning
- **RAG**: FAISS, SentenceTransformers
- **LLM**: Groq (OpenAI-compatible API)

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite
- **Styling**: Custom CSS with animations
- **State Management**: React Hooks

---

##  Dataset

**Kermany Chest X-Ray Dataset**

- **Source**: Mendeley Data (Kermany et al., 2018)
- **License**: CC BY 4.0
- **Classes**: NORMAL vs PNEUMONIA
- **Training**: 5,216 images (80% split, stratified)
- **Test**: 624 images (20% split)
- **Download**: [Kaggle - Chest X-Ray Images (Pneumonia)](https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia)

**Citation:**
```
Kermany, D., Zhang, K., & Goldbaum, M. (2018).
Labeled Optical Coherence Tomography (OCT) and Chest X-Ray Images for Classification.
Mendeley Data, v2. http://dx.doi.org/10.17632/rscbjbr9sj.2
```

---

##  Medical Disclaimer

**Q-MedTriage is a research prototype and educational demonstration.**

### This System is NOT:
- ❌ A medical device
- ❌ FDA-approved or clinically validated
- ❌ Intended for patient diagnosis
- ❌ A replacement for professional medical evaluation

### This System IS:
- ✅ An educational AI/ML demonstration
- ✅ A research prototype exploring quantum ML
- ✅ A showcase of RAG-based medical information retrieval
- ✅ For learning and hackathon purposes only

**If you have medical concerns, consult a qualified healthcare provider immediately.**

---

##  Educational Purpose

This project demonstrates:
- Transfer learning with pretrained CNNs
- Dimensionality reduction (PCA)
- Classical vs. quantum machine learning comparison
- Retrieval-augmented generation (RAG)
- LLM integration with safety constraints
- Medical AI safety and transparency principles

---

## 🔮 Future Enhancements

- [ ] Multi-class classification (bacterial vs. viral pneumonia)
- [ ] Grad-CAM visualization for explainability
- [ ] Real quantum hardware integration
- [ ] DICOM support
- [ ] Expanded multilingual knowledge base
- [ ] Clinical validation studies

---

##  License

[Specify License - e.g., MIT, Apache 2.0]

---

##  Acknowledgments

### Medical Knowledge Sources
- World Health Organization (WHO)
- Centers for Disease Control and Prevention (CDC)
- National Institutes of Health (NIH)
- Mayo Clinic

### Technologies
- PyTorch & TorchVision (Meta AI)
- Qiskit (IBM Quantum)
- FastAPI (Sebastián Ramírez)
- React (Meta)
- FAISS (Facebook Research)
- SentenceTransformers (Hugging Face)

---

##  Contact

[Add contact information or leave blank for hackathon submission]

---

**Built with ❤️ for advancing AI in healthcare education**
