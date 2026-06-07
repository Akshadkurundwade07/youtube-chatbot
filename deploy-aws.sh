#!/bin/bash

# AWS Deployment Script for YouTube Chatbot
# Usage: ./deploy-aws.sh

set -e

# Configuration
AWS_REGION="us-east-1"
AWS_ACCOUNT_ID="YOUR_AWS_ACCOUNT_ID"
BACKEND_REPO="youtube-chatbot-backend"
FRONTEND_REPO="youtube-chatbot-frontend"

echo "🚀 Starting AWS Deployment..."

# Step 1: Login to ECR
echo "📦 Logging into AWS ECR..."
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# Step 2: Build images
echo "🔨 Building Docker images..."
docker build -t $BACKEND_REPO:latest ./backend
docker build -t $FRONTEND_REPO:latest ./frontend

# Step 3: Tag images
echo "🏷️  Tagging images..."
docker tag $BACKEND_REPO:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$BACKEND_REPO:latest
docker tag $FRONTEND_REPO:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$FRONTEND_REPO:latest

# Step 4: Push to ECR
echo "⬆️  Pushing images to ECR..."
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$BACKEND_REPO:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$FRONTEND_REPO:latest

echo "✅ Deployment complete!"
echo "📝 Next: Update ECS service to use new images"
