# CI/CD Setup Guide

This guide explains how to set up automated deployment from your Cloud PC to your server using GitHub Actions.

## Overview

**Workflow:**
1. You develop on Cloud PC (no Docker needed)
2. Push code to GitHub
3. GitHub Actions automatically deploys to your server
4. Server runs the application with Docker

## Prerequisites

### On Your Cloud PC
- ✅ Git installed
- ✅ Python installed
- ✅ Code editor (VS Code)
- ❌ Docker NOT needed

### On Your Server
- ✅ Docker installed
- ✅ Docker Compose installed
- ✅ SSH access enabled
- ✅ Git installed

## Setup Steps

### Step 1: Prepare Your Server

SSH into your server and install Docker:

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add your user to docker group
sudo usermod -aG docker $USER

# Logout and login again for group changes to take effect
```

Verify installation:
```bash
docker --version
docker-compose --version
```

### Step 2: Generate SSH Key for GitHub Actions

On your server:

```bash
# Generate SSH key (press Enter for all prompts)
ssh-keygen -t rsa -b 4096 -C "github-actions" -f ~/.ssh/github_actions

# Display the private key (you'll need this for GitHub)
cat ~/.ssh/github_actions

# Add public key to authorized_keys
cat ~/.ssh/github_actions.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

**Copy the private key output** - you'll add it to GitHub secrets.

### Step 3: Create GitHub Repository

On your Cloud PC:

```powershell
# Navigate to your project
cd C:\Users\TilakPednekar\Downloads\assetmanagement

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit with PostgreSQL migration"

# Create repository on GitHub (go to github.com and create new repo)
# Then link it:
git remote add origin https://github.com/YOUR_USERNAME/asset-management.git

# Push code
git branch -M main
git push -u origin main
```

### Step 4: Configure GitHub Secrets

Go to your GitHub repository:
1. Click **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**

Add these secrets:

| Secret Name | Value | Description |
|-------------|-------|-------------|
| `SERVER_HOST` | `your.server.ip` | Your server IP address or domain |
| `SERVER_USERNAME` | `your_username` | SSH username on server |
| `SERVER_SSH_KEY` | `(paste private key)` | The private key from Step 2 |
| `SERVER_PORT` | `22` | SSH port (usually 22) |
| `DOCKER_USERNAME` | `(optional)` | Docker Hub username |
| `DOCKER_PASSWORD` | `(optional)` | Docker Hub password |

**Example:**
- SERVER_HOST: `192.168.1.100` or `myserver.com`
- SERVER_USERNAME: `ubuntu` or `admin`
- SERVER_SSH_KEY: Paste the entire private key including `-----BEGIN RSA PRIVATE KEY-----` and `-----END RSA PRIVATE KEY-----`

### Step 5: Test the Deployment

On your Cloud PC:

```powershell
# Make a small change
echo "# Test deployment" >> README.md

# Commit and push
git add .
git commit -m "Test CI/CD deployment"
git push
```

Go to GitHub → Your Repository → **Actions** tab

You should see:
- ✅ "Run Tests" workflow running
- ✅ "Deploy to Server" workflow running

### Step 6: Verify Deployment

After GitHub Actions completes:

```bash
# SSH to your server
ssh your_username@your_server_ip

# Check if containers are running
docker ps

# Check logs
docker logs asset-management-system

# Check application
curl http://localhost:5000
```

Access from browser: `http://your_server_ip:5000`

## Workflow Explanation

### 1. Test Workflow (`.github/workflows/test.yml`)

Runs on every push and pull request:
- Sets up Python and PostgreSQL
- Installs dependencies
- Runs database initialization
- Runs tests
- Verifies setup

### 2. Deploy Workflow (`.github/workflows/deploy.yml`)

Runs on push to main/master:
- Connects to your server via SSH
- Pulls latest code from GitHub
- Stops old containers
- Builds and starts new containers
- Shows deployment status

## Development Workflow

### On Cloud PC (Daily Work)

```powershell
# 1. Make changes to code
# Edit files in VS Code

# 2. Test locally (optional)
python server.py

# 3. Commit changes
git add .
git commit -m "Description of changes"

# 4. Push to GitHub
git push

# 5. GitHub Actions automatically deploys to server!
```

### Monitor Deployment

- **GitHub**: Check Actions tab for deployment status
- **Server**: `docker logs -f asset-management-system`
- **Browser**: Visit `http://your_server_ip:5000`

## Troubleshooting

### Deployment Fails

**Check GitHub Actions logs:**
1. Go to GitHub → Actions
2. Click on failed workflow
3. Check error messages

**Common issues:**

**SSH Connection Failed**
```bash
# On server, check SSH is running
sudo systemctl status ssh

# Check firewall
sudo ufw status
sudo ufw allow 22
```

**Docker Command Failed**
```bash
# On server, check Docker is running
sudo systemctl status docker

# Check user permissions
groups $USER  # Should include 'docker'
```

**Application Not Starting**
```bash
# Check logs
docker logs asset-management-system

# Check database
docker logs asset-management-db

# Restart containers
docker-compose restart
```

### Manual Deployment

If GitHub Actions fails, deploy manually:

```bash
# SSH to server
ssh your_username@your_server_ip

# Navigate to project
cd ~/asset-management

# Pull latest code
git pull

# Restart containers
docker-compose down
docker-compose up -d --build

# Check status
docker-compose ps
docker logs asset-management-system
```

## Advanced Configuration

### Environment Variables

Create `.env` file on server:

```bash
# On server
cd ~/asset-management
nano .env
```

Add:
```env
DATABASE_URL=postgresql://asset_admin:your_secure_password@postgres:5432/asset_management
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
```

Update `docker-compose.yml` to use `.env`:
```yaml
env_file:
  - .env
```

### Multiple Environments

Create separate workflows for staging and production:

**`.github/workflows/deploy-staging.yml`**
```yaml
on:
  push:
    branches:
      - develop
```

**`.github/workflows/deploy-production.yml`**
```yaml
on:
  push:
    branches:
      - main
```

Use different secrets for each environment:
- `STAGING_SERVER_HOST`
- `PRODUCTION_SERVER_HOST`

### Rollback

If deployment breaks:

```bash
# On server
cd ~/asset-management

# Check git history
git log --oneline

# Rollback to previous version
git checkout <previous-commit-hash>

# Restart containers
docker-compose down
docker-compose up -d --build
```

Or use GitHub:
1. Go to Actions → Select successful deployment
2. Click "Re-run jobs"

## Security Best Practices

1. **Use SSH Keys** (not passwords)
2. **Restrict SSH access** to specific IPs
3. **Use secrets** for sensitive data
4. **Enable firewall** on server
5. **Regular backups** of database
6. **Update dependencies** regularly
7. **Monitor logs** for suspicious activity

## Backup Strategy

Add backup workflow (`.github/workflows/backup.yml`):

```yaml
name: Backup Database

on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM
  workflow_dispatch:

jobs:
  backup:
    runs-on: ubuntu-latest
    steps:
      - name: Backup Database
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USERNAME }}
          key: ${{ secrets.SERVER_SSH_KEY }}
          script: |
            cd ~/asset-management
            docker exec asset-management-db pg_dump -U asset_admin asset_management > backup_$(date +%Y%m%d).sql
            python export_db_to_json.py
```

## Monitoring

### Check Application Health

```bash
# On server
curl http://localhost:5000

# Check container health
docker ps
docker stats

# Check disk space
df -h

# Check memory
free -h
```

### Set Up Alerts

Use services like:
- **UptimeRobot** - Monitor uptime
- **Sentry** - Error tracking
- **Datadog** - Performance monitoring

## Summary

✅ **Cloud PC**: Develop and push code (no Docker needed)  
✅ **GitHub**: Automatically test and deploy  
✅ **Server**: Run application with Docker  

**Workflow:**
```
Cloud PC → Git Push → GitHub Actions → Server Deployment → Live Application
```

This setup gives you:
- 🚀 Automated deployments
- ✅ Automated testing
- 🔄 Easy rollbacks
- 📊 Deployment history
- 🔒 Secure SSH deployment

## Next Steps

1. ✅ Set up GitHub repository
2. ✅ Configure GitHub secrets
3. ✅ Push code and test deployment
4. ✅ Monitor first deployment
5. ✅ Set up backups
6. ✅ Configure monitoring

You're now ready for professional CI/CD! 🎉
