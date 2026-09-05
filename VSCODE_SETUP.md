# VS Code Setup Guide for Q-MedTriage

## Prerequisites Checklist

Before starting, make sure you have:

- [ ] **Python 3.10 or higher** installed ([python.org/downloads](https://www.python.org/downloads/))
- [ ] **Node.js 18+** and npm installed ([nodejs.org](https://nodejs.org/))
- [ ] **VS Code** installed ([code.visualstudio.com](https://code.visualstudio.com/))
- [ ] **Git** (optional, for cloning)
- [ ] **8GB+ RAM** available

---

## Step-by-Step Setup

### 1. Open Project in VS Code

```bash
# If you have the project folder:
cd path/to/Q-MedTriage
code .

# Or open VS Code and use File > Open Folder
```

### 2. Install VS Code Extensions (Recommended)

Press `Ctrl+Shift+X` to open Extensions, then install:

- **Python** (by Microsoft) - Python language support
- **Pylance** (by Microsoft) - Fast Python language server
- **ES7+ React/Redux/React-Native snippets** - React development
- **ESLint** - JavaScript linting

### 3. Backend Setup

#### 3.1 Open Integrated Terminal

Press `Ctrl+` ` (backtick) or go to Terminal > New Terminal

#### 3.2 Navigate to Backend

```bash
cd backend
```

#### 3.3 Create Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
```

**Linux/Mac:**
```bash
python3 -m venv .venv
```

#### 3.4 Activate Virtual Environment

**Windows (PowerShell):**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
.venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

You should see `(.venv)` appear in your terminal prompt.

#### 3.5 Install Python Dependencies

```bash
pip install -r requirements.txt
```

This will take 2-5 minutes. It installs:
- FastAPI (backend framework)
- PyTorch (deep learning)
- Qiskit (quantum computing)
- scikit-learn (classical ML)
- FAISS (vector database)
- And more...

#### 3.6 Configure Environment Variables

```bash
# Copy example file
cp ../.env.example ../.env

# Open .env file in VS Code
code ../.env
```

**Edit the `.env` file and add your API key:**

```bash
# Option 1: Use Groq (Fast & Free)
XAI_API_KEY=gsk_your_actual_key_here

# Option 2: Use Google Gemini
GEMINI_API_KEY=your_actual_gemini_key_here
```

**Where to get API keys:**
- **Groq**: [console.groq.com](https://console.groq.com) → Sign up → API Keys → Create Key
- **Gemini**: [aistudio.google.com](https://aistudio.google.com) → Get API Key

#### 3.7 Build Knowledge Base (First Time Only)

```bash
# Make sure you're in backend directory with activated venv
python scripts/build_knowledge_index.py
```

This creates a FAISS vector index from medical documents (~30 seconds).

**Move index files to correct location:**

**Windows (PowerShell):**
```powershell
Move-Item -Path ../data/knowledge/index/* -Destination data/knowledge/index/ -Force
```

**Linux/Mac:**
```bash
mv ../data/knowledge/index/* data/knowledge/index/
```

#### 3.8 Start Backend Server

```bash
python -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

**You should see:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     FAISS index loaded: 22 vectors
INFO:     Intelligence layer fully operational
```

✅ **Backend is now running!** Keep this terminal open.

---

### 4. Frontend Setup (New Terminal)

#### 4.1 Open New Terminal

Click the `+` button in terminal panel or press `Ctrl+Shift+` `

#### 4.2 Navigate to Frontend

```bash
cd frontend
```

#### 4.3 Install Node Dependencies

```bash
npm install
```

This will take 1-3 minutes. It installs:
- React (UI framework)
- Vite (build tool)
- Framer Motion (animations)
- And more...

#### 4.4 Start Development Server

```bash
npm run dev
```

**You should see:**
```
VITE v5.x.x  ready in XXX ms

➜  Local:   http://localhost:5174/
➜  Network: use --host to expose
```

✅ **Frontend is now running!** Keep this terminal open too.

---

### 5. Access the Application

Open your browser and go to:

```
http://localhost:5174
```

You should see the Q-MedTriage landing page!

---

## Daily Workflow (After Initial Setup)

### Starting the Application

**Terminal 1 - Backend:**
```bash
cd backend
.\.venv\Scripts\Activate.ps1  # Windows
# source .venv/bin/activate    # Linux/Mac
python -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Browser:**
```
http://localhost:5174
```

### Stopping the Application

Press `Ctrl+C` in each terminal to stop the servers.

---

## Troubleshooting

### Python Virtual Environment Issues

**Problem:** `Activate.ps1 is not digitally signed`

**Solution (Windows):**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Backend Won't Start

**Check:**
1. Is `.env` file configured with API key?
2. Is virtual environment activated? (should see `(.venv)` in terminal)
3. Are all dependencies installed? Run `pip install -r requirements.txt` again
4. Is port 8000 already in use? Close other applications or use different port

### Frontend Won't Start

**Check:**
1. Is Node.js installed? Run `node --version` (should be 18+)
2. Are dependencies installed? Run `npm install` again
3. Is port 5174 already in use? Vite will auto-increment to 5175, 5176, etc.

### Q&A Service Unavailable

**Problem:** "The Q&A service is currently unavailable"

**Solutions:**
1. Check `.env` has valid API key (XAI_API_KEY or GEMINI_API_KEY)
2. Rebuild knowledge index:
   ```bash
   cd backend
   python scripts/build_knowledge_index.py
   ```
3. Ensure index files are in `backend/data/knowledge/index/`
4. Restart backend server

### Module Not Found Errors

**Solution:**
```bash
# Make sure virtual environment is activated
cd backend
.\.venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt
```

---

## VS Code Tips

### Python Interpreter

1. Press `Ctrl+Shift+P`
2. Type "Python: Select Interpreter"
3. Choose `.venv` interpreter from backend folder

### Multiple Terminals

- **Split terminals**: Click split icon in terminal panel
- **Rename terminals**: Right-click terminal tab → Rename
  - Name one "Backend" and one "Frontend" for clarity

### Debugging

**Backend (Python):**
1. Set breakpoints by clicking left of line numbers
2. Press `F5` → Select "Python File"
3. Debug features work automatically

**Frontend (React):**
1. Install "Debugger for Chrome" extension
2. Use browser DevTools (F12) for React debugging

---

## Project Structure in VS Code

```
Q-MedTriage/
├── .env                    ← Your API keys (DO NOT COMMIT)
├── .env.example           ← Template for environment variables
├── README.md              ← Main documentation
├── VSCODE_SETUP.md        ← This file
│
├── backend/               ← Python FastAPI backend
│   ├── .venv/            ← Virtual environment (created by you)
│   ├── src/              ← Source code
│   ├── tests/            ← Test files
│   ├── scripts/          ← Utility scripts
│   ├── requirements.txt  ← Python dependencies
│   └── data/             ← Knowledge base
│
└── frontend/              ← React + Vite frontend
    ├── node_modules/     ← Node dependencies (created by npm)
    ├── src/              ← Source code
    ├── public/           ← Static assets
    └── package.json      ← Node dependencies list
```

---

## Next Steps

1. ✅ **Upload a chest X-ray** to test the system
2. 📚 **Read full documentation** in `README.md`
3. 🧪 **Run tests**: `cd backend && pytest tests/ -v`
4. 🎨 **Customize the frontend** in `frontend/src/`
5. 🔬 **Explore quantum SVM** in `backend/src/quantum/`

---

## Getting Help

- **Documentation**: See `README.md` for full details
- **API Documentation**: Visit `http://localhost:8000/docs` when backend is running
- **Issues**: Check error messages in terminal output
- **Logs**: Backend shows detailed logs in terminal

---

**Happy Coding! 🚀**
