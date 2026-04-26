# 🏥 AI Healthcare Chatbot - Visual Quick Reference

## 📊 System Architecture Diagram

```
┌────────────────────────────────────────────────────────────────────────┐
│                          USER INTERFACE                                │
│                      (React Frontend - Port 3000)                      │
│  ┌──────────────┬──────────────┬──────────────┬──────────────────────┐ │
│  │  🧠 Chat    │  📊 Insights │  🔒 Security │  ⚙️  Settings       │ │
│  │              │              │              │                      │ │
│  │ • Messages   │ • Charts     │ • Encryption │ • Dark Mode         │ │
│  │ • Feedback   │ • Analytics  │ • DB Status  │ • Data Retention    │ │
│  │ • History    │ • Trends     │ • Privacy    │ • Clear History     │ │
│  └──────────────┴──────────────┴──────────────┴──────────────────────┘ │
└────────────────┬─────────────────────────────────────────────────────────┘
                 │ Encrypted HTTPS
                 ↓
┌────────────────────────────────────────────────────────────────────────┐
│                    BACKEND API SERVER                                  │
│                   (FastAPI - Port 8000)                                │
│  ┌────────────────────────────────────────────────────────────────┐   │
│  │  Routes & Controllers                                          │   │
│  │  • /chat         • /feedback      • /history                  │   │
│  │  • /insights     • /security      • /settings                 │   │
│  │  • /health       • /rl-stats      • /rl-recommendations       │   │
│  └────────────────────────────────────────────────────────────────┘   │
│                                                                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │
│  │ 🤖 LLM       │  │ 🧬 Medical   │  │ 🧠 Learning  │               │
│  │ Service      │  │ Service      │  │ Service      │               │
│  │              │  │              │  │              │               │
│  │ LLaMA 3      │  │ BioBERT      │  │ RL Feedback  │               │
│  │ (Groq API)   │  │ (NER)        │  │ System       │               │
│  └──────────────┘  └──────────────┘  └──────────────┘               │
│                                                                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │
│  │ 🔐 Encryption│  │ 💾 Database  │  │ ⚙️ Config   │               │
│  │ Service      │  │ Service      │  │              │               │
│  │              │  │              │  │ Settings &   │               │
│  │ AES-256      │  │ MongoDB Ops  │  │ Validation   │               │
│  └──────────────┘  └──────────────┘  └──────────────┘               │
└────────────────┬─────────────────────────────────────────────────────┘
                 │                         │
                 │ LLM Calls              │ MongoDB
                 ↓                         ↓
    ┌──────────────────┐      ┌────────────────────────┐
    │  EXTERNAL APIs   │      │  CLOUD DATABASE        │
    │                  │      │  MongoDB Atlas         │
    │  • Groq (Groq)   │      │                        │
    │  • HuggingFace   │      │  Collections:          │
    │  • Transformers  │      │  • chat_history        │
    └──────────────────┘      │  • feedback            │
                              │  • sessions            │
                              │  • users               │
                              └────────────────────────┘
```

---

## 🔄 Data Flow Diagram

```
USER INPUT
    ↓
┌─────────────────────┐
│ User sends message  │
│ "I have fever"      │
└──────┬──────────────┘
       ↓
┌──────────────────────────────┐
│ Frontend receives message    │
│ Displays as chat bubble      │
└──────┬───────────────────────┘
       ↓
┌──────────────────────────────────┐
│ Send to Backend API              │
│ POST /chat                       │
│ {content, user_id}              │
└──────┬───────────────────────────┘
       ↓
┌──────────────────────────────────┐
│ Backend: Encrypt message         │
│ AES-256 encryption               │
└──────┬───────────────────────────┘
       ↓
┌──────────────────────────────────┐
│ Backend: Detect Intent           │
│ Healthcare? Yes → Special mode   │
└──────┬───────────────────────────┘
       ↓
    ┌──┴─┬──────────────────────────────┐
    │    │                              │
    ↓    ↓                              ↓
┌─────────┐                       ┌─────────────┐
│ BioBERT │ Analyze               │ LLaMA 3     │
│ Extract │ Symptoms:             │ Generate    │
│ Symptoms│ • Fever               │ Response    │
│         │ • Malaise             │             │
└────┬────┘                       └────┬────────┘
     │                                 │
     └──────────┬──────────────────────┘
                ↓
        ┌──────────────────┐
        │ Predict Likely   │
        │ Conditions:      │
        │ • Flu (85%)      │
        │ • Cold (60%)     │
        │ • COVID (40%)    │
        └────────┬─────────┘
                 ↓
        ┌──────────────────────────────┐
        │ Encrypt Response             │
        │ Store in MongoDB (encrypted) │
        └────────┬─────────────────────┘
                 ↓
        ┌──────────────────────────────┐
        │ Send Response to Frontend    │
        │ Include symptoms & conditions│
        └────────┬─────────────────────┘
                 ↓
        ┌──────────────────────────────┐
        │ Frontend Shows Response      │
        │ Display symptoms             │
        │ Display conditions           │
        │ Show disclaimer              │
        └────────┬─────────────────────┘
                 ↓
        ┌──────────────────────────────┐
        │ User Rates Response          │
        │ Helpful? Yes (👍)            │
        │ or No (👎)                   │
        └────────┬─────────────────────┘
                 ↓
        ┌──────────────────────────────┐
        │ Send Feedback to Backend     │
        │ POST /feedback               │
        │ {message_id, is_helpful}     │
        └────────┬─────────────────────┘
                 ↓
        ┌──────────────────────────────┐
        │ RL System Learns             │
        │ +1 score for helpful         │
        │ -1 score for not helpful     │
        │ Update category performance  │
        └────────┬─────────────────────┘
                 ↓
        ┌──────────────────────────────┐
        │ System Improves              │
        │ Better responses next time   │
        │ Success rate: 85%            │
        └──────────────────────────────┘
```

---

## 🎯 Feature Implementation Map

```
┌─────────────────────────────────────────────────────────┐
│                   CHAT TAB (Messaging)                  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Components:                                           │
│  ✅ Message display (user + AI)                        │
│  ✅ Input textbox                                      │
│  ✅ Send button                                        │
│  ✅ Feedback buttons (👍 👎)                           │
│  ✅ Typing indicator                                   │
│  ✅ Clear history button                               │
│                                                         │
│  Features:                                             │
│  ✅ Real-time messaging                                │
│  ✅ Symptom detection                                  │
│  ✅ Healthcare mode toggle                             │
│  ✅ Condition prediction                               │
│  ✅ Smooth animations                                  │
│  ✅ Message encryption                                 │
│  ✅ Error handling                                     │
│  ✅ Loading states                                     │
│                                                         │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│              INSIGHTS TAB (Analytics)                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Metrics:                                              │
│  ✅ Total conversations                                │
│  ✅ Success rate                                       │
│  ✅ Helpful responses count                            │
│  ✅ Learning progress                                  │
│                                                         │
│  Charts:                                               │
│  ✅ Symptom frequency (Bar chart)                      │
│  ✅ Condition distribution (Pie chart)                 │
│  ✅ Feedback trends (Line chart)                       │
│  ✅ Learning insights (Text summary)                   │
│                                                         │
│  Data Sources:                                         │
│  ✅ MongoDB aggregation                                │
│  ✅ RL system statistics                               │
│  ✅ Real-time updates                                  │
│                                                         │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│              SECURITY TAB (Trust & Safety)              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Security Status:                                      │
│  ✅ Encryption enabled (AES-256)                       │
│  ✅ Database connection status                         │
│  ✅ API security indicators                            │
│  ✅ Trust score display                                │
│                                                         │
│  Information:                                          │
│  ✅ Encryption details & implementation                │
│  ✅ Data handling policy                               │
│  ✅ Privacy protection measures                        │
│  ✅ HIPAA compliance notes                             │
│  ✅ User privacy tips                                  │
│  ✅ Medical disclaimer (prominent)                     │
│                                                         │
│  Visual Elements:                                      │
│  ✅ Lock icons                                         │
│  ✅ Status indicators                                  │
│  ✅ Color coding (green=secure)                        │
│  ✅ Trust badges                                       │
│                                                         │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│              SETTINGS TAB (Customization)               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Appearance:                                           │
│  ✅ Dark mode toggle                                   │
│  ✅ Real-time theme switching                          │
│                                                         │
│  Privacy & Security:                                   │
│  ✅ Notifications toggle                               │
│  ✅ Data retention slider (7-90 days)                  │
│  ✅ Clear history with confirmation                    │
│                                                         │
│  Account Info:                                         │
│  ✅ User ID display                                    │
│  ✅ Version information                                │
│  ✅ Account status                                     │
│                                                         │
│  Support:                                              │
│  ✅ Help & support section                             │
│  ✅ Documentation links                                │
│  ✅ Contact information                                │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🧠 AI Pipeline Diagram

```
USER INPUT: "I have fever, cough, and body aches"
    ↓
┌──────────────────────────────┐
│ Intent Detection             │
│ Keywords: fever, cough, ache │
│ Result: HEALTHCARE MODE      │
└──────┬───────────────────────┘
       ↓
┌──────────────────────────────┐
│ BioBERT Symptom Extraction   │
│                              │
│ Input: Full message          │
│ Process: NLP analysis        │
│ Output:                      │
│ • Symptom 1: fever           │
│ • Symptom 2: cough           │
│ • Symptom 3: body aches      │
└──────┬───────────────────────┘
       ↓
┌──────────────────────────────┐
│ Condition Prediction         │
│                              │
│ Input: [fever, cough, aches] │
│ Matching:                    │
│ • Flu: 85%                   │
│ • Cold: 65%                  │
│ • COVID: 45%                 │
│ • Bronchitis: 40%            │
│ Top 3: Return                │
└──────┬───────────────────────┘
       ↓
┌──────────────────────────────┐
│ LLaMA 3 Response Generation  │
│                              │
│ System prompt:               │
│ "You are healthcare AI..."   │
│                              │
│ Context:                     │
│ • Symptoms detected          │
│ • Conditions predicted       │
│ • User input                 │
│                              │
│ Output: Natural response     │
│ with recommendations         │
└──────┬───────────────────────┘
       ↓
RESPONSE: "I understand you have fever, cough,
and body aches. These are common symptoms of
flu or a cold. Please ensure you get rest,
stay hydrated, and monitor your temperature.
If symptoms persist beyond 7 days or worsen,
please consult a healthcare provider..."
```

---

## 🔐 Encryption Flow

```
PLAINTEXT MESSAGE
    ↓
"I have severe pain in my chest"
    ↓
┌─────────────────────────────────────┐
│ Encryption Service (AES-256)        │
│                                     │
│ 1. Convert to bytes                │
│ 2. Encrypt with key                │
│ 3. Base64 encode                   │
│ 4. Return ciphertext               │
└────────┬────────────────────────────┘
         ↓
ENCRYPTED CIPHERTEXT
         ↓
"gAAAAABl4r...XyZ9kL8="
         ↓
    STORE IN DB
         ↓
┌─────────────────────────────────────┐
│ Later: Decrypt on Demand            │
│                                     │
│ 1. Get encrypted from DB            │
│ 2. Base64 decode                   │
│ 3. Decrypt with key                │
│ 4. Convert to string               │
│ 5. Return plaintext (only in RAM)  │
└────────┬────────────────────────────┘
         ↓
PLAINTEXT IN MEMORY (Temporarily)
         ↓
"I have severe pain in my chest"
         ↓
Display to user (then discarded)
```

---

## 📊 Database Schema

```
MongoDB Collections
│
├── chat_history
│   ├── _id: ObjectId
│   ├── user_id: string
│   ├── message: string (encrypted)
│   ├── response: string (encrypted)
│   ├── encrypted: boolean
│   ├── timestamp: datetime
│   ├── feedback: string (optional)
│   └── score: number (optional)
│   Indexes:
│   • (user_id, timestamp DESC)
│   • (encrypted)
│
├── feedback
│   ├── _id: ObjectId
│   ├── user_id: string
│   ├── message_id: string
│   ├── feedback: string
│   ├── score: number (-1 or 1)
│   ├── category: string
│   └── timestamp: datetime
│   Indexes:
│   • (user_id, timestamp DESC)
│   • (message_id)
│
├── sessions
│   ├── _id: ObjectId
│   ├── user_id: string
│   ├── created_at: datetime
│   ├── updated_at: datetime
│   └── metadata: object
│   Indexes:
│   • (user_id)
│   • (created_at)
│
└── users
    ├── _id: ObjectId
    ├── user_id: string (unique)
    ├── created_at: datetime
    ├── preferences: object
    │   ├── dark_mode: boolean
    │   ├── notifications: boolean
    │   └── data_retention_days: number
    └── last_active: datetime
    Indexes:
    • (user_id) - unique
```

---

## 📈 Learning Flow Diagram

```
FEEDBACK COLLECTION
         ↓
    Response: "Helpful"
         ↓
┌────────────────────────────┐
│ RL Feedback Processing     │
│                            │
│ Score: +1                 │
│ Category: healthcare      │
│ Timestamp: recorded       │
│ Store in feedback DB      │
└────────┬───────────────────┘
         ↓
┌────────────────────────────┐
│ Performance Analysis       │
│                            │
│ Calculate:                │
│ • Total feedback: 50      │
│ • Helpful: 42 (84%)      │
│ • Not helpful: 8 (16%)   │
│ • Success rate: 84%      │
└────────┬───────────────────┘
         ↓
┌────────────────────────────┐
│ Category Performance       │
│                            │
│ Healthcare: 88%           │
│ General: 75%              │
│ Low priority: 45%         │
└────────┬───────────────────┘
         ↓
┌────────────────────────────┐
│ Generate Recommendations   │
│                            │
│ • Focus on low priority    │
│ • Improve healthcare mode  │
│ • Keep general strong      │
└────────┬───────────────────┘
         ↓
┌────────────────────────────┐
│ System Adjusts             │
│                            │
│ • Better response tuning   │
│ • More confident replies   │
│ • Focused improvements     │
└────────┬───────────────────┘
         ↓
NEXT ITERATION (Improved Responses)
```

---

## 🎬 Component Rendering Diagram

```
App Component
    │
    ├─ Header
    │  ├─ Logo & Title
    │  ├─ Connection Status
    │  └─ Dark Mode Toggle
    │
    ├─ Tab Navigation
    │  ├─ Chat (Icon + Label)
    │  ├─ Insights (Icon + Label)
    │  ├─ Security (Icon + Label)
    │  └─ Settings (Icon + Label)
    │
    ├─ Active Tab Content (Animated)
    │  │
    │  ├─ IF activeTab === 'chat'
    │  │  └─ ChatTab
    │  │     ├─ Messages Container
    │  │     │  ├─ User Message Bubbles
    │  │     │  ├─ AI Message Bubbles
    │  │     │  ├─ Healthcare Info Panel
    │  │     │  └─ Feedback Buttons
    │  │     ├─ Loading Animation
    │  │     └─ Input Area
    │  │
    │  ├─ IF activeTab === 'insights'
    │  │  └─ InsightsTab
    │  │     ├─ Stat Cards
    │  │     ├─ Bar Chart
    │  │     ├─ Pie Chart
    │  │     ├─ Line Chart
    │  │     └─ Learning Info Card
    │  │
    │  ├─ IF activeTab === 'security'
    │  │  └─ SecurityTab
    │  │     ├─ Status Card
    │  │     ├─ Feature Cards
    │  │     ├─ Encryption Details
    │  │     ├─ Data Policy
    │  │     └─ Disclaimer
    │  │
    │  └─ IF activeTab === 'settings'
    │     └─ SettingsTab
    │        ├─ Appearance Section
    │        ├─ Privacy Section
    │        ├─ Data Management Section
    │        ├─ Account Section
    │        └─ Support Section
    │
    └─ Footer
       ├─ Medical Disclaimer
       └─ Version Info
```

---

## 🌐 Environment Variables Reference

```
BACKEND CONFIGURATION
├─ GROQ_API_KEY              API key for LLaMA 3
├─ HUGGINGFACE_API_KEY       Token for BioBERT
├─ MONGODB_URI               Database connection string
├─ ENCRYPTION_KEY            AES-256 encryption key (32 bytes hex)
├─ DEBUG                     True for development, False for production
├─ PORT                      Server port (default: 8000)
└─ HOST                      Server host (default: 0.0.0.0)

FRONTEND CONFIGURATION
└─ VITE_API_URL              Backend URL (default: http://localhost:8000)

PRODUCTION CONFIGURATION
├─ For Render:              Set DEBUG=False
├─ For Vercel:              Set VITE_API_URL=production API URL
└─ For MongoDB:             Whitelist production server IPs
```

---

## 📱 Responsive Design Breakpoints

```
Mobile (< 640px)
├─ Single column layout
├─ Stack all cards vertically
├─ Full-width buttons
└─ Optimized touch targets

Tablet (640px - 1024px)
├─ 2-column layout where applicable
├─ Adjust font sizes
├─ Grid adjustments
└─ Balanced spacing

Desktop (> 1024px)
├─ Multi-column layout
├─ Full feature display
├─ Side-by-side panels
└─ Optimal spacing

Dark Mode
├─ All colors inverted
├─ Higher contrast for accessibility
├─ Reduced brightness
└─ Eye-friendly design
```

---

## ✅ Deployment Checklist

```
Pre-Deployment
├─ [ ] All dependencies in requirements.txt
├─ [ ] All npm packages in package.json
├─ [ ] .env files with all keys
├─ [ ] Database initialized
├─ [ ] Tests passing locally
└─ [ ] Code committed to GitHub

Backend Deployment (Render)
├─ [ ] Create Render account
├─ [ ] Connect GitHub repository
├─ [ ] Set build command
├─ [ ] Set start command
├─ [ ] Add environment variables
├─ [ ] Deploy and test
└─ [ ] Verify API endpoints

Frontend Deployment (Vercel)
├─ [ ] Create Vercel account
├─ [ ] Import GitHub project
├─ [ ] Set build command
├─ [ ] Set output directory
├─ [ ] Add environment variables
├─ [ ] Deploy and test
└─ [ ] Verify UI works

Post-Deployment
├─ [ ] Test all features on production
├─ [ ] Monitor error logs
├─ [ ] Set up alerts
├─ [ ] Configure custom domain
├─ [ ] Set up backups
└─ [ ] Document deployment details
```

---

**This visual guide complements the technical documentation. For detailed setup, see SETUP_GUIDE.md. For deployment, see DEPLOYMENT.md.**

Built with ❤️ for healthcare innovation
