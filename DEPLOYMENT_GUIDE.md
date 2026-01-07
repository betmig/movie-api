# Movie API Deployment Guide

## Prerequisites
- VPS with Docker and Nginx Proxy Manager already set up
- SSH access configured (port 2222)
- GitHub repository for the project

## Step 1: Set Up SSH Key for GitHub on Server

```bash
# SSH into your server
ssh -p 2222 betmig@YOUR_SERVER_IP

# Generate SSH key for this project
ssh-keygen -t ed25519 -C "movie-api-deploy" -f ~/.ssh/movie_api_deploy

# Display public key
cat ~/.ssh/movie_api_deploy.pub
```

Copy the public key and add it to your GitHub repository:
- Go to GitHub repo → Settings → Deploy keys
- Click "Add deploy key"
- Paste the public key
- Give it a title like "VPS Deploy Key"
- Check "Allow write access" if needed
- Click "Add key"

## Step 2: Create Project Directory on Server

```bash
# Create directory structure
mkdir -p /docker/movie-api
cd /docker/movie-api

# Configure git to use the correct SSH key
cat > ~/.ssh/config << 'EOL'
Host github.com-movie-api
    HostName github.com
    User git
    IdentityFile ~/.ssh/movie_api_deploy
    IdentitiesOnly yes
EOL

# Clone your repository (replace with your actual repo)
git clone git@github.com-movie-api:YOUR_USERNAME/YOUR_REPO.git .

# Alternative: if using HTTPS
# git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git .
```

## Step 3: Copy Database (if deploying existing data)

If you have your populated database locally:

```bash
# On your LOCAL machine, copy the database to server
scp -P 2222 db.sqlite3 betmig@YOUR_SERVER_IP:/docker/movie-api/
```

## Step 4: Build and Start Container

```bash
# On the server, in /docker/movie-api
docker compose up -d --build

# Check if container is running
docker ps

# Check logs
docker logs movie-api
```

## Step 5: Configure Nginx Proxy Manager

1. Go to http://YOUR_SERVER_IP:81
2. Login with your credentials
3. Click "Proxy Hosts" → "Add Proxy Host"

**Details Tab:**
- Domain Names: `movieapi.betmig.link`
- Scheme: `http`
- Forward Hostname / IP: `movie-api`
- Forward Port: `8000`
- Cache Assets: ✓ (optional)
- Block Common Exploits: ✓
- Websockets Support: ✗

**SSL Tab:**
- SSL Certificate: "Request a new SSL Certificate"
- Force SSL: ✓
- HTTP/2 Support: ✓
- Email Address: your-email@example.com
- I Agree to the Let's Encrypt Terms of Service: ✓

**Advanced Tab (optional):**
```nginx
client_max_body_size 50M;
proxy_read_timeout 300;
proxy_connect_timeout 300;
proxy_send_timeout 300;
```

4. Click "Save"

## Step 6: Set Up GitHub Actions Auto-Deployment

Add these secrets to your GitHub repository:
- Go to GitHub repo → Settings → Secrets and variables → Actions
- Add these secrets:

```
SERVER_HOST: YOUR_SERVER_IP
SERVER_USERNAME: betmig
SSH_PRIVATE_KEY: (content of ~/.ssh/movie_api_deploy private key)
```

To get the private key content:
```bash
# On server
cat ~/.ssh/movie_api_deploy
```

## Step 7: Test the Deployment

```bash
# Test the API
curl https://movieapi.betmig.link/api/movies/

# Test specific endpoint
curl https://movieapi.betmig.link/api/movies/1/

# Test top-rated movies
curl https://movieapi.betmig.link/api/movies/top-rated/?min_rating=8.0
```

## Useful Commands

### View Logs
```bash
docker logs movie-api
docker logs -f movie-api  # Follow logs
```

### Restart Container
```bash
docker compose restart
```

### Rebuild Container
```bash
docker compose down
docker compose up -d --build
```

### Access Container Shell
```bash
docker exec -it movie-api bash
```

### Run Django Commands
```bash
# Create superuser
docker exec -it movie-api python manage.py createsuperuser

# Run migrations
docker exec -it movie-api python manage.py migrate

# Import data
docker exec -it movie-api python manage.py import_imdb
```

### Check Database
```bash
docker exec -it movie-api python manage.py shell
# Then in shell:
# from movies.models import Movie
# Movie.objects.count()
```

## Troubleshooting

### Container won't start
```bash
docker logs movie-api
```

### Database issues
```bash
# Check if database file exists and has correct permissions
docker exec -it movie-api ls -la db.sqlite3
```

### Port conflicts
```bash
# Check what's using port 8000
sudo lsof -i :8000
```

### Update domain/SSL issues
- Check Nginx Proxy Manager logs
- Verify DNS is pointing to your server
- Wait 5-10 minutes for SSL certificate generation

## API Endpoints

Once deployed, your API will be available at:

- **Base URL**: `https://movieapi.betmig.link/api/`
- **API Docs**: `https://movieapi.betmig.link/api/docs/`
- **OpenAPI Schema**: `https://movieapi.betmig.link/api/schema/`

### Main Endpoints:
- `GET /api/movies/` - List all movies (paginated)
- `GET /api/movies/{id}/` - Get specific movie
- `POST /api/movies/` - Create new movie
- `PUT /api/movies/{id}/` - Update movie
- `PATCH /api/movies/{id}/` - Partial update
- `DELETE /api/movies/{id}/` - Delete movie
- `GET /api/movies/top-rated/` - Get top-rated movies with filters

## Updating Your Application

After pushing changes to GitHub main branch, the GitHub Action will automatically:
1. Pull latest code on server
2. Rebuild the Docker container
3. Restart the service

You can also manually update:
```bash
cd /docker/movie-api
git pull
docker compose up -d --build
```
