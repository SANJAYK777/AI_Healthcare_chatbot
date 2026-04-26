# 🔧 Environment Variable Configuration - Technical Details

## How the Backend Loads Environment Variables

### File: `backend/app/config.py`

```python
"""
Configuration file for the AI Healthcare Chatbot
Loads and validates environment variables
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Get absolute path to .env file
ENV_FILE = Path(__file__).parent.parent / ".env"
print(f"🔍 Loading .env from: {ENV_FILE}")
print(f"🔍 .env exists: {ENV_FILE.exists()}")

# Load environment variables from .env file using absolute path
load_dotenv(dotenv_path=str(ENV_FILE), override=True)

# ==================== API KEYS ====================
# Load from environment, use empty string as fallback
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "").strip()
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb+srv://demo:demo@test.mongodb.net/healthcare")

# DEBUG: Print loaded keys (first 20 chars for security)
print(f"✓ CONFIG LOADED - GROQ_API_KEY (first 20 chars): {GROQ_API_KEY[:20] if GROQ_API_KEY else 'EMPTY'}")
print(f"✓ CONFIG LOADED - HUGGINGFACE_API_KEY (first 20 chars): {HUGGINGFACE_API_KEY[:20] if HUGGINGFACE_API_KEY else 'EMPTY'}")
```

### Key Loading Mechanism

1. **At Startup**: When `backend/app/main.py` imports `config.py`:
   - Looks for `.env` file in `backend/` directory
   - Uses `python-dotenv` to load environment variables
   - Prints debug info (first 20 chars of keys)

2. **At Runtime**: Services access keys via `config.py`:
   ```python
   from app.config import GROQ_API_KEY, HUGGINGFACE_API_KEY
   
   # Use in your service
   llama_client = Groq(api_key=GROQ_API_KEY)
   ```

3. **Environment Priority**:
   - System environment variables (highest priority)
   - `.env` file in `backend/`
   - Default values in code (fallback)

---

## .env File Structure

### Location: `backend/.env`

```env
# ============================================================
# 🔑 REQUIRED API KEYS
# ============================================================

# Groq API Key (for LLaMA 3)
# - Get from: https://console.groq.com/keys
# - Sign up, create new key
# - Key looks like: gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx (56 chars)
GROQ_API_KEY=your_actual_groq_key_here

# HuggingFace API Token (for BioBERT)  
# - Get from: https://huggingface.co/settings/tokens
# - Create "Read" access token
# - Token looks like: hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
HUGGINGFACE_API_KEY=your_actual_hf_token_here

# ============================================================
# 💾 DATABASE CONFIGURATION
# ============================================================

# MongoDB Connection String
# - Get from: https://www.mongodb.com/cloud/atlas
# - Create cluster, get connection string
# - Format: mongodb+srv://username:password@cluster.mongodb.net/healthcare
MONGODB_URI=mongodb+srv://user:password@your_cluster.mongodb.net/healthcare

# ============================================================
# 🔐 ENCRYPTION CONFIGURATION
# ============================================================

# Encryption Key (32 bytes = 64 hex characters)
# - Must be exactly 64 hex characters
# - Generate new: python -c "import os; print(os.urandom(32).hex())"
ENCRYPTION_KEY=0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef

# ============================================================
# ⚙️ SERVER CONFIGURATION
# ============================================================

# Debug mode (True for development, False for production)
DEBUG=True

# Server port
PORT=8000

# Server host
HOST=0.0.0.0

# ============================================================
# 📦 DATABASE SCHEMA
# ============================================================

DATABASE_NAME=healthcare_chatbot
```

---

## Production Environment Variables

### Using System Environment Variables

Instead of `.env` file, production systems set env vars:

**Docker:**
```bash
docker run -e GROQ_API_KEY="gsk_xxxxx" \
           -e HUGGINGFACE_API_KEY="hf_xxxxx" \
           -e MONGODB_URI="mongodb+srv://..." \
           my-app
```

**Heroku:**
```bash
heroku config:set GROQ_API_KEY="gsk_xxxxx"
heroku config:set HUGGINGFACE_API_KEY="hf_xxxxx"
heroku config:set MONGODB_URI="mongodb+srv://..."
```

**AWS Lambda/ECS:**
Set environment variables in AWS console or CloudFormation

**GitHub Actions CI/CD:**
```yaml
env:
  GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}
  HUGGINGFACE_API_KEY: ${{ secrets.HUGGINGFACE_API_KEY }}
```

---

## Security Best Practices

### ✅ DO

- ✅ Add `.env` to `.gitignore` (already done)
- ✅ Use `.env.example` with placeholders only
- ✅ Load env vars at application startup
- ✅ Validate required env vars exist before starting
- ✅ Never print full API keys (only first 20 chars)
- ✅ Use strong encryption keys
- ✅ Rotate API keys periodically
- ✅ Use different keys for dev/staging/production

### ❌ DON'T

- ❌ Commit `.env` file with real keys
- ❌ Store API keys in code comments
- ❌ Expose keys in error messages
- ❌ Log full API keys
- ❌ Use same API keys across environments
- ❌ Share API keys via email/Slack
- ❌ Hardcode connection strings
- ❌ Store keys in documentation

---

## Troubleshooting

### "Missing or invalid API keys" Error

**Problem**: Backend starts but shows config error

**Solution**:
```bash
cd backend

# Verify .env exists
ls -la .env

# Check content (first line should have = sign)
head -5 .env

# Verify values aren't empty
grep "GROQ_API_KEY" .env
grep "HUGGINGFACE_API_KEY" .env
```

### Keys Load But Services Fail

**Problem**: Config loaded but LLM/BioBERT service errors

**Causes**:
1. API keys are wrong format
2. API keys are expired/revoked
3. Network/firewall blocking API calls
4. API service down

**Solution**:
1. Test API key manually: `curl https://api.groq.com -H "Authorization: Bearer <KEY>"`
2. Check API account online
3. Verify firewall/proxy settings
4. Check API status page

### "MONGODB_URI" Connection Error

**Problem**: Database connection fails

**Solution**:
```python
# In backend/app/utils/database.py, falls back to in-memory storage
# This is intentional for development without MongoDB
```

If you want to use MongoDB:
1. Get connection string from MongoDB Atlas
2. Add to `.env`: `MONGODB_URI=mongodb+srv://...`
3. Restart backend

---

## Environment Variable Reference

| Variable | Type | Required | Format | Example |
|----------|------|----------|--------|---------|
| `GROQ_API_KEY` | String | Yes | `gsk_` prefix, 56 chars | `gsk_xxxxxxxx...` |
| `HUGGINGFACE_API_KEY` | String | Yes | `hf_` prefix | `hf_xxxxxxxx...` |
| `MONGODB_URI` | String | No | MongoDB connection string | `mongodb+srv://user:pass@...` |
| `ENCRYPTION_KEY` | String | No | 64 hex characters (32 bytes) | `0123456789abcdef...` |
| `DEBUG` | Boolean | No | `True` or `False` | `True` |
| `PORT` | Integer | No | 1-65535 | `8000` |
| `HOST` | String | No | IP address | `0.0.0.0` |
| `DATABASE_NAME` | String | No | Database name | `healthcare_chatbot` |

---

## Verification Script

Save as `verify_env.py`:

```python
#!/usr/bin/env python3
"""Verify all required environment variables are set"""

import os
from dotenv import load_dotenv

# Load from .env
load_dotenv()

required = {
    'GROQ_API_KEY': 'gsk_',
    'HUGGINGFACE_API_KEY': 'hf_',
}

optional = {
    'MONGODB_URI': 'mongodb',
    'ENCRYPTION_KEY': '256',  # Just check it's set
}

print("🔍 Checking required environment variables...")
for var, prefix in required.items():
    value = os.getenv(var, "").strip()
    if not value:
        print(f"❌ {var}: MISSING")
    elif not value.startswith(prefix):
        print(f"⚠️ {var}: Unexpected format (expected {prefix}...)")
    else:
        print(f"✅ {var}: OK (prefix: {prefix}...)")

print("\n🔍 Checking optional environment variables...")
for var, check in optional.items():
    value = os.getenv(var, "").strip()
    if not value:
        print(f"⚠️ {var}: Not set (optional)")
    else:
        print(f"✅ {var}: Set")

print("\n✅ Verification complete!")
```

Run with:
```bash
python verify_env.py
```

