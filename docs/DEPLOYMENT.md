# Q-MedTriage Deployment Guide

Complete guide for deploying Q-MedTriage frontend and backend to production.

---

## 🎯 Deployment Architecture

```
Frontend (Vercel/Netlify)
    ↓ API calls
Backend (Railway/Render/AWS/Heroku)
    ↓ Dependencies
External Services:
  - Groq API (LLM)
  - Model files (S3/Cloud Storage)
```

---

## 📦 Part 1: Backend Deployment

### Option A: Railway (Recommended - Easiest)

**Why Railway?**
- Free tier available
- Automatic HTTPS
- Easy Python deployment
- Good for ML apps

**Steps:**

1. **Prepare Backend for Deployment**

Create `backend/railway.json`:
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn src.api.main:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

Create `backend/runtime.txt`:
```
python-3.14.4
```

Create `backend/Procfile`:
```
web: uvicorn src.api.main:app --host 0.0.0.0 --port $PORT
```

2. **Upload Models to Cloud Storage**

Railway has limited storage. Upload models to S3/Google Cloud Storage:

```bash
# Example with AWS S3
aws s3 cp models/ s3://your-bucket/models/ --recursive
```

Update `backend/src/config.py` to download models at startup:
```python
import os
import boto3
from pathlib import Path

def download_models():
    if os.getenv("RAILWAY_ENVIRONMENT"):  # In production
        s3 = boto3.client('s3')
        models_dir = Path("models")
        models_dir.mkdir(exist_ok=True)
        
        s3.download_file('your-bucket', 'models/pca_reducer.pkl', 'models/pca_reducer.pkl')
        s3.download_file('your-bucket', 'models/classical_svm.pkl', 'models/classical_svm.pkl')
        s3.download_file('your-bucket', 'models/quantum_svm.pkl', 'models/quantum_svm.pkl')
```

3. **Deploy to Railway**

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
cd backend
railway init

# Add environment variables
railway variables set XAI_API_KEY="your-groq-api-key"
railway variables set XAI_MODEL="openai/gpt-oss-120b"
railway variables set INTELLIGENCE_ENABLED="true"
railway variables set AWS_ACCESS_KEY_ID="your-aws-key"
railway variables set AWS_SECRET_ACCESS_KEY="your-aws-secret"

# Deploy
railway up
```

4. **Get Backend URL**
```bash
railway domain
# Example: https://qmedtriage-backend-production.up.railway.app
```

---

### Option B: Render

**Why Render?**
- Free tier available
- Automatic SSL
- Good Python support

**Steps:**

1. **Create `backend/render.yaml`**:
```yaml
services:
  - type: web
    name: qmedtriage-backend
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn src.api.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.14.4
      - key: XAI_API_KEY
        sync: false
      - key: XAI_MODEL
        value: openai/gpt-oss-120b
      - key: INTELLIGENCE_ENABLED
        value: true
```

2. **Deploy via Render Dashboard**:
   - Go to https://render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Select `backend` as root directory
   - Add environment variables
   - Deploy!

3. **Note Backend URL**: `https://qmedtriage-backend.onrender.com`

---

### Option C: AWS EC2 (Most Control)

**For Production/Scalability**

1. **Launch EC2 Instance**:
   - Ubuntu 22.04 LTS
   - t3.medium or larger (ML models need RAM)
   - Open ports: 80, 443, 22

2. **Setup Script** (`deploy-ec2.sh`):
```bash
#!/bin/bash
# SSH into EC2 and run this

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.14
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt install python3.14 python3.14-venv python3.14-dev -y

# Install nginx
sudo apt install nginx -y

# Clone repo
git clone <your-repo-url>
cd Q-MedTriage/backend

# Create venv
python3.14 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn

# Create systemd service
sudo tee /etc/systemd/system/qmedtriage.service > /dev/null <<EOF
[Unit]
Description=Q-MedTriage Backend
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/Q-MedTriage/backend
Environment="PATH=/home/ubuntu/Q-MedTriage/backend/venv/bin"
ExecStart=/home/ubuntu/Q-MedTriage/backend/venv/bin/gunicorn src.api.main:app -w 2 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000

[Install]
WantedBy=multi-user.target
EOF

# Configure nginx
sudo tee /etc/nginx/sites-available/qmedtriage > /dev/null <<EOF
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
        client_max_body_size 50M;
    }
}
EOF

sudo ln -s /etc/nginx/sites-available/qmedtriage /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Start service
sudo systemctl daemon-reload
sudo systemctl enable qmedtriage
sudo systemctl start qmedtriage

# Setup SSL with Let's Encrypt
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

---

### Option D: Heroku

**Steps:**

1. **Create `backend/Procfile`**:
```
web: uvicorn src.api.main:app --host 0.0.0.0 --port $PORT
```

2. **Deploy**:
```bash
# Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

cd backend
heroku create qmedtriage-backend

# Set environment variables
heroku config:set XAI_API_KEY="your-key"
heroku config:set XAI_MODEL="openai/gpt-oss-120b"

# Deploy
git subtree push --prefix backend heroku main

# Or use container deployment for models
heroku container:push web
heroku container:release web
```

---

## 🎨 Part 2: Frontend Deployment

### Option A: Vercel (Recommended)

**Why Vercel?**
- Built for React/Vite
- Automatic deployments
- Free tier generous
- Fast global CDN

**Steps:**

1. **Update Frontend Environment**

Edit `frontend/.env.production`:
```env
VITE_API_URL=https://your-backend-url.railway.app
```

2. **Deploy via Vercel CLI**

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy from frontend directory
cd frontend
vercel

# Follow prompts:
# - Project name: qmedtriage-frontend
# - Framework: Vite
# - Build command: npm run build
# - Output directory: dist

# Deploy to production
vercel --prod
```

3. **Deploy via GitHub (Easier)**

   - Go to https://vercel.com
   - Click "Add New Project"
   - Import your GitHub repository
   - Configure:
     - **Framework Preset**: Vite
     - **Root Directory**: `frontend`
     - **Build Command**: `npm run build`
     - **Output Directory**: `dist`
     - **Environment Variables**:
       - `VITE_API_URL` = `https://your-backend-url.railway.app`
   - Click "Deploy"

4. **Get Frontend URL**: `https://qmedtriage.vercel.app`

---

### Option B: Netlify

**Steps:**

1. **Create `frontend/netlify.toml`**:
```toml
[build]
  command = "npm run build"
  publish = "dist"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[build.environment]
  NODE_VERSION = "18"
```

2. **Deploy**:
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login
netlify login

# Deploy
cd frontend
netlify deploy --prod

# Or via GitHub:
# - Go to netlify.com
# - Import repository
# - Set root directory: frontend
# - Build command: npm run build
# - Publish directory: dist
```

---

### Option C: Cloudflare Pages

**Steps:**

1. **Via Dashboard**:
   - Go to https://pages.cloudflare.com
   - Connect GitHub repository
   - Configure:
     - **Build command**: `npm run build`
     - **Build output**: `dist`
     - **Root directory**: `frontend`
     - **Environment variable**: `VITE_API_URL`

2. **Deploy**:
```bash
npm install -g wrangler
wrangler login
cd frontend
wrangler pages deploy dist
```

---

## 🔐 Part 3: Environment Variables

### Backend Environment Variables

Set these in your deployment platform:

```env
# Required
XAI_API_KEY=gsk_your_groq_api_key_here
XAI_MODEL=openai/gpt-oss-120b
INTELLIGENCE_ENABLED=true

# Optional
XAI_MAX_TOKENS=1000
XAI_TEMPERATURE=0.3
RAG_TOP_K=5
EMBEDDING_MODEL=all-MiniLM-L6-v2

# AWS (if using S3 for models)
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=us-east-1
S3_BUCKET_NAME=qmedtriage-models
```

### Frontend Environment Variables

Set these in Vercel/Netlify:

```env
# Required
VITE_API_URL=https://your-backend-url.railway.app

# Optional (for analytics)
VITE_ANALYTICS_ID=your_analytics_id
```

---

## 📊 Part 4: Handle Large Model Files

ML models are too large for Git/free hosting. Solutions:

### Option 1: AWS S3 (Recommended)

**Upload models:**
```bash
aws s3 cp backend/models/ s3://qmedtriage-models/models/ --recursive
```

**Download at startup** - Add to `backend/src/api/main.py`:
```python
import boto3
import os
from pathlib import Path

@app.on_event("startup")
async def download_models():
    if os.getenv("RAILWAY_ENVIRONMENT") or os.getenv("RENDER"):
        print("Downloading models from S3...")
        s3 = boto3.client('s3')
        models_dir = Path("models")
        models_dir.mkdir(exist_ok=True)
        
        models = ["pca_reducer.pkl", "classical_svm.pkl", "quantum_svm.pkl"]
        for model in models:
            s3.download_file(
                os.getenv("S3_BUCKET_NAME"),
                f"models/{model}",
                f"models/{model}"
            )
        print("Models downloaded!")
```

### Option 2: Google Cloud Storage

```python
from google.cloud import storage

def download_from_gcs():
    client = storage.Client()
    bucket = client.bucket('qmedtriage-models')
    
    for model in ["pca_reducer.pkl", "classical_svm.pkl", "quantum_svm.pkl"]:
        blob = bucket.blob(f"models/{model}")
        blob.download_to_filename(f"models/{model}")
```

### Option 3: Git LFS (Limited Free Tier)

```bash
# Install Git LFS
git lfs install

# Track model files
git lfs track "*.pkl"
git add .gitattributes

# Commit and push
git add backend/models/*.pkl
git commit -m "Add models with LFS"
git push
```

---

## 🔍 Part 5: CORS Configuration

Update `backend/src/api/main.py` for production:

```python
from fastapi.middleware.cors import CORSMiddleware
import os

# Get allowed origins from environment
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5174,https://qmedtriage.vercel.app"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,  # Production domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Set `ALLOWED_ORIGINS` environment variable in Railway/Render:
```
ALLOWED_ORIGINS=https://qmedtriage.vercel.app,https://qmedtriage.netlify.app
```

---

## 🧪 Part 6: Pre-Deployment Checklist

### Backend Checklist

- [ ] Models uploaded to cloud storage (S3/GCS)
- [ ] Environment variables configured
- [ ] `requirements.txt` up to date
- [ ] CORS configured for frontend domain
- [ ] Health check endpoint working: `/health`
- [ ] API key (XAI_API_KEY) is valid
- [ ] Test backend locally first
- [ ] Remove debug/development flags

### Frontend Checklist

- [ ] `VITE_API_URL` points to production backend
- [ ] Build succeeds locally: `npm run build`
- [ ] Test production build: `npm run preview`
- [ ] Remove console.logs
- [ ] Update meta tags in `index.html`
- [ ] Add favicon and social preview images
- [ ] Test on mobile devices

---

## 🚀 Part 7: Complete Deployment Flow

### Step-by-Step Deployment

**1. Deploy Backend First**

```bash
# Railway example
cd backend

# Test locally
python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000

# Deploy
railway init
railway up
railway domain  # Get your backend URL

# Example output: https://qmedtriage-backend-production.up.railway.app
```

**2. Update Frontend Config**

```bash
cd ../frontend

# Create production env file
echo "VITE_API_URL=https://qmedtriage-backend-production.up.railway.app" > .env.production

# Test build
npm run build
npm run preview  # Test production build locally
```

**3. Deploy Frontend**

```bash
# Vercel
vercel --prod

# Or GitHub: Push to main branch, Vercel auto-deploys
git add .
git commit -m "Configure production backend URL"
git push origin main
```

**4. Verify Deployment**

- Frontend: https://qmedtriage.vercel.app
- Backend: https://qmedtriage-backend-production.up.railway.app/health

Test the flow:
1. Open frontend
2. Upload a chest X-ray
3. Check prediction works
4. Verify explanation loads

---

## 💰 Cost Estimates

### Free Tier Options

| Service | Free Tier | Limits |
|---------|-----------|--------|
| **Vercel** (Frontend) | Yes | 100GB bandwidth/month |
| **Railway** (Backend) | $5 credit/month | ~500 hours |
| **Render** (Backend) | Yes | Sleeps after 15min inactive |
| **Groq API** | Yes | 14,400 requests/day |
| **AWS S3** (Models) | 5GB free | First year |

**Total Free Tier**: $0/month (with limitations)

### Paid Tiers (Recommended for Production)

| Service | Cost | Specs |
|---------|------|-------|
| **Vercel Pro** | $20/month | Unlimited sites |
| **Railway** | ~$10-30/month | 8GB RAM, 2 vCPU |
| **AWS S3** | ~$1/month | 10GB storage |
| **Groq API** | Pay-as-you-go | ~$0.10/1M tokens |

**Total Estimated**: $30-50/month

---

## 🐛 Common Deployment Issues

### Issue 1: "Module not found" errors

**Solution**: Ensure `requirements.txt` includes all dependencies:
```bash
cd backend
pip freeze > requirements.txt
```

### Issue 2: Models not loading

**Solution**: Check model paths are relative:
```python
# backend/src/config.py
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"
```

### Issue 3: CORS errors

**Solution**: Add frontend domain to CORS:
```python
allow_origins=["https://qmedtriage.vercel.app"]
```

### Issue 4: Frontend can't connect to backend

**Solution**: Check `VITE_API_URL` in frontend:
```bash
# Vercel dashboard → Project → Settings → Environment Variables
VITE_API_URL = https://your-backend.railway.app
```

### Issue 5: Out of memory on backend

**Solution**: 
- Upgrade to larger instance (Railway: $10/month for 2GB RAM)
- Or reduce model size / use model quantization
- Or lazy-load quantum model only when needed

---

## 📈 Monitoring & Maintenance

### Setup Monitoring

**Railway/Render**: Built-in monitoring dashboard

**Custom Monitoring**:
```python
# backend/src/api/main.py
from prometheus_fastapi_instrumentator import Instrumentator

@app.on_event("startup")
async def startup():
    Instrumentator().instrument(app).expose(app)
```

### Health Checks

Add health check endpoint (already exists):
```python
@app.get("/health")
async def health():
    return {
        "api": "online",
        "vision_model": "ready" if inference_pipeline else "offline",
        "intelligence_enabled": INTELLIGENCE_ENABLED
    }
```

Configure uptime monitoring:
- Uptime Robot (free): https://uptimerobot.com
- Better Uptime: https://betteruptime.com
- Pingdom: https://www.pingdom.com

---

## 🔒 Security Best Practices

1. **Never commit `.env` files**
   ```bash
   # Already in .gitignore
   .env
   *.env
   ```

2. **Use environment variables for all secrets**
   ```python
   API_KEY = os.getenv("XAI_API_KEY")  # ✓ Good
   API_KEY = "gsk_hardcoded"  # ✗ Bad
   ```

3. **Enable HTTPS only** (automatic on Vercel/Railway)

4. **Rate limiting** (optional):
   ```python
   from slowapi import Limiter
   
   limiter = Limiter(key_func=get_remote_address)
   
   @app.post("/predict")
   @limiter.limit("10/minute")
   async def predict(...):
       ...
   ```

5. **Input validation** (already implemented in FastAPI)

---

## 📝 Deployment Summary

**Quick Deploy Commands:**

```bash
# 1. Backend (Railway)
cd backend
railway login
railway init
railway up
railway domain  # Copy this URL

# 2. Frontend (Vercel)
cd ../frontend
echo "VITE_API_URL=<railway-url-from-above>" > .env.production
vercel login
vercel --prod

# Done! 🎉
```

**Your URLs:**
- Frontend: `https://qmedtriage.vercel.app`
- Backend: `https://qmedtriage-backend.up.railway.app`
- API Docs: `https://qmedtriage-backend.up.railway.app/docs`

---

## 🆘 Need Help?

- Railway Docs: https://docs.railway.app
- Vercel Docs: https://vercel.com/docs
- FastAPI Deployment: https://fastapi.tiangolo.com/deployment/
- Join Discord/Slack for support

---

**Last Updated**: 2026-08-27  
**Version**: 1.0
