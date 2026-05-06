# IT Asset Management System

A comprehensive web-based application for managing IT assets, support tickets, and user requests with PostgreSQL database backend.

## Features

### Asset Management
- Login authentication (username: admin, password: admin)
- Add, edit, view, and delete assets
- Support for multiple asset types:
  - **Devices**: Laptop, Desktop, Android Device, iOS Device, Mac Mini, Mac Device, Tablet, Server
  - **Network**: Firewall, Switch, Router, Access Point
  - **Accessories**: RAM, Mouse, Headphone, Hard Disk, WiFi Adapter, Keyboard, Charger
- Track laptop accessories (mouse, headphone, charger, monitor)
- Filter by category, status, and office location
- Security code protection for edit/delete operations (code: 4181)
- Track current and previous users

### Ticket System
- Automatic ticket creation from incoming emails
- Ticket numbering system (starting from #1001)
- Status management (Open, In Progress, Resolved, Closed)
- Reply to tickets with email integration
- Internal notes for tickets
- Auto-refresh every 30 seconds
- Search by ticket number, subject, or email
- Automatic closure email notification

### Request Management
- Submit requests via web interface
- Email notifications to specified recipients
- Request history tracking

## Technology Stack

- **Backend**: Python Flask
- **Database**: PostgreSQL 15
- **Email**: Flask-Mail with Gmail SMTP/IMAP
- **Containerization**: Docker & Docker Compose
- **ORM**: SQLAlchemy

## Quick Start with Docker (Recommended)

### Prerequisites
- Docker and Docker Compose installed

### Installation

1. Clone or download this repository

2. Start the application:
```bash
# Linux/Mac
./start.sh

# Windows
start.sh
```

Or manually:
```bash
docker-compose up -d
```

3. Access the application:
   - Local: http://localhost:5000
   - Network: http://YOUR_IP_ADDRESS:5000

4. Stop the application:
```bash
# Linux/Mac
./stop.sh

# Windows
stop.sh
```

Or manually:
```bash
docker-compose down
```

## Manual Installation (Development)

### Prerequisites
- Python 3.11 or higher
- PostgreSQL 15 or higher

### Setup

1. Install PostgreSQL and create database:
```sql
CREATE DATABASE asset_management;
CREATE USER asset_admin WITH PASSWORD 'asset_secure_pass_2026';
GRANT ALL PRIVILEGES ON DATABASE asset_management TO asset_admin;
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Set environment variable:
```bash
# Linux/Mac
export DATABASE_URL="postgresql://asset_admin:asset_secure_pass_2026@localhost:5432/asset_management"

# Windows PowerShell
$env:DATABASE_URL="postgresql://asset_admin:asset_secure_pass_2026@localhost:5432/asset_management"
```

4. Initialize database:
```bash
python init_db.py
```

5. (Optional) Migrate existing JSON data:
```bash
python migrate_json_to_postgres.py
```

6. Start the server:
```bash
python server.py
```

## Default Credentials

- **Login Username:** admin
- **Login Password:** admin
- **Edit/Delete Code:** 4181

## Email Configuration

The system uses Gmail for sending and receiving emails:
- **Email**: tyson741161@gmail.com
- **App Password**: sdxr csld bahs fpeg

To use your own email, update the configuration in `server.py`.

See [EMAIL_SETUP.md](EMAIL_SETUP.md) for detailed email configuration instructions.

## Database Management

### Backup Database

```bash
# Export to JSON
python export_db_to_json.py

# PostgreSQL dump
docker exec asset-management-db pg_dump -U asset_admin asset_management > backup.sql
```

### Restore Database

```bash
docker exec -i asset-management-db psql -U asset_admin asset_management < backup.sql
```

### Access Database

```bash
docker exec -it asset-management-db psql -U asset_admin -d asset_management
```

## Network Access

Once the server is running, anyone on your internal network can access it by:
1. Opening their web browser
2. Going to: http://YOUR_SERVER_IP:5000

### Finding Your IP Address

**Windows:**
```bash
ipconfig
```
Look for "IPv4 Address" (e.g., 192.168.1.100)

**Linux/Mac:**
```bash
ifconfig
# or
ip addr show
```

## Documentation

- [Docker Setup Guide](DOCKER_SETUP.md) - Detailed Docker installation and configuration
- [Deployment Guide](DEPLOYMENT.md) - Production deployment instructions
- [PostgreSQL Migration](POSTGRES_MIGRATION.md) - Database migration and management
- [Email Setup](EMAIL_SETUP.md) - Email configuration guide
- [Ticket System](TICKET_SETUP.md) - Ticket system configuration

## Project Structure

```
.
├── server.py                    # Main Flask application
├── models.py                    # Database models (SQLAlchemy)
├── init_db.py                   # Database initialization script
├── migrate_json_to_postgres.py  # JSON to PostgreSQL migration script
├── export_db_to_json.py         # Database to JSON export script
├── requirements.txt             # Python dependencies
├── docker-compose.yml           # Docker Compose configuration
├── Dockerfile                   # Docker image definition
├── docker-entrypoint.sh         # Container startup script
├── templates/
│   └── index.html              # Main web interface
├── static/
│   ├── app.js                  # Asset management JavaScript
│   ├── tickets.js              # Ticket system JavaScript
│   ├── request.js              # Request management JavaScript
│   └── style.css               # Application styles
└── *.json                      # Data files (backup/migration)
```

## Troubleshooting

### Database Connection Issues

```bash
# Check PostgreSQL is running
docker ps

# Check database logs
docker logs asset-management-db

# Test connection
docker exec asset-management-db pg_isready -U asset_admin -d asset_management
```

### Application Issues

```bash
# Check application logs
docker logs asset-management-system

# Restart application
docker-compose restart asset-management
```

### Reset Everything

```bash
# Stop and remove containers and volumes
docker-compose down -v

# Start fresh
docker-compose up -d
```

## Security Notes

### For Production Use:

1. **Change Default Passwords**:
   - Update PostgreSQL password in `docker-compose.yml`
   - Change `app.secret_key` in `server.py`
   - Update login credentials

2. **Environment Variables**:
   - Use `.env` file for sensitive data
   - Never commit credentials to version control

3. **Network Security**:
   - Don't expose PostgreSQL port (5432) publicly
   - Use firewall rules to restrict access
   - Consider using HTTPS/SSL

4. **Database Security**:
   - Enable SSL for PostgreSQL connections
   - Regular backups
   - Implement proper user permissions

5. **Application Security**:
   - Set `debug=False` in production
   - Implement rate limiting
   - Add CSRF protection
   - Use secure session cookies

## Performance Optimization

- Database indexes on frequently queried fields
- Connection pooling for database
- Lazy loading for relationships
- Efficient query patterns

## Contributing

When contributing:
1. Test changes locally
2. Update documentation
3. Follow existing code style
4. Test with both Docker and manual setup

## License

This project is for internal use. Modify as needed for your organization.

## Support

For issues or questions:
1. Check documentation in the repository
2. Review application logs
3. Check database logs
4. Refer to troubleshooting section
