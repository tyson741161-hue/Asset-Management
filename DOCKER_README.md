# 🐳 Docker Deployment - IT Asset Management System

## 🚀 Quick Start (3 Steps)

### Step 1: Install Docker
```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Or download from: https://docs.docker.com/get-docker/
```

### Step 2: Start the Application
```bash
# Linux/Mac
chmod +x start.sh
./start.sh

# Windows (PowerShell)
docker-compose up -d
```

### Step 3: Access the Application
- Open browser: `http://localhost:5000`
- Login: **admin** / **admin**

## 📦 What's Included

### Docker Files Created:
✅ `Dockerfile` - Container configuration  
✅ `docker-compose.yml` - Service orchestration  
✅ `.dockerignore` - Optimized builds  
✅ `start.sh` - One-command startup (Linux/Mac)  
✅ `stop.sh` - One-command shutdown (Linux/Mac)  

### Documentation:
✅ `DOCKER_SETUP.md` - Detailed Docker guide  
✅ `DEPLOYMENT.md` - Production deployment guide  
✅ `DOCKER_README.md` - This quick reference  

## 🎯 Common Commands

### Start Application:
```bash
docker-compose up -d
```

### Stop Application:
```bash
docker-compose down
```

### View Logs:
```bash
docker-compose logs -f
```

### Restart Application:
```bash
docker-compose restart
```

### Update Application:
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## 🌐 Network Access

### Local Access:
```
http://localhost:5000
```

### Network Access:
```
http://YOUR_SERVER_IP:5000
```

### Find Your Server IP:
```bash
# Linux/Mac
hostname -I

# Windows
ipconfig
```

## 📊 Data Persistence

Your data is automatically saved in these files:
- `assets_data.json` - All assets
- `tickets_data.json` - All tickets
- `requests_data.json` - All requests

These files persist even if you stop/restart the container.

## 🔧 Configuration

### Change Port (from 5000 to 8080):
Edit `docker-compose.yml`:
```yaml
ports:
  - "8080:5000"
```

### Email Settings:
Edit `server.py` before building:
```python
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-app-password'
```

Then rebuild:
```bash
docker-compose build --no-cache
docker-compose up -d
```

## 🛡️ Security Checklist

- [ ] Change admin password (default: admin/admin)
- [ ] Update email credentials
- [ ] Change Flask secret key
- [ ] Enable firewall rules
- [ ] Set up HTTPS (production)
- [ ] Regular backups

## 🔥 Firewall Configuration

### Ubuntu/Debian:
```bash
sudo ufw allow 5000/tcp
sudo ufw enable
```

### CentOS/RHEL:
```bash
sudo firewall-cmd --permanent --add-port=5000/tcp
sudo firewall-cmd --reload
```

### Windows:
```powershell
New-NetFirewallRule -DisplayName "Asset Management" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow
```

## 💾 Backup Your Data

### Quick Backup:
```bash
cp assets_data.json assets_data.json.backup
cp tickets_data.json tickets_data.json.backup
cp requests_data.json requests_data.json.backup
```

### Automated Daily Backup (Linux):
```bash
# Add to crontab
0 2 * * * cd /path/to/assetmanagement && tar -czf backup-$(date +\%Y\%m\%d).tar.gz *.json
```

## 🐛 Troubleshooting

### Container won't start:
```bash
# Check logs
docker-compose logs

# Check if port is in use
netstat -tuln | grep 5000

# Restart Docker
sudo systemctl restart docker
```

### Can't access from network:
1. Check firewall: `sudo ufw status`
2. Verify IP: `hostname -I`
3. Test locally: `curl http://localhost:5000`

### Email not working:
1. Check Gmail App Password
2. Enable IMAP in Gmail
3. View logs: `docker-compose logs -f`

## 📈 System Requirements

### Minimum:
- Docker 20.10+
- 512 MB RAM
- 1 GB Disk Space

### Recommended:
- Docker 24.0+
- 1 GB RAM
- 5 GB Disk Space

## 🎓 Learn More

- **Detailed Docker Guide**: See `DOCKER_SETUP.md`
- **Production Deployment**: See `DEPLOYMENT.md`
- **Email Setup**: See `EMAIL_SETUP.md`
- **Ticket System**: See `TICKET_SETUP.md`

## ✨ Features

✅ Asset Management (Laptops, Network Equipment, Accessories)  
✅ Support Ticket System (Email Integration)  
✅ Request Management  
✅ Auto-refresh Tickets (Every 30 seconds)  
✅ Email Notifications  
✅ Status Tracking  
✅ Search & Filters  
✅ Responsive Design  

## 🆘 Need Help?

1. Check logs: `docker-compose logs -f`
2. Review documentation files
3. Verify Docker is running: `docker ps`
4. Check system resources: `docker stats`

## 📝 Default Credentials

**Username:** admin  
**Password:** admin  

⚠️ **IMPORTANT:** Change these in production!

## 🎉 Success!

If you see this, you're ready to deploy:
```
✓ Docker files created
✓ Documentation ready
✓ Scripts configured
✓ Ready to deploy!
```

Run `./start.sh` (Linux/Mac) or `docker-compose up -d` (Windows) to begin!
