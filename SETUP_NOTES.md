# Setup Notes for movieapi.betmig.link

## Domain Configuration
Domain: `movieapi.betmig.link`

Make sure DNS A record points to your server IP before setting up SSL in Nginx Proxy Manager.

## Quick Setup Commands

### On Server (one-time setup)
```bash
ssh -p 2222 betmig@YOUR_SERVER_IP

mkdir -p /docker/movie-api
cd /docker/movie-api

# Clone repo
git clone YOUR_REPO_URL .

# Copy database from local
# (Run from local machine)
# scp -P 2222 db.sqlite3 betmig@YOUR_SERVER_IP:/docker/movie-api/

# Build and start
docker compose up -d --build

# Check status
docker logs movie-api
```

### Nginx Proxy Manager Setup
1. Go to http://YOUR_SERVER_IP:81
2. Add Proxy Host:
   - Domain: `movieapi.betmig.link`
   - Forward to: `movie-api:8000`
   - SSL: Let's Encrypt (force SSL, HTTP/2)

### Test Endpoints
```bash
# List movies
curl https://movieapi.betmig.link/api/movies/

# Get single movie
curl https://movieapi.betmig.link/api/movies/1/

# Top-rated
curl https://movieapi.betmig.link/api/movies/top-rated/

# API docs
open https://movieapi.betmig.link/api/docs/
```

### GitHub Actions Secrets
Add to repo Settings → Secrets and variables → Actions:
- `SERVER_HOST`: Your server IP
- `SERVER_USERNAME`: betmig
- `SSH_PRIVATE_KEY`: Content of ~/.ssh/movie_api_deploy

### Quick Deploy from Local
```bash
./deploy.sh
```

## Maintenance Commands

```bash
# View logs
ssh -p 2222 betmig@YOUR_SERVER_IP 'docker logs movie-api'

# Restart
ssh -p 2222 betmig@YOUR_SERVER_IP 'cd /docker/movie-api && docker compose restart'

# Rebuild
ssh -p 2222 betmig@YOUR_SERVER_IP 'cd /docker/movie-api && docker compose up -d --build'

# Check movie count
ssh -p 2222 betmig@YOUR_SERVER_IP "docker exec movie-api python manage.py shell -c 'from movies.models import Movie; print(Movie.objects.count())'"
```

## After Deployment

Your API will be live at:
- **Homepage**: https://movieapi.betmig.link/
- **API Base**: https://movieapi.betmig.link/api/movies/
- **Swagger Docs**: https://movieapi.betmig.link/api/docs/
- **Admin Panel**: https://movieapi.betmig.link/admin/
