# Docker Setup Guide for IT Asset Management System

This guide will help you run the IT Asset Management System using Docker.

## Prerequisites

- Docker installed on your server ([Install Docker](https://docs.docker.com/get-docker/))
- Docker Compose installed ([Install Docker Compose](https://docs.docker.com/compose/install/))

## Quick Start

### Option 1: Using Docker Compose (Recommended)

1. **Navigate to the project directory:**
   ```bash
   cd /path/to/assetmanagement
   ```

2. **Build and start the container:**
   ```bash
   docker-compose up -d
   ```

3. **Access the application:**
   - Open your browser and go to: `http://localhost:5000`
   - From other computers on your network: `http://YOUR_SERVER_IP:5000`

4. **View logs:**
   ```bash
   docker-compose logs -f
   ```

5. **Stop the container:**
   ```bash
   docker-compose down
   ```

### Option 2: Using Docker Commands

1. **Build the Docker image:**
   ```bash
   docker build -t asset-management .
   ```

2. **Run the container:**
   ```bash
   docker run -d \
     --name asset-management-system \
     -p 5000:5000 \
     -v $(pwd)/assets_data.json:/app/assets_data.json \
     -v $(pwd)/tickets_data.json:/app/tickets_data.json \
     -v $(pwd)/requests_data.json:/app/requests_data.json \
     asset-management
   ```

3. **Access the application:**
   - Open your browser and go to: `http://localhost:5000`

4. **View logs:**
   ```bash
   docker logs -f asset-management-system
   ```

5. **Stop the container:**
   ```bash
   docker stop asset-management-system
   docker rm asset-management-system
   ```

## Configuration

### Email Configuration

The email settings are configured in `server.py`. To change them:

1. Edit `server.py` before building the Docker image
2. Update the following settings:
   ```python
   app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
   app.config['MAIL_PASSWORD'] = 'your-app-password'
   IMAP_USERNAME = 'your-email@gmail.com'
   IMAP_PASSWORD = 'your-app-password'
   ```

3. Rebuild the Docker image:
   ```bash
   docker-compose down
   docker-compose build --no-cache
   docker-compose up -d
   ```

### Port Configuration

To change the port from 5000 to another port (e.g., 8080):

1. Edit `docker-compose.yml`:
   ```yaml
   ports:
     - "8080:5000"  # Change 8080 to your desired port
   ```

2. Restart the container:
   ```bash
   docker-compose down
   docker-compose up -d
   ```

## Data Persistence

The following files are mounted as volumes to persist data:
- `assets_data.json` - Asset information
- `tickets_data.json` - Support tickets
- `requests_data.json` - User requests

These files are stored on your host machine and will persist even if the container is removed.

## Useful Commands

### Check if container is running:
```bash
docker ps
```

### View container logs:
```bash
docker-compose logs -f
```

### Restart the container:
```bash
docker-compose restart
```

### Update the application:
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Access container shell:
```bash
docker exec -it asset-management-system /bin/bash
```

### Remove everything (including volumes):
```bash
docker-compose down -v
```

## Troubleshooting

### Container won't start:
1. Check logs: `docker-compose logs`
2. Verify port 5000 is not in use: `netstat -tuln | grep 5000`
3. Check Docker is running: `docker ps`

### Can't access from other computers:
1. Check firewall settings on the server
2. Verify the server IP address
3. Ensure port 5000 is open: `sudo ufw allow 5000` (Ubuntu/Debian)

### Email not working:
1. Verify Gmail App Password is correct
2. Check IMAP is enabled in Gmail settings
3. View logs for error messages: `docker-compose logs -f`

### Data not persisting:
1. Ensure JSON files exist in the project directory
2. Check volume mounts in `docker-compose.yml`
3. Verify file permissions: `ls -la *.json`

## Production Deployment

For production deployment, consider:

1. **Use environment variables for sensitive data:**
   - Create a `.env` file for email credentials
   - Never commit credentials to Git

2. **Use a reverse proxy (Nginx):**
   - Set up SSL/TLS certificates
   - Configure domain name

3. **Set up automatic backups:**
   - Backup JSON data files regularly
   - Use cron jobs or backup scripts

4. **Monitor the application:**
   - Set up logging
   - Monitor container health
   - Set up alerts for failures

## Security Notes

- Change the default secret key in `server.py`
- Use strong passwords for email accounts
- Keep Docker and dependencies updated
- Use HTTPS in production
- Restrict network access with firewall rules

## Support

For issues or questions:
- Check the logs: `docker-compose logs -f`
- Verify all configuration files are correct
- Ensure all dependencies are installed

## Login Credentials

- **Username:** admin
- **Password:** admin

**Important:** Change these credentials in production!
