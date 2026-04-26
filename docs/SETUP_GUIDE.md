# AI Healthcare Chatbot Platform - Complete Setup Guide

## 🏥 Project Overview

A production-ready, hackathon-winning AI healthcare chatbot platform featuring:
- **LLaMA 3** via Groq API for conversational AI
- **BioBERT** for medical entity recognition
- **AES-256 Encryption** for secure data storage
- **Reinforcement Learning** feedback system
- **Modern React Dashboard** with Tailwind CSS & Framer Motion
- **MongoDB Atlas** for cloud database

---

## 📋 Prerequisites

### System Requirements
- **Python 3.10+**
- **Node.js 18+** and npm
- **Git**
- **pip** (Python package manager)

### Required Accounts (All Free)
1. **Groq API** (for LLaMA 3)
   - Sign up: https://console.groq.com
   - Get free API key with rate limits

2. **MongoDB Atlas** (Free Tier)
   - Sign up: https://www.mongodb.com/cloud/atlas
   - Create a free cluster
   - Get connection string

3. **HuggingFace** (for BioBERT)
   - Sign up: https://huggingface.co/join
   - Get API token for model access

---

## ⚙️ BACKEND SETUP

### Step 1: Clone and Navigate to Backend

```bash
cd backend
```

### Step 2: Create Python Virtual Environment

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**If you encounter issues, install individually:**
```bash
pip install fastapi uvicorn pymongo cryptography python-dotenv
pip install langchain langchain-groq langchain-community
pip install transformers torch numpy
pip install httpx requests pydantic
```

### Step 4: Setup Environment Variables

Create `.env` file in the `backend` folder:

```bash
# Copy from .env.example
cp .env.example .env
```

Edit `.env` and fill in your API keys:

```env
# 1. Get from https://console.groq.com
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# 2. Get from https://huggingface.co/settings/tokens
HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# 3. Get from MongoDB Atlas (Connection String)
# Format: mongodb+srv://username:password@cluster.mongodb.net/healthcare
MONGODB_URI=mongodb+srv://your_user:your_password@cluster.mongodb.net/healthcare

# 4. Generate encryption key:
# python -c "import os; print(os.urandom(32).hex())"
ENCRYPTION_KEY=your_32_byte_hex_key_here

# Server settings
DEBUG=True
PORT=8000
HOST=0.0.0.0
```

### Step 5: Generate Encryption Key

```bash
python -c "import os; print('ENCRYPTION_KEY=' + os.urandom(32).hex())"
```

Copy the output to your `.env` file.

### Step 6: Test Backend

```bash
python -m uvicorn app.main:app --reload
```

**Output should show:**
```
✓ Connected to MongoDB
✓ LLM Service initialized
✓ BioBERT Service initialized
✓ All services initialized successfully!
```

**Test the API:**
- Open browser: http://localhost:8000/health
- API Docs: http://localhost:8000/docs
- Chat endpoint: http://localhost:8000/chat

---

## 🎨 FRONTEND SETUP

### Step 1: Navigate to Frontend

```bash
cd ../frontend
```

### Step 2: Install Dependencies

```bash
npm install
```

### Step 3: Configure Backend URL (Optional)

Edit `src/api/apiClient.js` and set your backend URL:

```javascript
const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';
```

Or create `.env`:

```env
VITE_API_URL=http://localhost:8000
```

### Step 4: Start Development Server

```bash
npm run dev
```

**Output:**
```
  VITE v5.0.0  ready in 500 ms

  ➜  Local:   http://localhost:3000/
  ➜  press h to show help
```

Open http://localhost:3000 in your browser!

---

## 🚀 RUNNING THE COMPLETE SYSTEM

### Terminal 1: Backend
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python -m uvicorn app.main:app --reload
```

### Terminal 2: Frontend
```bash
cd frontend
npm run dev
```

### Terminal 3: (Optional) MongoDB Monitor
```bash
# Check MongoDB connection is working
mongo "your_mongodb_uri"
```

---

## 🔑 Getting API Keys - Detailed Steps

### 1. Groq API Key (LLaMA 3)

1. Go to https://console.groq.com/login
2. Sign up or login with Google/GitHub
3. Go to **API Keys** section
4. Click **Create API Key**
5. Copy the key to `.env` as `GROQ_API_KEY`

### 2. MongoDB Connection String

1. Go to https://www.mongodb.com/cloud/atlas
2. Sign up for free account
3. Create a **New Project**
4. Create a **New Cluster** (M0 Free tier)
5. Click **Connect**
6. Select **Drivers** → Python 3.10+
7. Copy connection string
8. Replace `<username>`, `<password>`, and database name in URL
9. Save as `MONGODB_URI` in `.env`

Example:
```
MONGODB_URI=mongodb+srv://admin:SecurePassword123@cluster.mongodb.net/healthcare
```

### 3. HuggingFace API Token

1. Go to https://huggingface.co/join
2. Create account
3. Go to **Settings** → **Access Tokens**
4. Create **New token** (read only is fine)
5. Copy to `.env` as `HUGGINGFACE_API_KEY`

---

## 🧪 Testing the System

### Test Chat Functionality

```bash
# Terminal with backend running

# Test 1: Health check
curl http://localhost:8000/health

# Test 2: Send message
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"content": "I have a fever and cough", "user_id": "test_user"}'

# Test 3: Get history
curl -X POST "http://localhost:8000/history" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_user", "limit": 10}'
```

### Test Encryption

```python
# Create test_encryption.py
from app.utils.encryption import EncryptionService

encryption = EncryptionService("your-32-byte-key-here")
plaintext = "This is sensitive health data"
encrypted = encryption.encrypt(plaintext)
decrypted = encryption.decrypt(encrypted)

print(f"Original: {plaintext}")
print(f"Encrypted: {encrypted}")
print(f"Decrypted: {decrypted}")
assert plaintext == decrypted
print("✓ Encryption working!")
```

Run:
```bash
python test_encryption.py
```

---

## 📊 Features Walkthrough

### Chat Tab
1. Type symptoms or health questions
2. AI responds with healthcare recommendations
3. Rate responses with 👍 👎 buttons
4. System learns from feedback

### Health Insights Tab
1. View symptom frequency charts
2. See predicted conditions
3. Track response feedback trends
4. Monitor learning progress

### Security Tab
1. View encryption status (AES-256 enabled)
2. Check database security
3. Review privacy policy
4. Understand data handling

### Settings Tab
1. Toggle dark mode
2. Manage data retention (7-90 days)
3. Clear chat history
4. View account information

---

## 🔒 Security Checklist

- [ ] Encryption key is 32 bytes
- [ ] API keys stored in `.env` (not committed)
- [ ] MongoDB has strong password
- [ ] CORS origins configured properly
- [ ] HTTPS enabled in production
- [ ] No sensitive data in logs
- [ ] Rate limiting enabled
- [ ] Input validation implemented

---

## 🐛 Troubleshooting

### Backend won't start
```
Error: ModuleNotFoundError: No module named 'transformers'
Solution: pip install transformers torch
```

### MongoDB connection failed
```
Error: ServerSelectionTimeoutError
Solution: 
1. Check connection string in .env
2. Whitelist your IP in MongoDB Atlas
3. Verify database exists
```

### Frontend can't reach backend
```
Error: CORS error
Solution:
1. Backend must be running on http://localhost:8000
2. Check CORS settings in app/main.py
3. Update API_BASE in apiClient.js
```

### Encryption errors
```
Error: Decryption failed
Solution:
1. Ensure ENCRYPTION_KEY is consistent
2. Don't modify encrypted data
3. Regenerate ENCRYPTION_KEY if lost
```

---

## 📦 Project Structure

```
aihealthcare/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app
│   │   ├── config.py            # Configuration
│   │   ├── models/
│   │   │   └── schemas.py       # Pydantic models
│   │   ├── services/
│   │   │   ├── llm_service.py   # LLaMA 3 integration
│   │   │   ├── biobert_service.py # BioBERT
│   │   │   └── rl_learning.py   # RL feedback system
│   │   ├── utils/
│   │   │   ├── encryption.py    # AES-256
│   │   │   └── database.py      # MongoDB
│   │   └── routes/              # API routes
│   ├── main.py                  # Entry point
│   ├── requirements.txt         # Python dependencies
│   └── .env.example            # Environment template
│
├── frontend/
│   ├── src/
│   │   ├── main.jsx            # React entry
│   │   ├── App.jsx             # Main component
│   │   ├── index.css           # Tailwind + custom CSS
│   │   ├── api/
│   │   │   └── apiClient.js    # API calls
│   │   ├── store/
│   │   │   └── store.js        # Zustand state
│   │   └── pages/
│   │       ├── ChatTab.jsx
│   │       ├── InsightsTab.jsx
│   │       ├── SecurityTab.jsx
│   │       └── SettingsTab.jsx
│   ├── index.html              # HTML template
│   ├── package.json            # NPM dependencies
│   ├── vite.config.js          # Vite config
│   ├── tailwind.config.js      # Tailwind config
│   └── postcss.config.js       # PostCSS config
│
└── README.md                    # This file
```

---

## Next Steps

1. **Local Testing**: Ensure everything runs on localhost
2. **Backend Deployment**: Deploy to Render/Railway
3. **Frontend Deployment**: Deploy to Vercel
4. **Domain Setup**: Add custom domain
5. **Monitoring**: Set up error tracking
6. **Scaling**: Optimize for production load

See `DEPLOYMENT.md` for detailed deployment instructions.

---

## 📚 API Documentation

API docs available at: **http://localhost:8000/docs**

### Key Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/chat` | POST | Send message and get response |
| `/feedback` | POST | Submit feedback on response |
| `/history` | POST | Get chat history |
| `/insights` | GET | Get health insights |
| `/security/status` | GET | Check security status |
| `/rl-stats` | GET | Get RL learning stats |
| `/settings` | GET | Get user settings |

---

## 📞 Support

For issues or questions:
1. Check troubleshooting section above
2. Review API logs: `http://localhost:8000/docs`
3. Check database connection
4. Verify all API keys are valid

---

## ⚖️ Medical Disclaimer

**This application is for educational and informational purposes only.**

- NOT a replacement for professional medical advice
- DO NOT use for diagnosing medical conditions
- ALWAYS consult qualified healthcare providers
- In emergencies, call 911 or your local emergency number

---

## 📄 License

This project is provided as-is for educational purposes.

---

## 🎉 Enjoy Your AI Healthcare Platform!

Built with ❤️ for healthcare innovation.
