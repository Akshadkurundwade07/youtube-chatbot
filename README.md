# TubeChat — YouTube AI Chatbot

Chat with any YouTube video using Groq + LangChain + FAISS.

## Project Structure

```
youtube-chatbot/
├── backend/
│   ├── main.py          # FastAPI app
│   ├── chatbot.py       # Core RAG logic (from your notebook)
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── App.jsx
    │   ├── main.jsx
    │   └── index.css
    ├── index.html
    ├── package.json
    └── vite.config.js
```

---

## Run Locally

### Option 1: Docker (Recommended) 🐳

**Prerequisites:**
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- Your Groq API key

**Steps:**

1. **Clone or navigate to the project:**
   ```bash
   cd youtube-chatbot
   ```

2. **Create/verify `.env` file** in the root directory:
   ```bash
   GROQ_API_KEY=your_groq_api_key_here
   VITE_API_URL=http://localhost:8000
   ```

3. **Build and start containers:**
   ```bash
   docker-compose up --build
   ```
   
   First build takes 2-3 minutes. Subsequent starts are faster.

4. **Access the application:**
   - 🌐 **Frontend:** http://localhost:3000
   - 🔌 **Backend API:** http://localhost:8000
   - 📚 **API Docs:** http://localhost:8000/docs

5. **Stop the application:**
   ```bash
   # Press Ctrl+C, then:
   docker-compose down
   ```

**Useful Docker Commands:**
```bash
# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Rebuild after code changes
docker-compose up --build

# Remove everything (clean slate)
docker-compose down -v
```

---

### Option 2: Manual Setup

#### Backend
```bash
cd backend
pip install -r requirements.txt
export GROQ_API_KEY=your_key_here  # Windows: set GROQ_API_KEY=your_key_here
uvicorn main:app --reload --port 8000
```

#### Frontend
```bash
cd frontend
npm install
# Create .env file:
echo "VITE_API_URL=http://localhost:8000" > .env
npm run dev
```

Open http://localhost:5173

---

## Deploy for Free

### Backend → Render.com

1. Push `backend/` folder to a GitHub repo
2. Go to https://render.com → **New Web Service**
3. Connect your GitHub repo
4. Set these values:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment Variable:** `GROQ_API_KEY = your_key_here`
5. Click **Deploy**
6. Copy your live URL e.g. `https://tubechat-api.onrender.com`

### Frontend → Vercel.com

1. Push `frontend/` folder to a GitHub repo
2. Go to https://vercel.com → **Add New Project**
3. Import your repo
4. Add environment variable:
   - `VITE_API_URL = https://tubechat-api.onrender.com`
5. Click **Deploy**
6. Your app is live at `https://your-app.vercel.app` ✅

---

## How It Works

1. User pastes a YouTube URL or video ID
2. Backend downloads VTT subtitles via yt-dlp
3. Transcript is split into chunks (1000 chars, 200 overlap)
4. Chunks are embedded with `all-MiniLM-L6-v2` (free, local)
5. Stored in FAISS vector store
6. User asks a question → top 4 relevant chunks retrieved
7. Groq `llama-3.1-8b-instant` answers using only the transcript context

---

## Docker Architecture

```
┌─────────────────────────────────────────┐
│         Docker Compose Network          │
│                                         │
│  ┌──────────────┐    ┌──────────────┐  │
│  │   Frontend   │    │   Backend    │  │
│  │              │    │              │  │
│  │ React + Vite │───▶│   FastAPI    │  │
│  │   + Nginx    │    │  + Python    │  │
│  │              │    │              │  │
│  │  Port 3000   │    │  Port 8000   │  │
│  └──────────────┘    └──────────────┘  │
│                                         │
└─────────────────────────────────────────┘
         ▲                      ▲
         │                      │
    Browser (You)          API Requests
```

**Frontend Container:**
- Multi-stage build (Node.js → Nginx)
- Serves optimized static files
- ~25MB final image

**Backend Container:**
- Python 3.11 + FastAPI
- Includes ffmpeg for yt-dlp
- Handles video processing & AI

---

## Troubleshooting

### Docker Issues

**Port already in use:**
```bash
# Edit docker-compose.yml and change ports:
ports:
  - "3001:80"   # Frontend
  - "8001:8000" # Backend
```

**Build fails:**
```bash
docker-compose down -v
docker system prune -a
docker-compose up --build
```

**Can't connect to backend:**
```bash
# Check if containers are running
docker ps

# View logs
docker-compose logs backend
docker-compose logs frontend
```

### Application Issues

**"Video not loaded" error:**
- Make sure you clicked "Load" first
- Check if video has captions/subtitles
- View backend logs: `docker-compose logs backend`

**API key error:**
- Verify `.env` file has `GROQ_API_KEY=your_actual_key`
- Restart containers: `docker-compose restart`

---

## Environment Variables

| Variable | Location | Description |
|----------|----------|-------------|
| `GROQ_API_KEY` | Root `.env` | Your Groq API key (required) |
| `VITE_API_URL` | Root `.env` | Backend URL for frontend (default: `http://localhost:8000`) |

---

## Tech Stack

**Backend:**
- FastAPI - Modern Python web framework
- LangChain - LLM orchestration
- Groq - Ultra-fast LLM inference
- FAISS - Vector similarity search
- yt-dlp - YouTube transcript extraction

**Frontend:**
- React 18 - UI framework
- Vite - Build tool
- Nginx - Production web server

**DevOps:**
- Docker - Containerization
- Docker Compose - Multi-container orchestration
