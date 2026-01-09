# 🚀 Full Stack Setup Guide

Complete setup instructions for the Interview Agent with Next.js frontend and FastAPI backend.

## Architecture Overview

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│   Next.js       │  HTTP   │   FastAPI        │  Code   │   LangGraph     │
│   Frontend      ├────────►│   Backend        ├────────►│   Evaluation    │
│   (Port 3000)   │         │   (Port 8000)    │         │   Engine        │
│                 │         │                  │         │                 │
│                 │  WS     │                  │         │   (Existing     │
│                 ├────────►│   WebSocket      │         │    src/graph/)  │
│                 │         │   Real-time      │         │                 │
└─────────────────┘         └──────────────────┘         └─────────────────┘
```

## Prerequisites

- **Python 3.10+**
- **Node.js 18+** and npm
- **Azure OpenAI API credentials** (already configured in `.env`)

---

## 🔧 Backend Setup (FastAPI)

### 1. Install Dependencies

```bash
cd backend
pip install fastapi uvicorn[standard] python-multipart pydantic-settings
```

The backend reuses all existing dependencies from your root `requirements.txt` (langchain, langgraph, openai, etc.)

### 2. Start the Backend Server

```bash
cd backend
python run.py
```

You should see:
```
🚀 Interview Agent API started
📚 API docs: http://localhost:8000/docs
🔌 WebSocket: ws://localhost:8000/ws/evaluations/{evaluation_id}
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 3. Test Backend (Optional)

Visit http://localhost:8000/docs to see the interactive API documentation.

Test health check:
```bash
curl http://localhost:8000/api/v1/health
```

---

## 🎨 Frontend Setup (Next.js)

### 1. Install Dependencies

Open a **NEW terminal** (keep backend running):

```bash
cd frontend
npm install
```

This will install all Next.js, React, Tailwind, shadcn/ui, and other frontend dependencies.

### 2. Start the Frontend Server

```bash
cd frontend
npm run dev
```

You should see:
```
  ▲ Next.js 14.2.0
  - Local:        http://localhost:3000
  - Ready in 2.3s
```

---

## ✨ Using the Application

### 1. Open the App

Visit **http://localhost:3000** in your browser.

### 2. Fill Out the Evaluation Form

**Candidate Information:**
- Name: e.g., "Sarah Chen"
- Current Level: e.g., "L5 PM"
- Target Level: e.g., "L6 Senior PM"
- Years at Current Level: e.g., 3
- Level Expectations: Describe what distinguishes the target level

**Evaluation Rubric:**
Write your criteria in plain English:
```markdown
## Strategic Thinking
- Demonstrates long-term vision beyond immediate roadmap
- Makes decisions considering broader organizational impact

## Leadership & Influence
- Influences without authority across teams
- Builds consensus among stakeholders
```

**Interview Transcript:**
Either paste text directly or upload a .txt/.md file with the interview transcript.

### 3. Run the Evaluation

Click **"Run Evaluation"** button. You'll be redirected to the results page where you'll see:

- **Real-time progress bar** (0% → 25% → 50% → 75% → 100%)
- **4 agent status cards** updating live
- **WebSocket connection status**
- **Live token counts** as agents complete

### 4. View Results

Once complete (typically 2-3 minutes), you'll see:

- **Recommendation badge** (STRONG RECOMMEND / RECOMMEND / BORDERLINE / DO NOT RECOMMEND)
- **Metrics**: Execution time, total tokens, cost, model version
- **Evaluation Journey**: 4-panel accordion showing:
  1. Primary Evaluation
  2. Peer Challenges
  3. Calibrated Response
  4. Final Decision

---

## 🏗️ Project Structure

```
Interview Agent/
├── backend/                          # FastAPI Backend
│   ├── app/
│   │   ├── main.py                   # FastAPI entry point
│   │   ├── models/                   # Pydantic schemas
│   │   ├── services/                 # Business logic
│   │   ├── api/
│   │   │   ├── routes/               # REST endpoints
│   │   │   └── websocket/            # WebSocket handlers
│   │   └── utils/                    # Graph executor
│   ├── run.py                        # Server runner
│   └── requirements.txt              # Backend dependencies
│
├── frontend/                         # Next.js Frontend
│   ├── src/
│   │   ├── app/                      # Pages (App Router)
│   │   │   ├── page.tsx              # Home (evaluation form)
│   │   │   └── evaluations/[id]/     # Results page
│   │   ├── components/
│   │   │   ├── ui/                   # shadcn/ui components
│   │   │   ├── evaluation/           # Evaluation components
│   │   │   └── shared/               # Shared components
│   │   ├── lib/
│   │   │   ├── api/                  # API client
│   │   │   ├── websocket/            # WebSocket hook
│   │   │   └── validation/           # Zod schemas
│   │   └── types/                    # TypeScript types
│   ├── package.json
│   └── README.md
│
├── src/                              # Existing LangGraph Code (REUSED!)
│   ├── graph/
│   │   ├── graph.py                  # LangGraph workflow
│   │   ├── nodes.py                  # 4-agent implementations
│   │   └── state.py                  # State definitions
│   ├── prompts/
│   │   └── manager.py                # Prompt versioning
│   └── utils/
│       └── azure_client.py           # Azure OpenAI client
│
├── data/                             # Prompts and rubrics
├── config.yaml                       # Model configuration
├── .env                              # Azure OpenAI credentials
└── requirements.txt                  # Python dependencies
```

---

## 🔍 How It Works

1. **User submits form** → POST /api/v1/evaluations
2. **Backend validates** → Creates evaluation ID, starts background task
3. **Frontend redirects** → /evaluations/{id} page
4. **WebSocket connects** → ws://localhost:8000/ws/evaluations/{id}
5. **LangGraph executes** → Your existing 4-agent workflow from `src/graph/graph.py`
6. **Real-time updates** → Backend streams progress events via WebSocket
7. **Frontend updates** → Progress bar, agent cards update live
8. **Evaluation completes** → Full results displayed with beautiful UI

---

## 🛠️ Troubleshooting

### Backend won't start

**Error**: `ModuleNotFoundError: No module named 'fastapi'`
**Solution**:
```bash
cd backend
pip install fastapi uvicorn[standard] python-multipart pydantic-settings
```

### Frontend won't start

**Error**: `Cannot find module 'next'`
**Solution**:
```bash
cd frontend
npm install
```

### WebSocket not connecting

**Check**:
1. Backend is running on port 8000
2. Frontend is configured to connect to `ws://localhost:8000`
3. No firewall blocking WebSocket connections

### Evaluation fails with Azure OpenAI error

**Check**:
1. `.env` file has correct `AZURE_OPENAI_API_KEY` and `AZURE_OPENAI_ENDPOINT`
2. API key is valid and has credits
3. Backend logs show the error details

---

## 📊 API Endpoints

### REST API

- `POST /api/v1/evaluations` - Create evaluation
- `GET /api/v1/evaluations/{id}` - Get evaluation status
- `GET /api/v1/evaluations` - List evaluations
- `GET /api/v1/health` - Health check

### WebSocket

- `ws://localhost:8000/ws/evaluations/{id}` - Real-time progress stream

Interactive API docs: http://localhost:8000/docs

---

## 🎯 Next Steps

### Enhancements

1. **History Page**: View past evaluations
2. **Prompt Editor**: UI for managing prompt versions
3. **Authentication**: Add user login
4. **Database**: Replace in-memory storage with PostgreSQL/Redis
5. **Export Reports**: Download PDF evaluations

### Deployment

1. **Backend**: Deploy to AWS/GCP/Azure (containerize with Docker)
2. **Frontend**: Deploy to Vercel/Netlify (automatic with Next.js)
3. **Production Config**: Update CORS origins, add HTTPS

---

## 🙌 Summary

You now have a complete full-stack AI evaluation system:

✅ **Backend**: FastAPI with WebSocket streaming
✅ **Frontend**: Beautiful Next.js UI with shadcn/ui
✅ **Real-time**: Live progress updates
✅ **Existing Code**: Reuses your LangGraph evaluation engine
✅ **Type-safe**: TypeScript + Pydantic throughout

**Run both servers and visit http://localhost:3000 to start evaluating!** 🚀
