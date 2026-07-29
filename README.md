# AI Medical Report Assistant

An enterprise-grade, production-inspired AI solution designed for multimodal medical report interpretation, including Blood Test PDFs (OCR + Rule Engine), Brain MRI scans (4-class PyTorch ConvNext tiny classification + Grad-CAM), and Chest X-Ray scans (Binary Pneumonia detection + Grad-CAM).

> [!IMPORTANT]
> **Educational & Non-Diagnostic Disclaimer**: This system is designed as an educational tool for academic demonstration and research. It does **not** provide medical diagnoses or prescribe treatment plans. All outputs are paired with educational disclaimers.

---

## 🌟 Tech Stack Overview

* **Frontend**: React 18, Vite, Tailwind CSS, Axios, React Router v6, Chart.js / React-Chartjs-2, Lucide Icons.
* **Backend**: FastAPI (Python 3.11+), SQLAlchemy 2.0 ORM, Pydantic v2, PostgreSQL, Alembic, PyJWT, Passlib (Bcrypt).
* **AI & Machine Learning**: PyTorch, torchvision, EasyOCR, pdfplumber, Grad-CAM.
* **DevOps**: Docker, Docker Compose.

---

## 📁 Repository Structure

```
ai-medical-report-assistant/
├── backend/                  # FastAPI Application Server
│   ├── app/
│   │   ├── api/v1/          # REST Endpoint Routers & Handlers
│   │   ├── core/            # Config, Security, DB Connection & Logging
│   │   ├── models/          # SQLAlchemy ORM Models (Users, Reports, ChatHistory)
│   │   ├── schemas/         # Pydantic Request/Response DTOs
│   │   ├── services/        # OCR, ML Inferences, Rule Engine & Health Assistant
│   │   └── ml_weights/      # Pretrained PyTorch .pt Model Artifacts
│   ├── alembic/             # Database Migration Scripts
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                 # React 18 + Vite Single Page Application
│   ├── src/
│   │   ├── components/      # Modular UI Components & Layouts
│   │   ├── context/         # Auth & Global Context Providers
│   │   ├── pages/           # Application Router Views
│   │   └── services/        # Axios API Client Interceptors & Endpoints
│   ├── Dockerfile
│   └── package.json
├── training/                 # Offline PyTorch Training Pipelines
│   ├── brain_mri/           # 4-Class Brain MRI Training Scripts
│   ├── chest_xray/          # Binary Chest X-Ray Training Scripts
│   └── blood_parser/        # Biomarker Standard Reference Datasets
├── datasets/                 # Local Training & Validation Image Datasets
├── evaluation/               # Model Evaluation Suite (Confusion Matrix, Metrics, Plots)
└── docker-compose.yml        # Orchestration Blueprint
```

---

## 🚀 Quick Start Guide

### Prerequisites
* Python 3.11+
* Node.js 18+ & npm
* PostgreSQL 15+ (or Docker)

### 1. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure Environment
cp .env.example .env

# Run Database Migrations
alembic upgrade head

# Start FastAPI Dev Server
uvicorn app.main:app --reload --port 8000
```
Backend API interactive documentation available at: `http://localhost:8000/docs`

### 2. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start Vite Dev Server
npm run dev
```
Frontend Web UI available at: `http://localhost:5173`

---

## 🐳 Docker Deployment
To launch PostgreSQL, FastAPI Backend, and React Frontend simultaneously via Docker Compose:
```bash
docker-compose up --build
```
