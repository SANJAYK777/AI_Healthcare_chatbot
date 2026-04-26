# Deployment Guide - Production Ready

## 🚀 Deployment Architecture

```
Frontend (Vercel)     Backend (Render)      Database (MongoDB Atlas)
     ↓                      ↓                         ↓
  React App    ←→    FastAPI Server    ←→    MongoDB Cluster
  (3000)              (8000)                   (Cloud)
```

---

## Backend Deployment (Render)

### Step 1: Prepare Backend for Production

Update `backend/main.py`:

```python
# Change debug mode
DEBUG = os.getenv("DEBUG", "False") == "True"

# Add production logging
if not DEBUG:
    logging.basicConfig(level=logging.WARNING)
```

### Step 2: Create Render Account

1. Go to https://render.com
2. Sign up with GitHub
3. Grant repository access

### Step 3: Connect GitHub Repository

1. Click **"New +"** → **"Web Service"**
2. Select your GitHub repository
3. Fill in settings:
   - **Name**: `ai-healthcare-backend`
   - **Environment**: `Python 3.10`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

### Step 4: Set Environment Variables on Render

Go to **Settings** → **Environment Variables** and add:

```
GROQ_API_KEY=your_groq_key
HUGGINGFACE_API_KEY=your_hf_token
MONGODB_URI=your_mongodb_uri
ENCRYPTION_KEY=your_32_byte_key
DEBUG=False
PORT=8000
```

### Step 5: Deploy

Click **"Deploy"** and wait for build to complete.

**Your backend URL**: `https://ai-healthcare-backend.onrender.com`

### Step 6: Verify Deployment

```bash
# Test health endpoint
curl https://ai-healthcare-backend.onrender.com/health

# Should return:
# {"status":"healthy","services":{...}}
```

---

## Frontend Deployment (Vercel)

### Step 1: Build Frontend Locally

```bash
cd frontend
npm run build
```

This creates optimized `dist/` folder.

### Step 2: Create Vercel Account

1. Go to https://vercel.com
2. Sign up with GitHub
3. Grant repository access

### Step 3: Deploy Frontend

#### Option A: Via Vercel Dashboard

1. Click **"Add New..."** → **"Project"**
2. Select your GitHub repository
3. Configure:
   - **Framework**: Vite
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

#### Option B: Via Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel --prod
```

### Step 4: Set Environment Variables

In Vercel Dashboard:
1. **Settings** → **Environment Variables**
2. Add:
   ```
   VITE_API_URL=https://ai-healthcare-backend.onrender.com
   ```

### Step 5: Redeploy

The frontend will automatically redeploy with the new environment variables.

**Your frontend URL**: `https://ai-healthcare-frontend.vercel.app`

---

## MongoDB Atlas Setup (Free Tier)

### Step 1: Create Free Cluster

1. Go to https://www.mongodb.com/cloud/atlas
2. Create **New Project**: "AI Healthcare"
3. Create **New Cluster** (M0 Free Tier)
4. Choose region closest to you
5. Wait for cluster to be ready (~10 min)

### Step 2: Create Database User

1. Go to **Database Access**
2. Click **"Add New Database User"**
3. Set username and strong password
4. Click **"Add User"**

### Step 3: Whitelist IPs

1. Go to **Network Access**
2. Click **"Add IP Address"**
3. Select **"Allow access from anywhere"** (for development)
   - For production, whitelist specific IPs
4. Click **"Confirm"**

### Step 4: Get Connection String

1. Go to **Clusters**
2. Click **"Connect"**
3. Select **"Drivers"** → Python 3.10
4. Copy connection string
5. Replace placeholders:
   - `<username>`: your database user
   - `<password>`: your database password
   - `/healthcare`: database name (optional)

Example:
```
mongodb+srv://admin:SecurePass123@cluster.mongodb.net/healthcare
```

### Step 5: Configure Collections Indexes

Connect to MongoDB and run:

```javascript
// Create indexes for better performance
db.chat_history.createIndex({ "user_id": 1, "timestamp": -1 });
db.chat_history.createIndex({ "encrypted": 1 });
db.feedback.createIndex({ "user_id": 1, "timestamp": -1 });
db.sessions.createIndex({ "user_id": 1 });
```

---

## Custom Domain Setup (Optional)

### For Vercel Frontend

1. **Buy domain** from:
   - GoDaddy
   - Namecheap
   - Route 53
   - Vercel Domains

2. **Add to Vercel**:
   - Go to project **Settings** → **Domains**
   - Enter domain name
   - Follow DNS instructions
   - Update nameservers at registrar

### For Render Backend

1. **Add domain**:
   - Go to service **Settings** → **Custom Domain**
   - Add your domain
   - Update CNAME record at registrar

Example DNS records:
```
Frontend:  www.yourdomain.com → yourdomain.vercel.app
Backend:   api.yourdomain.com → ai-healthcare-backend.onrender.com
```

---

## Monitoring & Logging

### Render Logs

```bash
# View logs in real-time
# In Render Dashboard → Your Service → Logs tab

# Or use tail command
tail -f logs
```

### Vercel Analytics

1. Go to project
2. Click **"Analytics"**
3. View:
   - Page load times
   - Core Web Vitals
   - Geographical distribution
   - Error tracking

### MongoDB Monitoring

1. Go to **Monitoring**
2. View:
   - Database performance
   - Connection count
   - Storage usage
   - Query analysis

---

## Performance Optimization

### Frontend Optimization

```javascript
// Frontend build optimizations
// vite.config.js
export default {
  build: {
    minify: 'terser',
    sourcemap: false,
    rollupOptions: {
      output: {
        manualChunks: {
          'react': ['react', 'react-dom'],
          'motion': ['framer-motion'],
          'charts': ['recharts'],
        }
      }
    }
  }
}
```

### Backend Optimization

```python
# Enable caching
from fastapi_cache2 import FastAPICache2
from fastapi_cache2.backends.redis import RedisBackend
from redis import asyncio as aioredis

# Use connection pooling for MongoDB
from pymongo.errors import ConnectionFailure

# Implement rate limiting
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
```

### Database Optimization

```javascript
// MongoDB query optimization
// Use indexes and projection
db.chat_history.find(
  { user_id: "user123" },
  { message: 1, response: 1, timestamp: 1 }
).limit(50)
```

---

## Security Checklist for Production

- [ ] All API keys stored in environment variables
- [ ] HTTPS enabled on all endpoints
- [ ] CORS properly configured (specific origins)
- [ ] Rate limiting implemented
- [ ] Input validation on all endpoints
- [ ] SQL injection prevention (using parameterized queries)
- [ ] XSS prevention (Sanitize user input)
- [ ] CSRF tokens implemented
- [ ] Sensitive data encrypted
- [ ] Error messages don't leak info
- [ ] Logging doesn't log sensitive data
- [ ] API keys rotated regularly
- [ ] Database backups configured
- [ ] SSL certificates valid
- [ ] Security headers set (CSP, X-Frame-Options, etc.)

---

## Backup & Recovery

### MongoDB Automatic Backups

1. Go to **Backups** section
2. Enable **Daily Automatic Backups** (Free M0)
3. Retention: Last 7 days

### Manual Backup

```bash
# Dump database
mongodump --uri="your_mongodb_uri" --out=./backup

# Restore database
mongorestore --uri="your_mongodb_uri" ./backup
```

### GitHub Backup

Always keep code in GitHub:
```bash
git push origin main
```

---

## Scaling for Production

### When to Scale Up

1. **Frontend**: 
   - If Vercel reports high latency
   - Solution: Upgrade to Pro plan, use CDN

2. **Backend**:
   - If Render reports CPU usage > 80%
   - Solution: Upgrade to Standard plan, add more workers

3. **Database**:
   - If MongoDB storage > 512MB
   - Solution: Upgrade to M2 cluster

---

## Cost Estimation (Monthly)

| Service | Free Tier | Cost |
|---------|-----------|------|
| Vercel | 100GB bandwidth | Free |
| Render | 750 hours | Free |
| MongoDB | 0.5GB storage | Free |
| **Total** | **Limited** | **$0** |

**Upgrade costs** (if needed):
- Vercel Pro: $20/month
- Render Standard: $7/month
- MongoDB M2: $15-20/month

---

## Troubleshooting Deployments

### Render Build Fails
```
Error: pip install fails

Solution:
1. Check requirements.txt syntax
2. Remove problematic packages (test locally first)
3. Increase build timeout
```

### Vercel Build Fails
```
Error: npm install fails

Solution:
1. Clear npm cache: npm cache clean --force
2. Delete package-lock.json, reinstall
3. Check Node version compatibility
```

### MongoDB Connection Timeout
```
Error: ServerSelectionTimeoutError

Solution:
1. Whitelist Render/Vercel IP ranges
2. Check MongoDB URI format
3. Verify database exists
4. Increase timeout: serverSelectionTimeoutMS=30000
```

---

## CI/CD Pipeline (Advanced)

### GitHub Actions Auto-Deploy

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy Backend
        run: |
          curl https://api.render.com/deploy/srv-xxxxx?key=${{ secrets.RENDER_DEPLOY_KEY }}
      
      - name: Deploy Frontend
        run: |
          vercel --prod --token ${{ secrets.VERCEL_TOKEN }}
```

---

## Maintenance

### Weekly Tasks
- [ ] Monitor error logs
- [ ] Check API response times
- [ ] Review database usage

### Monthly Tasks
- [ ] Update dependencies
- [ ] Review security logs
- [ ] Backup database manually
- [ ] Update encryption keys (if needed)

### Quarterly Tasks
- [ ] Load testing
- [ ] Security audit
- [ ] Performance review
- [ ] Cost optimization

---

## Support & Troubleshooting

### Render Support
- Docs: https://render.com/docs
- Status: https://status.render.com
- Support: support@render.com

### Vercel Support
- Docs: https://vercel.com/docs
- Status: https://www.vercel-status.com
- Support: support@vercel.com

### MongoDB Support
- Docs: https://docs.mongodb.com
- Status: https://status.mongodb.com
- Community: https://community.mongodb.com

---

## 🎉 Deployment Complete!

Your AI Healthcare Platform is now live and production-ready!

**Access your platform:**
- Frontend: https://ai-healthcare-frontend.vercel.app
- Backend API: https://api.yourdomain.com
- API Docs: https://api.yourdomain.com/docs

---

**Last Updated**: 2024
**Version**: 1.0.0
