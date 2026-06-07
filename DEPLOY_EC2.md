# 🚀 EC2 Deployment Guide

## Prerequisites
- AWS EC2 t3.micro instance (Free Tier)
- **20 GB EBS volume minimum**
- Security Groups: Ports 22, 3000, 8000

## Quick Deploy

```bash
# On EC2
git clone https://github.com/Akshadkurundwade07/youtube-chatbot.git
cd youtube-chatbot

# Set your API key
export GROQ_API_KEY=your_api_key_here

# Run deployment script
chmod +x deploy.sh
./deploy.sh
```

## Access
- Frontend: http://YOUR_EC2_IP:3000
- Backend: http://YOUR_EC2_IP:8000
