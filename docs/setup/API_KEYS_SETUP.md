# 🔑 API KEYS SETUP GUIDE

## Quick Start - Get Your API Keys (5 minutes)

This guide shows you how to get free API keys for LLaMA 3 and BioBERT to enable full chatbot features.

---

## 1️⃣ GROQ API KEY (LLaMA 3 - Required)

### What is GROQ?
GROQ provides free access to LLaMA 3 model through their API, perfect for our healthcare chatbot.

### Steps to Get Your Key:

1. **Go to GROQ Console:**
   - Visit: https://console.groq.com/keys
   - Click "Sign Up" or "Sign In"

2. **Create Account:**
   - Use your email or Google/GitHub
   - Verify your email

3. **Generate API Key:**
   - Click "Create API Key"
   - Copy the key (keep it secret!)
   - Click "Copy"

4. **Example key:**
   ```
   gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

---

## 2️⃣ HUGGINGFACE API KEY (BioBERT - Optional but Recommended)

### What is HuggingFace?
HuggingFace provides access to BioBERT, a medical-specific AI model for symptom/condition detection.

### Steps to Get Your Token:

1. **Go to HuggingFace:**
   - Visit: https://huggingface.co/settings/tokens
   - Click "Sign Up" or "Log In"

2. **Create Account:**
   - Use email or social login
   - Verify your email

3. **Create New Token:**
   - Click "New token"
   - Name: "Healthcare Chatbot"
   - Type: "Read" (fine for our use)
   - Click "Create"

4. **Copy Token:**
   - Click copy icon
   - Token looks like: `hf_xxxxxxxxxxxxxxxxxxxxx`

---

## 3️⃣ CREATE .env FILE

### Location:
```
c:\Users\SANJAY K\Documents\aihealthcare\backend\.env
```

### Content:
```
# GROQ API (Required for LLaMA 3)
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# HuggingFace API (Required for BioBERT)
HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxxxxxxxxxx

# MongoDB (Optional - leave as is for demo)
MONGODB_URI=mongodb+srv://demo:demo@test.mongodb.net/healthcare

# Encryption Key (Optional - already set)
ENCRYPTION_KEY=0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef

# Server Settings
DEBUG=True
PORT=8000
HOST=127.0.0.1
```

### ⚠️ IMPORTANT:
- **DO NOT share your .env file**
- **DO NOT commit .env to GitHub**
- **Keep API keys secret!**

---

## 4️⃣ VERIFY SETUP

### Test Backend:
```bash
cd backend
python -c "from app.config import CONFIG_STATUS, IS_PRODUCTION_READY; print(f'Status: {CONFIG_STATUS}'); print(f'Production Ready: {IS_PRODUCTION_READY}')"
```

### Expected Output (with keys):
```
Status: All API keys configured - Production mode enabled!
Production Ready: True
```

### Expected Output (demo mode):
```
Status: Missing or invalid API keys: GROQ_API_KEY, HUGGINGFACE_API_KEY
Production Ready: False
```

---

## 5️⃣ RESTART BACKEND

After adding API keys:

```bash
# Kill current backend (Ctrl+C)

# Restart backend
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### Look for in console:
```
✅ All API keys configured - Production mode enabled!
✓ LLM Service (LLaMA 3) initialized with GROQ_API_KEY
```

---

## 6️⃣ TEST IN CHATBOT

1. **Open:** http://localhost:3000
2. **Send message:** "I have a fever and cough"
3. **You should get:**
   - ✅ Real LLaMA 3 response (not demo message)
   - ✅ Symptom detection (fever, cough)
   - ✅ Condition suggestions

---

## 📊 COMPARISON: Demo vs Production

| Feature | Demo Mode | Production Mode |
|---------|-----------|-----------------|
| Chat UI | ✅ Works | ✅ Works |
| Messages | ✅ Works | ✅ Works |
| LLaMA 3 Response | ❌ Demo text | ✅ Real AI |
| Symptom Detection | ❌ Fake | ✅ Real BioBERT |
| Condition Prediction | ❌ Hardcoded | ✅ ML-based |
| Encryption | ✅ Works | ✅ Works |
| Database | ✅ In-memory | ✅ Production-ready |

---

## 🆘 TROUBLESHOOTING

### Issue: "Missing or invalid API keys" message
**Solution:** 
- Check .env file exists in `backend/` folder
- Verify keys are pasted correctly (no extra spaces)
- Restart backend after adding keys

### Issue: Backend shows demo mode on startup
**Solution:**
- Copy exact key from console.groq.com
- Remove any quotes or extra characters
- Ensure .env file is in backend folder (not root)

### Issue: "Invalid GROQ_API_KEY"
**Solution:**
- Go back to console.groq.com
- Create new key
- Keys expire - may need fresh one
- Test key on https://console.groq.com/playground

### Issue: HuggingFace token not working
**Solution:**
- Use "Read" permission token (not "Write")
- Keys must start with `hf_`
- Create new token if unsure

---

## 📚 WHAT EACH API DOES

### GROQ API (LLaMA 3)
- **Purpose:** Generates conversational responses
- **Model:** Mixtral-8x7b-32768 (LLaMA compatible)
- **Speed:** Ultra-fast (best for production)
- **Cost:** Free tier available
- **Use in:** `/chat` endpoint - generates AI responses

### HuggingFace BioBERT
- **Purpose:** Medical entity recognition
- **Model:** dmis-lab/biobert-base-cased-v1.1
- **Speed:** Fast enough for real-time
- **Cost:** Free tier available
- **Use in:** Symptom detection, condition prediction

---

## 🚀 NEXT STEPS

1. ✅ Get both API keys (15 min)
2. ✅ Add to .env file (2 min)
3. ✅ Restart backend (1 min)
4. ✅ Test chatbot (2 min)
5. ✅ Deploy to production (follow DEPLOYMENT.md)

---

## 📞 NEED HELP?

- **GROQ Issues:** https://console.groq.com/docs
- **HuggingFace Issues:** https://huggingface.co/docs/hub/security-tokens
- **Backend Issues:** Check backend console for error messages

---

## 🔒 SECURITY BEST PRACTICES

✅ **DO:**
- Keep .env in backend folder only
- Add .env to .gitignore (already done)
- Use new keys for each environment
- Rotate keys occasionally

❌ **DON'T:**
- Commit .env to git
- Share keys in Discord/Slack
- Use same key in production
- Expose keys in error messages

---

**Once configured, your chatbot will have:**
- Real LLaMA 3 AI responses
- Medical symptom detection
- Healthcare-aware responses
- Full production capabilities

Good luck! 🎉
