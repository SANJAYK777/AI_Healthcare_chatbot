# 🎯 GET YOUR AI HEALTHCARE CHATBOT WORKING - QUICK GUIDE

## Current Status ✅

| Component | Status | Note |
|-----------|--------|------|
| Frontend | ✅ Running | http://localhost:3000 |
| Backend | ✅ Running | http://localhost:8000 |
| Demo Mode | ✅ Active | Working but limited |
| Production Mode | ⚠️ Needs API Keys | Full features available |

---

## 3-Step Setup (10 minutes)

### STEP 1: Get GROQ API Key (3 minutes)

1. Open: https://console.groq.com/keys
2. Sign up / Log in
3. Click "Create API Key"
4. Copy the key (looks like: `gsk_xxxxxxxxxxxx`)
5. Keep it safe!

✅ **You now have:** GROQ_API_KEY

---

### STEP 2: Get HuggingFace Token (3 minutes)

1. Open: https://huggingface.co/settings/tokens
2. Sign up / Log in
3. Click "New token"
4. Name: "Healthcare Chatbot"
5. Type: "Read"
6. Click "Create"
7. Copy token (looks like: `hf_xxxxxxxxxx`)

✅ **You now have:** HUGGINGFACE_API_KEY

---

### STEP 3: Add Keys to .env File (2 minutes)

**File Location:**
```
c:\Users\SANJAY K\Documents\aihealthcare\backend\.env
```

**Replace these lines:**
```
GROQ_API_KEY=demo_key_for_testing
HUGGINGFACE_API_KEY=demo_hf_token
```

**With your actual keys:**
```
GROQ_API_KEY=gsk_your_actual_key_here
HUGGINGFACE_API_KEY=hf_your_actual_token_here
```

---

### STEP 4: Restart Backend (1 minute)

1. **Stop backend:** Press `Ctrl+C` in backend terminal
2. **Restart backend:**
   ```bash
   cd "c:\Users\SANJAY K\Documents\aihealthcare\backend"
   python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
   ```

3. **Look for message:**
   ```
   ✅ All API keys configured - Production mode enabled!
   ✓ LLM Service (LLaMA 3) initialized with GROQ_API_KEY
   ```

---

### STEP 5: Test the Chatbot! 🎉

1. Open: http://localhost:3000
2. Send message: **"I have a fever and cough"**
3. Get real LLaMA 3 response!

---

## ✨ What Changes with Real API Keys

### Before (Demo Mode):
```
User: I have a fever
Bot: I notice you're asking about a health concern. 
     In demo mode, I can't provide medical analysis...
```

### After (Production Mode):
```
User: I have a fever
Bot: Based on your symptoms of fever and cough, 
     these could indicate:
     • Common cold
     • Influenza
     • Other respiratory infections
     
     Please ensure you get rest, stay hydrated, 
     and consult a healthcare provider if symptoms persist.
```

---

## 📊 Backend Configuration Messages

After restarting, your backend will show:

**✅ Success (with valid API keys):**
```
====================================================================
🚀 Starting AI Healthcare Chatbot Platform...
====================================================================
✅ All API keys configured - Production mode enabled!
✓ LLM Service (LLaMA 3) initialized with GROQ_API_KEY
✓ BioBERT Service initialized (Medical NLP)
✓ Database initialized successfully
✓ All services ready!
====================================================================
```

**⚠️ Demo Mode (without API keys):**
```
====================================================================
🚀 Starting AI Healthcare Chatbot Platform...
====================================================================
⚠️  Missing or invalid API keys: GROQ_API_KEY, HUGGINGFACE_API_KEY
📝 To enable production features, add API keys to backend/.env:
   GROQ_API_KEY=your_key_from_console.groq.com
   HUGGINGFACE_API_KEY=your_token_from_huggingface.co
⚠️ LLM Service: Using demo mode (no GROQ_API_KEY)
✓ All services ready!
====================================================================
```

---

## 🔒 Security Reminders

✅ **DO:**
- Keep API keys in .env file only
- Don't share keys on internet
- Add .env to .gitignore (already done)
- Use different keys for different environments

❌ **DON'T:**
- Commit .env to GitHub
- Share keys in Discord/chat
- Use placeholder keys in production
- Hardcode keys in code

---

## 🆘 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| "Missing API keys" message | Add real keys to .env file |
| Backend shows demo mode | Restart backend after adding keys |
| Keys not working | Make sure no spaces around key value |
| Still getting demo response | Check backend console for errors |
| HuggingFace token rejected | Use "Read" permission token |

---

## 📚 Related Documentation

- [API_KEYS_SETUP.md](API_KEYS_SETUP.md) - Detailed setup guide
- [README.md](README.md) - Project overview
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Local development setup
- [DEPLOYMENT.md](DEPLOYMENT.md) - Production deployment

---

## 🚀 Next Steps After Setup

1. ✅ Add API keys → Restart backend
2. ✅ Test chatbot at http://localhost:3000
3. ✅ Send some health questions to verify
4. ✅ Explore other tabs (Health Insights, Security, Settings)
5. ✅ Deploy to production (see DEPLOYMENT.md)

---

## 📞 Support

### Backend Issues
Check backend console for error messages. Key status is shown on startup.

### API Key Issues
- GROQ: https://console.groq.com/docs
- HuggingFace: https://huggingface.co/docs/hub/security-tokens

### Chatbot Issues
- Refresh browser (Ctrl+Shift+R)
- Check browser console (F12)
- Restart both frontend and backend

---

**Ready to enable full AI features? Just add your API keys! 🎉**
