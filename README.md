# 🎬 TubeChat - YouTube AI Chatbot

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

**Chat with any YouTube video using AI-powered semantic search**

[Demo](#-demo) • [Features](#-features) • [Quick Start](#-quick-start) • [Deployment](#-deployment) • [Tech Stack](#-tech-stack)

</div>

---

## 🎥 Demo

### Video Walkthrough

https://github.com/user-attachments/assets/your-video-here

> **Note:** Upload your `tubechat_demo.mp4` to display here, or link to YouTube

### Screenshots

<div align="center">
  <img src="https://via.placeholder.com/800x450/1a1a1a/00ff00?text=TubeChat+Interface" alt="TubeChat Interface" width="800"/>
  <p><i>Replace with actual screenshot</i></p>
</div>

### Try It Out

```bash
git clone https://github.com/Akshadkurundwade07/youtube-chatbot.git
cd youtube-chatbot
docker-compose up
```

Open http://localhost:3000 and chat with any YouTube video!

---

## ✨ Features

- 🎯 **Intelligent Q&A** - Ask questions about any YouTube video
- ⚡ **Lightning Fast** - Powered by Groq's ultra-fast LLM inference
- 🔍 **Semantic Search** - FAISS vector embeddings for accurate retrieval
- 🎨 **Modern UI** - Clean, responsive React interface
- 🐳 **Docker Ready** - One-command deployment
- 🆓 **Free to Run** - Uses free-tier services (Groq, AWS, Render)

---

## 🚀 Quick Start

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (recommended)
- OR Python 3.11+ and Node.js 18+
- [Groq API Key](https://console.groq.com/keys) (free)

### Option 1: Docker (Recommended)

```bash
# 1. Clone repository
git clone https://github.com/Akshadkurundwade07/youtube-chatbot.git
cd youtube-chatbot

# 2. Create .env file
echo "GROQ_API_KEY=your_groq_api_key_here" > .env
echo "VITE_API_URL=http://localhost:8000" >> .env

# 3. Start application
docker-compose up --build

# 4. Open browser
# Frontend: http://localhost:3000
# Backend:  http://localhost:8000/docs
```

### Option 2: Manual Setup

<details>
<summary>Click to expand manual installation steps</summary>

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
export GROQ_API_KEY=your_key_here
uvicorn main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
echo "VITE_API_URL=http://localhost:8000" > .env
npm run dev
```

Open http://localhost:5173

</details>

---

## 📁 Project Structure

```
youtube-chatbot/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── chatbot.py           # RAG logic & LangChain pipeline
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile           # Backend container config
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main React component
│   │   ├── main.jsx         # App entry point
│   │   └── index.css        # Styling
│   ├── package.json         # Node dependencies
│   ├── Dockerfile           # Frontend container config
│   └── nginx.conf           # Production web server config
├── docker-compose.yml       # Multi-container orchestration
├── .env                     # Environment variables (not in git)
└── README.md
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                       User Browser                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (React + Vite)                  │
│                         Port 3000                           │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP Requests
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Backend (FastAPI)                         │
│                      Port 8000                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  1. YouTube Transcript API / yt-dlp                 │   │
│  │  2. Text Splitting (1000 chars, 200 overlap)      │   │
│  │  3. Embeddings (sentence-transformers)            │   │
│  │  4. Vector Store (FAISS)                          │   │
│  │  5. Retrieval (top 4 chunks)                      │   │
│  │  6. LLM (Groq - llama-3.1-8b-instant)            │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🌐 Deployment

### Option 1: AWS EC2 (Free Tier)

Complete guide: [DEPLOY_EC2.md](./DEPLOY_EC2.md)

```bash
# On EC2 instance
git clone https://github.com/Akshadkurundwade07/youtube-chatbot.git
cd youtube-chatbot
echo "GROQ_API_KEY=your_key" > .env
docker-compose up -d
```

**Requirements:**
- EC2 t3.micro instance
- 20 GB EBS volume
- Security groups: ports 3000, 8000

### Option 2: Render.com (Free)

**Backend:**
1. New Web Service → Connect GitHub
2. Build: `pip install -r requirements.txt`
3. Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add env: `GROQ_API_KEY`

**Frontend:**
1. New Static Site → Connect GitHub
2. Build: `npm run build`
3. Publish: `dist`
4. Add env: `VITE_API_URL=<backend-url>`

---

## 🛠️ Tech Stack

### Backend
- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern Python web framework
- **[LangChain](https://langchain.com/)** - LLM orchestration framework
- **[Groq](https://groq.com/)** - Ultra-fast LLM inference (llama-3.1-8b)
- **[FAISS](https://github.com/facebookresearch/faiss)** - Vector similarity search
- **[Sentence Transformers](https://www.sbert.net/)** - Text embeddings (all-MiniLM-L6-v2)
- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** - YouTube transcript extraction

### Frontend
- **[React 18](https://react.dev/)** - UI library
- **[Vite](https://vitejs.dev/)** - Build tool & dev server
- **[Nginx](https://nginx.org/)** - Production web server

### DevOps
- **[Docker](https://www.docker.com/)** - Containerization
- **[Docker Compose](https://docs.docker.com/compose/)** - Multi-container orchestration

---

## 🔧 Configuration

### Environment Variables

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `GROQ_API_KEY` | ✅ Yes | Groq API key for LLM access | - |
| `VITE_API_URL` | ✅ Yes | Backend API URL | `http://localhost:8000` |

### Docker Commands

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Stop services
docker-compose down

# Rebuild after code changes
docker-compose up --build

# Clean everything
docker-compose down -v
docker system prune -a
```

---

## ⚠️ Known Limitations

### YouTube Cloud IP Restrictions

**Issue:** YouTube blocks transcript downloads from cloud IPs (AWS, GCP, Azure) to prevent automated scraping.

| Environment | Status | Details |
|-------------|--------|---------|
| 🏠 Local Development | ✅ Works | Residential IPs are allowed |
| ☁️ Cloud Deployment | ⚠️ Limited | Blocked by YouTube's bot detection |

**Solutions for Production:**

1. **Use YouTube Data API v3** (Recommended)
   - Official API with 10,000 requests/day free
   - Requires Google Cloud API key
   - More reliable for production

2. **Residential Proxy Services** (Paid)
   - Bright Data, Oxylabs, ScraperAPI
   - ~$10-20/month

3. **Alternative Hosting**
   - Railway.app, Fly.io (sometimes work)
   - Home server with static IP

**Note:** This is a platform limitation, not a code issue. Many commercial applications face the same challenge.

---

## 📊 Performance

- **First video load:** 30-60 seconds (model loading + embedding)
- **Subsequent videos:** 10-20 seconds
- **Query response:** 1-3 seconds
- **Memory usage:** ~800MB (t3.micro compatible)

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Groq](https://groq.com/) - Ultra-fast LLM inference
- [LangChain](https://langchain.com/) - LLM orchestration framework
- [Hugging Face](https://huggingface.co/) - Pre-trained embeddings models
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube transcript extraction
- [FAISS](https://github.com/facebookresearch/faiss) - Efficient similarity search

---

## 📧 Contact & Support

- **Author:** Akshad Kurundwade
- **GitHub:** [@Akshadkurundwade07](https://github.com/Akshadkurundwade07)
- **Project:** [youtube-chatbot](https://github.com/Akshadkurundwade07/youtube-chatbot)

**Found a bug?** [Open an issue](https://github.com/Akshadkurundwade07/youtube-chatbot/issues)

**Have questions?** [Start a discussion](https://github.com/Akshadkurundwade07/youtube-chatbot/discussions)

---

<div align="center">

**⭐ Star this repo if you found it helpful!**

Made with ❤️ using React, FastAPI, and Groq

</div>
