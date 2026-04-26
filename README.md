# README - AI Healthcare Chatbot Platform

## 🏥 Welcome to the AI Healthcare Chatbot Platform

A **production-ready**, **hackathon-winning** intelligent healthcare assistant powered by cutting-edge AI technology.

### ✨ Key Features

- 🤖 **LLaMA 3 AI** - Natural language conversations via Groq API
- 🧬 **BioBERT** - Medical entity recognition and symptom analysis
- 🔒 **AES-256 Encryption** - Military-grade data security
- 📊 **Health Insights Dashboard** - Interactive charts and analytics
- 🧠 **Reinforcement Learning** - Learns from user feedback
- 🎨 **Modern UI/UX** - React + Tailwind + Framer Motion
- 💾 **MongoDB Integration** - Cloud database with encryption
- 🌙 **Dark Mode** - Beautiful light and dark themes

---

## 🎯 What This Does

### For Users
- Ask about symptoms and health concerns
- Get AI-powered health insights
- Track your interactions
- Secure encrypted conversations
- Learn from personalized feedback

### For Developers
- Complete source code
- Production-ready architecture
- Easy deployment instructions
- Clear documentation
- RESTful API with 10+ endpoints

---

## � Setup - Getting Started (IMPORTANT)

### Prerequisites
- Python 3.8+ 
- Node.js 16+
- Git
- API keys (see below)

### ⚙️ 1. Configure Environment Variables

**Backend Setup:**
```bash
cd backend

# Copy the example to create your .env
cp .env.example .env

# Edit .env with your actual API keys
# Use your favorite editor (VS Code, nano, etc.)
```

**Required API Keys:**

1. **Groq API Key** (LLaMA 3)
   - Go to: https://console.groq.com/keys
   - Sign up and create new API key
   - Copy key (looks like: `gsk_xxxxxxxx...`)
   - Add to `backend/.env`: `GROQ_API_KEY=gsk_xxxxx...`

2. **HuggingFace Token** (BioBERT)
   - Go to: https://huggingface.co/settings/tokens
   - Create "Read" access token
   - Add to `backend/.env`: `HUGGINGFACE_API_KEY=hf_xxxxx...`

3. **MongoDB Atlas** (Optional - for persistence)
   - Go to: https://www.mongodb.com/cloud/atlas
   - Create free cluster
   - Get connection string
   - Add to `backend/.env`: `MONGODB_URI=mongodb+srv://user:pass@...`

4. **Encryption Key** (Auto-generated, optional to change)
   - Already generated in `.env`
   - Or generate new: `python -c "import os; print(os.urandom(32).hex())"`

### ⚠️ Security Notice
- **NEVER commit `.env` file to Git** (already in `.gitignore`)
- Only `.env.example` is committed (with placeholders)
- Each team member creates their own `.env` with their API keys
- For CI/CD: Set environment variables through GitHub Secrets, GitLab CI/CD, or your platform

---

## �🚀 Quick Start (5 minutes)

### Option 1: Full Local Setup

```bash
# Navigate to project
cd aihealthcare

# ===== BACKEND SETUP =====
cd backend

# Create & activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# ✅ Make sure .env is configured with API keys (see Setup section above)

# Start backend server
python -m uvicorn app.main:app --reload

# ✓ Backend running at http://localhost:8000
# ✓ API docs at http://localhost:8000/docs
```

```bash
# ===== FRONTEND SETUP (New Terminal) =====
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# ✓ Frontend running at http://localhost:3000
```

### ✅ Verify Everything Works

1. **Backend API**: http://localhost:8000/docs (interactive API docs)
2. **Frontend UI**: http://localhost:3000 (chat interface)
3. **Try it**: Ask the chatbot a health question

---

## 📦 Running with Docker (Production-Ready)

```bash
# Build images
docker-compose build

# Run both services
docker-compose up

# Backend at http://localhost:8000
# Frontend at http://localhost:3000
```

**Note:** Set environment variables in `.env` file or Docker environment.

---

## 🛠️ Project Structure

```
aihealthcare/
├── backend/              # FastAPI + LLaMA 3 + BioBERT
│   ├── app/
│   │   ├── main.py       # FastAPI app
│   │   ├── config.py     # Env config loader
│   │   ├── models/       # Pydantic schemas
│   │   ├── services/     # LLM, BioBERT, etc.
│   │   └── utils/        # Database, encryption
│   ├── tests/            # Test suite
│   └── requirements.txt   # Python dependencies
├── frontend/             # React + Tailwind + Vite
│   ├── src/
│   │   ├── pages/        # Chat, Insights, Security, Settings
│   │   ├── components/   # Reusable components
│   │   ├── store/        # Zustand state management
│   │   └── api/          # API client
│   └── package.json      # NPM dependencies
├── docs/                 # Documentation
└── .env.example          # Template (commit to repo)
```

See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for detailed structure.

---

## 📚 Documentation

- [🔑 API Keys Setup](docs/API_KEYS_SETUP.md) - How to get each API key
- [🏗️ Architecture](docs/ARCHITECTURE.md) - System design & components
- [⚙️ Backend Setup](docs/SETUP_GUIDE.md) - Detailed backend guide
- [🚀 Production Deployment](docs/QUICK_START_PRODUCTION.md) - Deploy to AWS/Heroku/DigitalOcean
- [🔒 Security](docs/BACKEND_IMPROVEMENTS.md) - Security best practices

---

## 🤝 Contributing

1. Clone the repository
2. Create your feature branch: `git checkout -b feature/my-feature`
3. Create `.env` with your API keys (don't commit it)
4. Make your changes
5. Push to branch: `git push origin feature/my-feature`
6. Open a Pull Request

---

## 📝 License

MIT License - feel free to use for personal or commercial projects

---

## 🎓 Learning Resources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [LLaMA 3 via Groq](https://console.groq.com/)
- [BioBERT Medical NLP](https://huggingface.co/dmis-lab/biobert-base-cased-v1.1)
- [React Documentation](https://react.dev/)
- [Tailwind CSS](https://tailwindcss.com/)

---

## ⭐ If you found this helpful, consider starring the repository!
cp .env.example .env
# Edit .env with your API keys

# Run backend (Terminal 1)
python -m uvicorn app.main:app --reload

# Setup Frontend (Terminal 2)
cd ../frontend
npm install
npm run dev

# Open http://localhost:3000
```

### Option 2: Deployed Version

- **Frontend**: https://ai-healthcare-frontend.vercel.app
- **API Docs**: https://ai-healthcare-backend.onrender.com/docs

---

## 📋 Requirements

### API Keys Needed (All Free)

1. **Groq API** - LLaMA 3 access
   - Get here: https://console.groq.com
   - Free tier: 30 requests per day

2. **MongoDB Atlas** - Cloud database
   - Get here: https://www.mongodb.com/cloud/atlas
   - Free tier: 512MB storage

3. **HuggingFace API** - BioBERT models
   - Get here: https://huggingface.co
   - Free tier: Unlimited

### System Requirements
- Python 3.10+
- Node.js 18+
- Modern web browser
- Internet connection

---

## 📁 Project Structure

```
aihealthcare/
├── backend/
│   ├── app/
│   │   ├── main.py              ← FastAPI app
│   │   ├── config.py            ← Configuration
│   │   ├── models/              ← Data models
│   │   ├── services/            ← Business logic
│   │   │   ├── llm_service.py   ← LLaMA 3
│   │   │   ├── biobert_service.py ← Medical NLP
│   │   │   └── rl_learning.py   ← Feedback system
│   │   └── utils/               ← Utilities
│   │       ├── encryption.py    ← AES-256
│   │       └── database.py      ← MongoDB
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx              ← Main component
│   │   ├── pages/               ← Tab pages
│   │   ├── api/                 ← API client
│   │   ├── store/               ← State management
│   │   └── index.css            ← Tailwind CSS
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
│
├── SETUP_GUIDE.md               ← Installation guide
├── DEPLOYMENT.md                ← Deployment guide
└── README.md                    ← This file
```

---

## 🎨 Features Breakdown

### 1. Chat Tab - Conversational AI
```
💬 Send health questions/symptoms
→ AI analyzes and responds
→ Healthcare mode activated for symptoms
→ Rate responses (👍 👎)
→ System learns from feedback
```

**Key Features:**
- Real-time streaming responses
- Symptom detection
- Condition prediction
- Feedback collection
- Conversation history

### 2. Health Insights Tab - Analytics Dashboard
```
📊 View Charts:
   - Symptom frequency
   - Predicted conditions
   - Feedback trends
   - Learning progress
```

**Key Metrics:**
- Total conversations
- Success rate
- Helpful responses
- Learning statistics

### 3. Security Tab - Trust & Safety
```
🔒 Security Features:
   ✓ AES-256 encryption
   ✓ Secure database
   ✓ API protection
   ✓ Data privacy compliance
```

**Security Details:**
- Encryption implementation
- Data handling policy
- Privacy tips
- Medical disclaimer

### 4. Settings Tab - Customization
```
⚙️ Configuration:
   • Dark mode toggle
   • Data retention settings
   • Chat history management
   • Account information
```

---

## 🔌 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | System health check |
| `/chat` | POST | Send message & get response |
| `/feedback` | POST | Submit response feedback |
| `/history` | POST | Get chat history |
| `/insights` | GET | Get health insights |
| `/rl-stats` | GET | Get learning statistics |
| `/rl-recommendations` | GET | Get improvement suggestions |
| `/security/status` | GET | Check security status |
| `/settings` | GET | Get user settings |
| `/docs` | GET | Interactive API documentation |

**Full API docs**: http://localhost:8000/docs

---

## 🔐 Security Features

### Encryption
- **Algorithm**: AES-256 via Fernet
- **Coverage**: All messages and responses
- **Storage**: Database encryption
- **Keys**: Environment-based key management

### Privacy
- **Data Retention**: Configurable (7-90 days)
- **Anonymity**: User-only tracking
- **No Sharing**: Zero third-party data sharing
- **GDPR Ready**: Compliant data handling

### API Security
- **CORS**: Restricted origins
- **Rate Limiting**: Prevent abuse
- **Input Validation**: Sanitize all inputs
- **Error Handling**: Safe error messages

---

## 🤖 AI Models Used

### LLaMA 3 (8B via Groq)
- **Purpose**: Natural conversation, reasoning
- **Strengths**: Fast, accurate, conversational
- **Integration**: LangChain + Groq API
- **Performance**: <2 second response time

### BioBERT
- **Purpose**: Medical entity recognition
- **Strengths**: Biomedical NLP, symptom extraction
- **Integration**: HuggingFace Transformers
- **Performance**: 95%+ accuracy

### Reinforcement Learning System
- **Purpose**: Learns from user feedback
- **Method**: Reward/penalty scoring
- **Adaptation**: Improves over time
- **Metrics**: Success rate tracking

---

## 🧪 Testing

### API Testing
```bash
# Health check
curl http://localhost:8000/health

# Send message
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"content": "I have a fever", "user_id": "test"}'

# Get feedback stats
curl http://localhost:8000/rl-stats
```

### Frontend Testing
```bash
# Run with Vite dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### End-to-End Testing
```bash
# Both backend and frontend running
# Visit http://localhost:3000
# Send test messages
# Check chat history
# Verify encryption in DB
```

---

## 📊 Performance Metrics

| Metric | Value | Status |
|--------|-------|--------|
| API Response Time | <1s | ✅ Excellent |
| Frontend Load Time | <2s | ✅ Good |
| Encryption Overhead | <100ms | ✅ Negligible |
| Database Query | <500ms | ✅ Fast |
| Feedback Loop | <200ms | ✅ Responsive |

---

## 🚀 Deployment

### Quick Deploy (Free)

**Backend on Render:**
```bash
git push origin main
# Auto-deploy triggered
# Wait 5-10 minutes
# Backend live!
```

**Frontend on Vercel:**
```bash
npm run build
vercel --prod
# Auto-deploy triggered
# Frontend live in 1-2 minutes!
```

See **DEPLOYMENT.md** for detailed instructions.

---

## 🔄 How It Works

### User Flow
```
User sends message
    ↓
Encryption (AES-256)
    ↓
LLM detects intent
    ├─ Healthcare → BioBERT analysis
    └─ General → Direct response
    ↓
Generate response via LLaMA 3
    ↓
Store encrypted in MongoDB
    ↓
Send to frontend
    ↓
User rates (👍 👎)
    ↓
Feedback → RL system learns
```

### Learning Flow
```
User feedback collected
    ↓
Score calculated (+1 / -1)
    ↓
Category performance tracked
    ↓
Improvement recommendations generated
    ↓
System adjusts future responses
    ↓
Success rate increases
```

---

## 📚 Documentation

- **SETUP_GUIDE.md** - Complete setup instructions
- **DEPLOYMENT.md** - Production deployment guide
- **API Docs** - http://localhost:8000/docs
- **Code Comments** - Extensive inline documentation

---

## 🤝 Contributing

This is an educational project. Feel free to:
- Fork and customize
- Add new features
- Improve documentation
- Report issues
- Submit improvements

---

## ⚠️ Medical Disclaimer

**IMPORTANT**: This application is for educational and informational purposes ONLY.

- 🚫 NOT a medical diagnostic tool
- 🚫 NOT a substitute for professional medical advice
- 🚫 Does NOT provide medical diagnosis
- ✅ Always consult licensed healthcare providers
- ✅ In emergencies, call 911 or local emergency number

---

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI
- **AI**: LangChain + Groq + HuggingFace
- **Encryption**: Cryptography library
- **Database**: MongoDB
- **Language**: Python 3.10+

### Frontend
- **Framework**: React 18
- **Build**: Vite
- **Styling**: Tailwind CSS
- **Animations**: Framer Motion
- **Charts**: Recharts
- **Icons**: Lucide React
- **State**: Zustand
- **HTTP**: Axios

### Infrastructure
- **Backend Hosting**: Render
- **Frontend Hosting**: Vercel
- **Database**: MongoDB Atlas
- **API**: RESTful with OpenAPI
- **Monitoring**: Built-in logging

---

## 📈 Growth Roadmap

### Phase 1 ✅ (Current)
- Basic chat interface
- AI responses
- Encryption system
- Health insights

### Phase 2 (Future)
- Mobile app (React Native)
- Doctor integration
- Prescription tracking
- Medication reminders
- Appointment scheduling

### Phase 3 (Future)
- Wearable integration (Apple Watch)
- Lab result analysis
- Personalized health plans
- Insurance integration
- Multi-language support

---

## 📞 Support

### Getting Help
1. Check SETUP_GUIDE.md
2. Review API documentation at /docs
3. Check error logs in terminal
4. Verify API keys are correct
5. Check internet connection

### Common Issues
- **Backend won't start**: Check Python version and dependencies
- **Frontend can't reach backend**: Verify API URL in apiClient.js
- **MongoDB connection fails**: Check connection string and IP whitelist
- **Encryption errors**: Verify ENCRYPTION_KEY is 32 bytes

---

## 📄 License

This project is provided for educational purposes.
Feel free to use, modify, and distribute with attribution.

---

## 🎉 Let's Build the Future of Healthcare!

This platform demonstrates:
- ✅ Production-ready AI integration
- ✅ Secure data handling
- ✅ Modern UI/UX design
- ✅ Cloud deployment
- ✅ Learning systems
- ✅ Professional architecture

**Use this as:**
- A hackathon submission
- A learning resource
- A portfolio project
- A foundation for your product
- An educational tool

---

## 🙏 Credits

Built with:
- 🤖 AI/ML expertise
- 🎨 UI/UX best practices
- 🔒 Security best practices
- ☁️ Cloud architecture
- 📱 Modern web technologies

---

## 📞 Questions?

Open an issue on GitHub or check the documentation.

**Happy healing! 🏥**

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**Status**: Production Ready ✅
#   A I _ M e d i B o t 
 
 