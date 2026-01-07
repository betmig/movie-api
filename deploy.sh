#!/bin/bash

# Movie API Quick Deployment Script
# Run this on your LOCAL machine after setting up SSH access

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
SERVER_USER="betmig"
SERVER_HOST=""  # Set your server IP
SSH_PORT="2222"
DEPLOY_PATH="/docker/movie-api"

echo -e "${GREEN}Movie API Deployment Script${NC}"
echo "================================"

# Check if server host is set
if [ -z "$SERVER_HOST" ]; then
    read -p "Enter your server IP address: " SERVER_HOST
fi

echo -e "\n${YELLOW}Step 1: Copying database to server...${NC}"
scp -P $SSH_PORT db.sqlite3 ${SERVER_USER}@${SERVER_HOST}:${DEPLOY_PATH}/ || echo "Database already on server or copy failed"

echo -e "\n${YELLOW}Step 2: Pulling latest code...${NC}"
ssh -p $SSH_PORT ${SERVER_USER}@${SERVER_HOST} "cd ${DEPLOY_PATH} && git pull"

echo -e "\n${YELLOW}Step 3: Building and starting container...${NC}"
ssh -p $SSH_PORT ${SERVER_USER}@${SERVER_HOST} "cd ${DEPLOY_PATH} && docker compose down && docker compose up -d --build"

echo -e "\n${YELLOW}Step 4: Checking container status...${NC}"
ssh -p $SSH_PORT ${SERVER_USER}@${SERVER_HOST} "docker ps | grep movie-api"

echo -e "\n${GREEN}Deployment complete!${NC}"
echo -e "\n${YELLOW}Useful commands:${NC}"
echo "  View logs:    ssh -p $SSH_PORT ${SERVER_USER}@${SERVER_HOST} 'docker logs movie-api'"
echo "  Restart:      ssh -p $SSH_PORT ${SERVER_USER}@${SERVER_HOST} 'cd ${DEPLOY_PATH} && docker compose restart'"
echo "  Shell access: ssh -p $SSH_PORT ${SERVER_USER}@${SERVER_HOST} 'docker exec -it movie-api bash'"
