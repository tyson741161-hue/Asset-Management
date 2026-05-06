# Quick Start Guide

## For First-Time Users

### Using Docker (Easiest)

1. **Install Docker Desktop**
   - Windows/Mac: Download from https://www.docker.com/products/docker-desktop
   - Linux: Follow instructions at https://docs.docker.com/engine/install/

2. **Start the Application**
   ```bash
   docker-compose up -d
   ```

3. **Access the Application**
   - Open browser: http://localhost:5000
   - Login: admin / admin

4. **Stop the Application**
   ```bash
   docker-compose down
   ```

### Without Docker

1. **Install PostgreSQL**
   - Download from https://www.postgresql.org/download/

2. **Create Database**
   ```sql
   CREATE DATABASE asset_management;
   CREATE USER asset_admin WITH PASSWORD 'asset_secure_pass_2026';
   GRANT ALL PRIVILEGES ON DATABASE asset_management TO asset_admin;
   ```

3. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize Database**
   ```bash
   python init_db.py
   ```

5. **Start Server**
   ```bash
   python server.py
   ```

6. **Access Application**
   - Open browser: http://localhost:5000
   - Login: admin / admin

## Common Tasks

### Add an Asset

1. Login to the application
2. Click "Assets" tab
3. Click "+ Add Asset" button
4. Fill in the form
5. Click "Add Asset"

### Create a Ticket

Tickets are created automatically from emails sent to: tyson741161@gmail.com

Or manually:
1. Click "Tickets" tab
2. Click "Refresh" to fetch new emails
3. New tickets appear automatically

### Reply to a Ticket

1. Click "Tickets" tab
2. Click on a ticket to view details
3. Click "Reply" button
4. Type your message
5. Click "Send Reply"

### Submit a Request

1. Click "Request" tab
2. Click "Submit a Request" button
3. Fill in:
   - Recipient email
   - Subject
   - Description
4. Click "Submit Request"

### Backup Data

```bash
# Export to JSON
python export_db_to_json.py

# PostgreSQL backup
docker exec asset-management-db pg_dump -U asset_admin asset_management > backup.sql
```

### View Logs

```bash
# Application logs
docker logs asset-management-system

# Database logs
docker logs asset-management-db

# Follow logs in real-time
docker logs -f asset-management-system
```

### Restart Application

```bash
# Restart everything
docker-compose restart

# Restart only application
docker-compose restart asset-management

# Restart only database
docker-compose restart postgres
```

### Update Application

```bash
# Stop containers
docker-compose down

# Pull latest changes (if using git)
git pull

# Rebuild and start
docker-compose up -d --build
```

## Troubleshooting

### Can't Access Application

**Check if containers are running:**
```bash
docker ps
```

You should see:
- asset-management-system
- asset-management-db

**If not running:**
```bash
docker-compose up -d
```

### Database Connection Error

**Check database health:**
```bash
docker exec asset-management-db pg_isready -U asset_admin -d asset_management
```

**Restart database:**
```bash
docker-compose restart postgres
```

### Email Not Working

1. Check email configuration in `server.py`
2. Verify Gmail App Password is correct
3. Check IMAP/SMTP settings
4. See [EMAIL_SETUP.md](EMAIL_SETUP.md) for details

### Tickets Not Appearing

1. Click "Refresh" button in Tickets tab
2. Check email account has unread emails
3. Check application logs:
   ```bash
   docker logs asset-management-system
   ```

### Data Not Saving

1. Check database is running:
   ```bash
   docker ps | grep postgres
   ```

2. Check database connection:
   ```bash
   docker logs asset-management-system | grep -i error
   ```

3. Restart application:
   ```bash
   docker-compose restart asset-management
   ```

## Default Credentials

| Item | Value |
|------|-------|
| Web Login Username | admin |
| Web Login Password | admin |
| Edit/Delete Code | 4181 |
| Database Name | asset_management |
| Database User | asset_admin |
| Database Password | asset_secure_pass_2026 |
| Email Account | tyson741161@gmail.com |
| Email App Password | sdxr csld bahs fpeg |

## Ports Used

| Service | Port |
|---------|------|
| Web Application | 5000 |
| PostgreSQL | 5432 |

## File Locations

### In Docker Container

| File | Location |
|------|----------|
| Application | /app/ |
| Database Data | /var/lib/postgresql/data |
| JSON Backups | /app/*.json |

### On Host Machine

| File | Location |
|------|----------|
| Application | ./ (current directory) |
| Database Data | Docker volume: postgres_data |
| JSON Backups | ./*.json |

## Useful Commands

### Docker Commands

```bash
# View all containers
docker ps -a

# View logs
docker logs <container-name>

# Execute command in container
docker exec -it <container-name> <command>

# Remove all stopped containers
docker container prune

# Remove unused volumes
docker volume prune

# View disk usage
docker system df
```

### Database Commands

```bash
# Connect to database
docker exec -it asset-management-db psql -U asset_admin -d asset_management

# Count assets
docker exec asset-management-db psql -U asset_admin -d asset_management -c "SELECT COUNT(*) FROM assets;"

# Count tickets
docker exec asset-management-db psql -U asset_admin -d asset_management -c "SELECT COUNT(*) FROM tickets;"

# View recent tickets
docker exec asset-management-db psql -U asset_admin -d asset_management -c "SELECT ticket_number, subject, status FROM tickets ORDER BY date DESC LIMIT 5;"
```

## Getting Help

1. **Check Documentation**
   - README.md - Main documentation
   - POSTGRES_MIGRATION.md - Database details
   - DOCKER_SETUP.md - Docker configuration
   - EMAIL_SETUP.md - Email configuration

2. **Check Logs**
   ```bash
   docker logs asset-management-system
   docker logs asset-management-db
   ```

3. **Check Container Status**
   ```bash
   docker ps
   docker-compose ps
   ```

4. **Restart Everything**
   ```bash
   docker-compose down
   docker-compose up -d
   ```

## Next Steps

- Read [README.md](README.md) for complete documentation
- Configure email settings (see [EMAIL_SETUP.md](EMAIL_SETUP.md))
- Set up backups (see [POSTGRES_MIGRATION.md](POSTGRES_MIGRATION.md))
- Review security settings for production use
- Customize for your organization's needs
