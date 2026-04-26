# 🏥 AI Healthcare Chatbot

A full-stack, production-ready AI healthcare assistant that provides intelligent medical symptom analysis, health insights, and conversational guidance using advanced LLMs.

## 🌟 Features

* **Intelligent Conversational AI:** Powered by LLaMA 3 (via Groq) for natural, contextual, and empathetic health discussions.
* **Medical NLP:** Integrates BioBERT (via Hugging Face) for accurate medical entity recognition and symptom detection.
* **Secure & Private:** AES-256 encryption ensures all user data and chat history remain completely confidential.
* **Modern Frontend:** Responsive UI built with React, Tailwind CSS, and Framer Motion.
* **Robust Backend:** High-performance FastAPI server with a MongoDB database.

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd aihealthcare
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv

# Activate virtual environment
# On Windows: venv\Scripts\activate
# On Mac/Linux: source venv/bin/activate

pip install -r requirements.txt

# Setup Environment Variables
cp .env.example .env
# Edit .env to add your GROQ_API_KEY and HUGGINGFACE_API_KEY
```

### 3. Frontend Setup
Open a new terminal window:
```bash
cd frontend
npm install
```

### 4. Run the Application
**Start the backend (Terminal 1):**
```bash
cd backend
python -m uvicorn app.main:app --reload
```

**Start the frontend (Terminal 2):**
```bash
cd frontend
npm run dev
```

Visit `http://localhost:3000` to start chatting!

## 🔐 Security & API Keys

This project uses strict environment variables to keep API keys secure. **Never commit your `.env` file to version control.**
* Obtain a free Groq API Key for LLaMA 3 capabilities.
* Obtain a free Hugging Face Token for BioBERT capabilities.