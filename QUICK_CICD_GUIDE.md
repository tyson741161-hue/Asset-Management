# Quick CI/CD Guide

## TL;DR - What You Need

### On Cloud PC (Development)
- ✅ Git
- ✅ Python
- ✅ VS Code
- ❌ **NO Docker needed!**

### On Server (Production)
- ✅ Docker
- ✅ Docker Compose
- ✅ SSH access

---

## 5-Minute Setup

### 1. On Cloud PC - Push to GitHub

```powershell
# Run setup script
.\setup_git.ps1

# Create repo on GitHub: https://github.com/new

# Add remote and push
git remote add origin https://github.com/YOUR_USERNAME/asset-management.git
git push -u origin main
```

### 2. On Server - Install Docker

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add user to docker group
sudo usermod -aG docker $USER
```

### 3. On Server - Generate SSH Key

```bash
# Generate key
ssh-keygen -t rsa -b 4096 -f ~/.ssh/github_actions

# Show private key (copy this)
cat ~/.ssh/github_actions

# Add public key to authorized_keys
cat ~/.ssh/github_actions.pub >> ~/.ssh/authorized_keys
```

### 4. On GitHub - Add Secrets

Go to: **Settings → Secrets → Actions → New secret**

Add:
- `SERVER_HOST` = Your server IP
- `SERVER_USERNAME` = Your SSH username
- `SERVER_SSH_KEY` = Private key from step 3
- `SERVER_PORT` = 22

### 5. Test Deployment

```powershell
# On Cloud PC
echo "# Test" >> README.md
git add .
git commit -m "Test deployment"
git push
```

Check: **GitHub → Actions** tab

---

## Daily Workflow

### On Cloud PC

```powershell
# 1. Make changes
# Edit files...

# 2. Commit and push
git add .
git commit -m "Your changes"
git push

# 3. Done! GitHub Actions deploys automatically
```

### Check Deployment

- **GitHub**: Actions tab
- **Server**: `docker logs asset-management-system`
- **Browser**: `http://your_server_ip:5000`

---

## Common Commands

### Cloud PC (Development)

```powershell
# Check status
git status

# See changes
git diff

# Commit changes
git add .
git commit -m "Description"
git push

# Pull latest
git pull

# Create branch
git checkout -b feature-name

# Switch branch
git checkout main
```

### Server (Production)

```bash
# Check containers
docker ps

# View logs
docker logs asset-management-system
docker logs asset-management-db

# Restart
docker-compose restart

# Stop
docker-compose down

# Start
docker-compose up -d

# Update manually
cd ~/asset-management
git pull
docker-compose up -d --build
```

---

## Troubleshooting

### Deployment Failed

**Check GitHub Actions:**
- Go to Actions tab
- Click failed workflow
- Read error message

**Common fixes:**

```bash
# On server - restart Docker
sudo systemctl restart docker

# Check SSH
ssh your_username@your_server_ip

# Check logs
docker logs asset-management-system
```

### Can't Push to GitHub

```powershell
# Check remote
git remote -v

# Re-add remote
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

---

## Architecture

```
┌─────────────┐
│  Cloud PC   │  ← You develop here (no Docker)
│  (Windows)  │
└──────┬──────┘
       │ git push
       ↓
┌─────────────┐
│   GitHub    │  ← Code repository
│   Actions   │  ← Automated deployment
└──────┬──────┘
       │ SSH deploy
       ↓
┌─────────────┐
│   Server    │  ← Docker runs here
│  (Linux)    │
└─────────────┘
       │
       ↓
┌─────────────┐
│   Users     │  ← Access application
└─────────────┘
```

---

## What Happens When You Push

1. **You push code** to GitHub
2. **GitHub Actions** runs tests
3. **If tests pass**, connects to server via SSH
4. **Pulls latest code** on server
5. **Rebuilds Docker** containers
6. **Restarts application**
7. **Application is live!**

All automatic! ⚡

---

## Files You Created

- `.github/workflows/deploy.yml` - Deployment automation
- `.github/workflows/test.yml` - Test automation
- `.gitignore` - Files to ignore
- `CICD_SETUP.md` - Detailed guide
- `setup_git.ps1` - Setup script

---

## Security Checklist

- ✅ Use SSH keys (not passwords)
- ✅ Keep secrets in GitHub Secrets
- ✅ Don't commit `.env` files
- ✅ Use strong passwords for database
- ✅ Enable firewall on server
- ✅ Regular backups

---

## Need Help?

1. Read `CICD_SETUP.md` for detailed guide
2. Check GitHub Actions logs
3. Check server logs: `docker logs asset-management-system`
4. SSH to server and debug

---

## Summary

✅ **Cloud PC**: Just code and push  
✅ **GitHub**: Handles deployment  
✅ **Server**: Runs the application  

**You don't need Docker on Cloud PC!** 🎉
