# AI Medical Report Assistant 
 
An enterprise-grade, production-inspired AI solution designed for multimodal medical report analysis, currently supporting **Blood Report Analysis** and **Brain MRI Classification**, with AI-powered educational interpretation. 
 
The platform combines OCR, rule-based medical parameter extraction, deep learning, generative AI, secure authentication, a PostgreSQL database, and a modern React frontend. 
 
> [!IMPORTANT] 
> **Educational & Non-Diagnostic Disclaimer**: This system is designed as an educational tool for academic demonstration and research. It does **not** provide medical diagnoses or prescribe treatment plans. All outputs are paired with educational disclaimers and should be reviewed by qualified healthcare professionals. 
 
--- 
 
## 🌟 Tech Stack Overview 
 
* **Frontend**: React, Vite, Tailwind CSS, Axios, React Router. 
* **Backend**: FastAPI, Python 3.11+, SQLAlchemy, Pydantic, PostgreSQL, JWT Authentication. 
* **AI & Machine Learning**: PyTorch, torchvision, ConvNeXt Tiny, EasyOCR, Google Gemini API. 
* **Computer Vision**: MRI image preprocessing, deep-learning image classification, OCR-based medical report processing. 
* **Database**: PostgreSQL with SQLAlchemy ORM. 
* **API Documentation**: FastAPI Swagger / OpenAPI. 
* **Version Control**: Git, GitHub. 
 
--- 
 
## 📁 Repository Structure 
 
```text
AI-Medical-Report-Assistant/ 
├── backend/                       # FastAPI Application Server 
│   ├── app/ 
│   │   ├── api/                  # REST API Routers & Endpoints 
│   │   ├── core/                 # Configuration, Security & Database 
│   │   ├── models/               # SQLAlchemy Database Models 
│   │   ├── schemas/              # Pydantic Request/Response Schemas 
│   │   ├── services/             # OCR, Blood Parser & AI Services 
│   │   └── ml/                   # Machine Learning Model Integration 
│   │ 
│   ├── ml_weights/ 
│   │   └── brain_mri/            # Brain MRI Model Weights 
│   │ 
│   ├── uploads/                  # Uploaded Report Files 
│   ├── requirements.txt 
│   └── .env.example 
│ 
├── frontend/                     # React + Vite Single Page Application 
│   ├── src/ 
│   │   ├── components/           # Reusable UI Components 
│   │   ├── context/              # Authentication & Global Context 
│   │   ├── pages/                # Application Pages 
│   │   └── services/             # Axios API Client & Endpoints 
│   │ 
│   ├── package.json 
│   └── vite.config.js 
│ 
└── README.md


🚀 Currently Implemented Modules
1.🩸 Blood Report Analyzer

The Blood Report Analyzer processes CBC (Complete Blood Count) reports using EasyOCR and a specialized rule-based parsing engine.
Blood Report
     │
     ▼
 File Upload
     │
     ▼
   EasyOCR
     │
     ▼
  OCR Text
     │
     ▼
 CBC Parser
     │
     ├── OCR Error Handling
     ├── Parameter Detection
     ├── Multiline Extraction
     ├── Unit Normalization
     ├── Scale Conversion
     └── Reference Range Detection
     │
     ▼
Normal / High / Low
     │
     ▼
  Gemini API
     │
     ▼
Educational AI Summary


2.🧠 Brain MRI Classifier

The Brain MRI module uses a fine-tuned ConvNeXt Tiny deep learning model to classify brain MRI scans into four categories.
Brain MRI
    │
    ▼
 File Upload
    │
    ▼
Image Preprocessing
    │
    ▼
 ConvNeXt Tiny
    │
    ├── Glioma
    ├── Meningioma
    ├── Pituitary Tumor
    └── No Tumor
    │
    ▼
Prediction + Confidence
    │
    ▼
Class Probability Distribution
    │
    ▼
 Gemini API
    │
    ▼
Educational AI Interpretation
🤖 Generative AI Interpretation

The system integrates the Google Gemini API to generate educational summaries from structured analysis results.

Blood Reports

Gemini receives:

Extracted CBC parameters
Normal / High / Low classifications
Reference ranges
Overall abnormality information
Brain MRI

Gemini receives:

Predicted class
Model confidence
Class probability distribution
Classification context

The generated output is designed to:

Explain results in understandable language
Highlight abnormal findings
Provide educational context
Summarize the analysis
Maintain a non-diagnostic medical boundary

🔐 Authentication

The application implements secure user authentication using JWT.

The authentication system provides:

User registration
User login
JWT access tokens
Protected backend endpoints
Protected React routes
Automatic Authorization header handling
Logout functionality


🌐 Frontend Application

The frontend is built using React + Vite and provides a modern clinical dashboard for interacting with the medical analysis modules.

Current Pages
/login
/register
/dashboard
/blood-report
/brain-mri
Dashboard

The dashboard provides access to:

🩸 Blood Report Analyzer
🧠 Brain MRI Classifier
Blood Report Interface

The Blood Report Analyzer interface includes:

Drag-and-drop upload
File validation
Upload progress
OCR processing status
CBC parsing status
AI interpretation status
Biomarker table
Reference ranges
Normal / High / Low indicators
Processing information
AI interpretation panel
Brain MRI Interface

The Brain MRI Classifier interface includes:

Drag-and-drop MRI upload
MRI image preview
Processing progress
Prediction result
Confidence percentage
Class probability visualization
AI interpretation panel
Medical disclaimer
🔌 REST API

The FastAPI backend provides REST APIs with interactive Swagger/OpenAPI documentation.

screenshots:
## 🖥️ Screenshots

### 🔐 Login Page

<img width="900" alt="Login Page" src="https://github.com/user-attachments/assets/2d616618-df9f-45bb-8fc3-863446dffd65" />

### 🏠 Dashboard

<img width="900" alt="Dashboard" src="https://github.com/user-attachments/assets/41627d8b-8c22-4182-88b4-099d9bc82197" />

### 🩸 Blood Report Analyzer

<img width="900" alt="Blood Report Analyzer" src="https://github.com/user-attachments/assets/2b746450-d598-4c14-8889-9e6382b5cd6f" />
















