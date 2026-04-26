# 📁 AI Healthcare Chatbot - Project Structure

## Overview
This document describes the reorganized hierarchical structure of the AI Healthcare Chatbot project for better maintainability and scalability.

---

## 📂 Root Directory Structure

```
aihealthcare/
├── docs/                          # 📚 ALL documentation (moved from root)
│   ├── API_KEYS_SETUP.md
│   ├── ARCHITECTURE.md
│   ├── BACKEND_IMPROVEMENTS.md
│   ├── DEPLOYMENT.md
│   ├── QUICK_START_PRODUCTION.md
│   ├── SETUP_GUIDE.md
│   └── ...
├── backend/                       # 🐍 FastAPI Backend
├── frontend/                      # ⚛️ React Frontend
├── README.md                      # 📖 Main project README
├── PROJECT_STRUCTURE.md           # 📋 This file
├── .gitignore                     # Git ignore rules
├── .env.example                   # Environment template
├── start.cmd                      # Windows startup script
└── start.sh                       # Unix startup script
```

---

## 🐍 Backend Structure

```
backend/
├── main.py                        # Entry point (calls app.main)
├── requirements.txt               # Python dependencies
├── .env                           # Environment variables (NEVER commit)
├── .env.example                   # Template for .env
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application setup
│   ├── config.py                  # Configuration loader
│   │
│   ├── models/                    # 📊 Data Models & Schemas
│   │   ├── __init__.py
│   │   └── schemas.py             # Pydantic schemas (ChatMessage, Response, etc.)
│   │
│   ├── routes/                    # 🛣️ API Endpoints (expandable)
│   │   ├── __init__.py
│   │   ├── chat.py                # Chat endpoints (future)
│   │   ├── health.py              # Health data endpoints (future)
│   │   └── admin.py               # Admin endpoints (future)
│   │
│   ├── services/                  # 🧠 Business Logic Services
│   │   ├── __init__.py
│   │   ├── llm_service.py         # LLaMA 3 via Groq API
│   │   ├── biobert_service.py     # Medical NLP (BioBERT)
│   │   └── rl_learning.py         # Reinforcement Learning feedback
│   │
│   └── utils/                     # 🔧 Utility Functions
│       ├── __init__.py
│       ├── database.py            # MongoDB utilities
│       └── encryption.py          # AES-256 encryption
│
├── tests/                         # ✅ Test Suite (organized)
│   ├── __init__.py
│   ├── test_api.py                # API endpoint tests
│   ├── test_chat.py               # Chat functionality tests
│   ├── test_encryption.py         # Encryption tests
│   ├── test_health_chat.py        # Health chat tests
│   └── init_db.py                 # Database initialization
│
├── logs/                          # 📝 Application logs
├── venv/                          # 🐍 Virtual environment (git-ignored)
└── __pycache__/                   # Python cache (git-ignored)
```

---

## ⚛️ Frontend Structure

```
frontend/
├── package.json                   # NPM dependencies
├── vite.config.js                 # Vite configuration
├── tailwind.config.js             # Tailwind CSS config
├── postcss.config.js              # PostCSS config
├── index.html                     # HTML entry point
│
└── src/
    ├── main.jsx                   # React entry point
    ├── App.jsx                    # Main app component
    ├── index.css                  # Global styles
    │
    ├── pages/                     # 📄 Page Components
    │   ├── ChatTab.jsx            # Chat interface
    │   ├── InsightsTab.jsx        # Health insights dashboard
    │   ├── SecurityTab.jsx        # Security & encryption info
    │   └── SettingsTab.jsx        # User settings
    │
    ├── components/                # 🧩 Reusable Components (expandable)
    │   ├── MessageList.jsx        # Message display (future)
    │   ├── InputBox.jsx           # Chat input (future)
    │   └── Charts.jsx             # Dashboard charts (future)
    │
    ├── store/                     # 🏪 State Management
    │   └── store.js               # Zustand store (chat state, settings)
    │
    ├── api/                       # 🌐 API Communication
    │   └── apiClient.js           # Axios/fetch API client
    │
    ├── hooks/                     # 🎣 Custom React Hooks (expandable)
    │   ├── useChat.js             # Chat logic
    │   └── useAuth.js             # Authentication (future)
    │
    ├── utils/                     # 🔧 Helper Functions (expandable)
    │   ├── format.js              # Text formatting
    │   └── validators.js          # Input validation
    │
    └── types/                     # 📋 TypeScript Types (expandable)
        └── index.d.ts             # Type definitions
```

---

## 🔄 Import Patterns

### Backend
```python
# ✅ CORRECT - Use absolute imports from app root
from app.models.schemas import ChatMessage
from app.services.llm_service import LLMService
from app.utils.encryption import EncryptionService
```

### Frontend
```javascript
// ✅ CORRECT - Use absolute or relative imports
import { useChatStore } from '@/store/store';
import { chatAPI } from '@/api/apiClient';
import ChatTab from '@/pages/ChatTab';
```

---

## 🗑️ Cleanup Changes

### ✅ Deleted Files
- **`backend/fix_env.py`** - 🔴 SECURITY RISK (contained hardcoded API keys)

### ✅ Moved Files
- All `test_*.py` files → `backend/tests/`
- All documentation (MD files) → `docs/`
- `init_db.py` → `backend/tests/init_db.py`

### ✅ Created Directories
- `backend/tests/` - Test suite
- `backend/app/routes/` - For future route modularization
- `frontend/src/components/` - Reusable components
- `frontend/src/hooks/` - Custom React hooks
- `frontend/src/utils/` - Helper functions
- `frontend/src/types/` - TypeScript definitions
- `docs/` - Centralized documentation

---

## 📋 File Naming Conventions

### Python Backend
- **Services**: `noun_service.py` (e.g., `llm_service.py`, `biobert_service.py`)
- **Routes**: `entity_routes.py` (e.g., `chat_routes.py`, `user_routes.py`)
- **Tests**: `test_feature.py` (e.g., `test_api.py`, `test_encryption.py`)
- **Utils**: `action.py` (e.g., `database.py`, `encryption.py`)

### React Frontend
- **Components**: `PascalCase.jsx` (e.g., `ChatTab.jsx`, `MessageList.jsx`)
- **Hooks**: `camelCase.js` with `use` prefix (e.g., `useChat.js`)
- **Utils**: `camelCase.js` (e.g., `formatDate.js`, `validators.js`)
- **Stores**: `store.js` (e.g., `store.js` for Zustand)

---

## 🔐 Security Notes

- ✅ `.env` files are in `.gitignore` - Never commit credentials
- ✅ API keys are loaded from environment variables only
- ✅ Encryption service uses AES-256 for data security
- ✅ CORS properly configured for development

---

## 🚀 Running the Project

### With proper structure:
```bash
# Backend
cd backend
python -m uvicorn app.main:app --reload

# Frontend (separate terminal)
cd frontend
npm run dev
```

### Access Points:
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`

---

## 📈 Future Expansion Areas

### Backend
- `backend/app/routes/` - Modularize endpoints
- `backend/app/middleware/` - Custom middleware
- `backend/app/models/` - Add more schema models

### Frontend
- `frontend/src/components/` - Break down complex pages into components
- `frontend/src/hooks/` - Extract complex logic into custom hooks
- `frontend/src/types/` - Add TypeScript types

---

## ✅ Verification Checklist

- [x] All documentation moved to `docs/`
- [x] Test files organized in `backend/tests/`
- [x] `fix_env.py` deleted (security risk)
- [x] Python package structure with `__init__.py` files
- [x] `.gitignore` properly configured
- [x] Backend imports work with new structure
- [x] Frontend structure ready for scaling
- [x] Project is fully functional

---

**Last Updated**: April 26, 2026  
**Status**: ✅ Reorganization Complete
