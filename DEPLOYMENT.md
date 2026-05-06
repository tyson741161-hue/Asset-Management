# IT Asset Management System - Deployment Guide

## Quick Deployment Steps

### For Linux/Mac Servers:

1. **Upload all files to your server**
2. **Make scripts executable:**
   ```bash
   chmod +x start.sh stop.sh
   ```

3. **Start the application:**
   ```bash
   ./start.sh
   ```

4. **Access the application:**
   - Open browser: `http://YOUR_SERVER_IP:5000`
   - Login: admin / admin

### For Windows Servers:

1. **Upload all files to your server**
2. **Open PowerShell as Administrator**
3. **Navigate to project directory:**
   ```powershell
   cd C:\path\to\assetmanagement
   ```

4. **Start the application:**
   ```powershell
   docker-compose up -d
   ```

5. **Access the application:**
   - Open browser: `http://localhost:5000`
   - Login: admin / admin

## Without Docker (Traditional Method)

If you prefer not to use Docker:

1. **Install Python 3.11+**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the server:**
   ```bash
   python server.py
   ```

4. **Access the application:**
   - Open browser: `http://localhost:5000`

## Files Included

### Docker Files:
- `Dockerfile` - Docker image configuration
- `docker-compose.yml` - Docker Compose configuration
- `.dockerignore` - Files to exclude from Docker image
- `start.sh` - Quick start script (Linux/Mac)
- `stop.sh` - Quick stop script (Linux/Mac)

### Application Files:
- `server.py` - Main Flask application
- `requirements.txt` - Python dependencies
- `templates/` - HTML templates
- `static/` - CSS, JavaScript files
- `*.json` - Data storage files

### Documentation:
- `DOCKER_SETUP.md` - Detailed Docker instructions
- `DEPLOYMENT.md` - This file
- `README.md` - Project overview
- `EMAIL_SETUP.md` - Email configuration guide
- `TICKET_SETUP.md` - Ticket system guide

## System Requirements

### Minimum:
- CPU: 1 core
- RAM: 512 MB
- Disk: 1 GB
- OS: Linux, Windows, or macOS

### Recommended:
- CPU: 2 cores
- RAM: 1 GB
- Disk: 5 GB
- OS: Linux (Ubuntu 20.04+)

## Network Configuration

### Firewall Rules:
```bash
# Ubuntu/Debian
sudo ufw allow 5000/tcp

# CentOS/RHEL
sudo firewall-cmd --permanent --add-port=5000/tcp
sudo firewall-cmd --reload
```

### Access from Network:
The application will be accessible at:
- `http://SERVER_IP:5000`

Replace `SERVER_IP` with your server's IP address.

## Production Checklist

- [ ] Change default admin password
- [ ] Update email credentials in `server.py`
- [ ] Change Flask secret key in `server.py`
- [ ] Set up SSL/TLS (HTTPS)
- [ ] Configure firewall rules
- [ ] Set up automatic backups
- [ ] Configure monitoring/logging
- [ ] Test email functionality
- [ ] Test ticket system
- [ ] Document custom configurations

## Backup Strategy

### Manual Backup:
```bash
# Backup data files
cp assets_data.json assets_data.json.backup
cp tickets_data.json tickets_data.json.backup
cp requests_data.json requests_data.json.backup
```

### Automated Backup (Linux):
Create a cron job:
```bash
crontab -e
```

Add this line (daily backup at 2 AM):
```
0 2 * * * cd /path/to/assetmanagement && cp *.json /backup/location/
```

## Monitoring

### Check Container Status:
```bash
docker ps
```

### View Logs:
```bash
docker-compose logs -f
```

### Check Resource Usage:
```bash
docker stats asset-management-system
```

## Troubleshooting

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
1. Check firewall settings
2. Verify server IP address
3. Test with: `curl http://localhost:5000`

### Data not saving:
1. Check file permissions: `ls -la *.json`
2. Verify volume mounts in docker-compose.yml
3. Check disk space: `df -h`

## Updating the Application

1. **Stop the container:**
   ```bash
   docker-compose down
   ```

2. **Backup data files:**
   ```bash
   cp *.json backup/
   ```

3. **Update application files**

4. **Rebuild and start:**
   ```bash
   docker-compose build --no-cache
   docker-compose up -d
   ```

## Support

For issues or questions:
1. Check logs: `docker-compose logs -f`
2. Review documentation files
3. Verify configuration settings
4. Check system requirements

## Security Best Practices

1. **Change default credentials immediately**
2. **Use strong passwords**
3. **Enable HTTPS in production**
4. **Keep Docker and dependencies updated**
5. **Restrict network access**
6. **Regular backups**
7. **Monitor logs for suspicious activity**
8. **Use environment variables for secrets**

## Performance Optimization

### For High Traffic:
1. Increase container resources in docker-compose.yml
2. Use a reverse proxy (Nginx)
3. Enable caching
4. Optimize database queries
5. Monitor resource usage

### Resource Limits:
Edit `docker-compose.yml`:
```yaml
services:
  asset-management:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 1G
```

## License

This project is for internal use. Ensure compliance with all software licenses.
