# PostgreSQL Migration Guide

This document explains the migration from JSON file storage to PostgreSQL database for the IT Asset Management System.

## Overview

The system has been migrated from JSON file-based storage to PostgreSQL database for:
- Better data integrity and consistency
- Improved performance with large datasets
- ACID compliance for transactions
- Better concurrent access handling
- Relational data management

## Database Schema

### Tables

1. **assets** - Stores all IT assets (laptops, network equipment, accessories)
2. **tickets** - Stores support tickets from emails
3. **ticket_replies** - Stores replies to tickets
4. **ticket_notes** - Stores internal notes for tickets
5. **requests** - Stores user requests

### Relationships

- `tickets` → `ticket_replies` (one-to-many)
- `tickets` → `ticket_notes` (one-to-many)

## Migration Process

### Automatic Migration (Docker)

When using Docker Compose, the migration happens automatically:

1. PostgreSQL container starts first
2. Application container waits for PostgreSQL to be ready
3. Database tables are created automatically
4. If JSON files exist and database is empty, data is migrated automatically

### Manual Migration (Development)

#### Step 1: Start PostgreSQL

```bash
# Using Docker
docker run -d \
  --name asset-postgres \
  -e POSTGRES_DB=asset_management \
  -e POSTGRES_USER=asset_admin \
  -e POSTGRES_PASSWORD=asset_secure_pass_2026 \
  -p 5432:5432 \
  postgres:15-alpine
```

Or install PostgreSQL locally and create the database.

#### Step 2: Set Environment Variable

```bash
# Linux/Mac
export DATABASE_URL="postgresql://asset_admin:asset_secure_pass_2026@localhost:5432/asset_management"

# Windows PowerShell
$env:DATABASE_URL="postgresql://asset_admin:asset_secure_pass_2026@localhost:5432/asset_management"
```

#### Step 3: Initialize Database

```bash
python init_db.py
```

This creates all necessary tables.

#### Step 4: Migrate Data from JSON

```bash
python migrate_json_to_postgres.py
```

This reads data from:
- `assets_data.json`
- `tickets_data.json`
- `requests_data.json`

And migrates it to PostgreSQL.

#### Step 5: Start Application

```bash
python server.py
```

## Database Configuration

### Default Configuration

- **Host**: postgres (in Docker) or localhost (local)
- **Port**: 5432
- **Database**: asset_management
- **User**: asset_admin
- **Password**: asset_secure_pass_2026

### Custom Configuration

Set the `DATABASE_URL` environment variable:

```bash
DATABASE_URL="postgresql://username:password@host:port/database"
```

## Backup and Export

### Export Database to JSON

To create JSON backups of your PostgreSQL data:

```bash
python export_db_to_json.py
```

This creates:
- `assets_data_backup.json`
- `tickets_data_backup.json`
- `requests_data_backup.json`

### PostgreSQL Backup

```bash
# Backup
docker exec asset-management-db pg_dump -U asset_admin asset_management > backup.sql

# Restore
docker exec -i asset-management-db psql -U asset_admin asset_management < backup.sql
```

## Docker Compose Configuration

The `docker-compose.yml` includes:

1. **PostgreSQL Service**
   - Image: postgres:15-alpine
   - Persistent volume for data
   - Health check for readiness
   - Port 5432 exposed

2. **Application Service**
   - Depends on PostgreSQL
   - Waits for database to be healthy
   - Automatic database initialization
   - Automatic migration if needed

## Troubleshooting

### Database Connection Issues

**Problem**: Application can't connect to PostgreSQL

**Solutions**:
1. Check PostgreSQL is running: `docker ps`
2. Check DATABASE_URL is correct
3. Verify PostgreSQL health: `docker logs asset-management-db`
4. Test connection: `pg_isready -h localhost -U asset_admin -d asset_management`

### Migration Errors

**Problem**: Migration script fails

**Solutions**:
1. Check JSON files exist and are valid
2. Verify database is empty (migration won't overwrite existing data)
3. Check database permissions
4. Review error logs for specific issues

### Data Not Appearing

**Problem**: Data migrated but not showing in application

**Solutions**:
1. Check database has data: 
   ```bash
   docker exec -it asset-management-db psql -U asset_admin -d asset_management -c "SELECT COUNT(*) FROM assets;"
   ```
2. Restart application container
3. Check application logs: `docker logs asset-management-system`

## Development Tips

### Accessing PostgreSQL

```bash
# Using Docker
docker exec -it asset-management-db psql -U asset_admin -d asset_management

# Common queries
SELECT COUNT(*) FROM assets;
SELECT COUNT(*) FROM tickets;
SELECT * FROM tickets ORDER BY date DESC LIMIT 5;
```

### Reset Database

```bash
# Stop containers
docker-compose down

# Remove volume (WARNING: deletes all data)
docker volume rm it-asset-management_postgres_data

# Start fresh
docker-compose up -d
```

### Running Migrations Again

If you need to re-run migration:

1. Clear database:
   ```sql
   TRUNCATE assets, tickets, ticket_replies, ticket_notes, requests CASCADE;
   ```

2. Run migration:
   ```bash
   python migrate_json_to_postgres.py
   ```

## Performance Considerations

### Indexes

The database includes indexes on:
- `ticket_number` (unique)
- Foreign keys for relationships

### Query Optimization

- Tickets are ordered by date (DESC) for latest-first display
- Relationships use lazy loading to avoid unnecessary queries
- Use `db.session.commit()` only after all related operations

## Security Notes

1. **Change Default Password**: Update PostgreSQL password in production
2. **Environment Variables**: Use `.env` file for sensitive data
3. **Network Security**: Don't expose PostgreSQL port (5432) publicly
4. **Backup Regularly**: Schedule automated backups
5. **SSL/TLS**: Enable SSL for PostgreSQL connections in production

## Rollback to JSON (If Needed)

If you need to rollback to JSON storage:

1. Export current database:
   ```bash
   python export_db_to_json.py
   ```

2. Rename backup files:
   ```bash
   mv assets_data_backup.json assets_data.json
   mv tickets_data_backup.json tickets_data.json
   mv requests_data_backup.json requests_data.json
   ```

3. Use the old version of `server.py` (from git history)

## Support

For issues or questions:
1. Check application logs: `docker logs asset-management-system`
2. Check database logs: `docker logs asset-management-db`
3. Review this documentation
4. Check PostgreSQL documentation: https://www.postgresql.org/docs/
