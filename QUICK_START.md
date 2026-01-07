# Quick Start Deployment

## Step 1: Set Up GitHub Access on Server

```bash
# SSH into your server
ssh -p 2222 betmig@YOUR_SERVER_IP

# Generate SSH key for GitHub
ssh-keygen -t ed25519 -C "movie-api-deploy" -f ~/.ssh/movie_api_deploy

# Display public key (copy this)
cat ~/.ssh/movie_api_deploy.pub
```

**Add the key to GitHub:**
1. Copy the public key output
2. Go to your GitHub repo → Settings → Deploy keys
3. Click "Add deploy key"
4. Paste the key, title it "VPS Deploy Key"
5. Click "Add key"

## Step 2: Clone and Deploy

```bash
# Still on server - configure git to use the SSH key
cat > ~/.ssh/config << 'EOL'
Host github.com-movie-api
    HostName github.com
    User git
    IdentityFile ~/.ssh/movie_api_deploy
    IdentitiesOnly yes
EOL

# Create project directory
mkdir -p /docker/movie-api
cd /docker/movie-api

# Clone your repository (replace YOUR_USERNAME/YOUR_REPO)
git clone git@github.com-movie-api:YOUR_USERNAME/YOUR_REPO.git .

# Alternative: if using HTTPS instead
# git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git .

# Copy your database file (if you have one locally)
# From LOCAL machine:
scp -P 2222 db.sqlite3 betmig@YOUR_SERVER_IP:/docker/movie-api/

# Build and start
docker compose up -d --build
```

## Step 3: Configure Nginx Proxy Manager

1. Go to `http://YOUR_SERVER_IP:81`
2. Add Proxy Host:
   - **Domain**: `movieapi.betmig.link`
   - **Forward to**: `movie-api` port `8000`
   - **Enable SSL**: Yes (Let's Encrypt)

## Step 4: Test Your API

```bash
curl https://movieapi.betmig.link/api/movies/
```

## Step 5: Set Up Auto-Deploy (Optional)

Add GitHub Secrets to enable auto-deployment on every push:

1. Go to your GitHub repo → Settings → Secrets and variables → Actions
2. Add these secrets:
   - `SERVER_HOST`: Your server IP address
   - `SERVER_USERNAME`: `betmig`
   - `SSH_PRIVATE_KEY`: Content of `~/.ssh/movie_api_deploy` (run `cat ~/.ssh/movie_api_deploy` on server)

Now every push to main branch will auto-deploy!

## Quick Commands

```bash
# View logs
docker logs movie-api

# Restart
docker compose restart

# Rebuild
docker compose up -d --build

# Check movie count
docker exec movie-api python manage.py shell -c "from movies.models import Movie; print(f'Total movies: {Movie.objects.count()}')"
```

For detailed instructions, see [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)
