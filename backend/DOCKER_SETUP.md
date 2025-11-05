# Docker Setup Guide for Login Service

This guide will walk you through setting up Docker and Docker Compose for the first time.

## Prerequisites

### 1. Install Docker Desktop

**For Windows:**
1. Download Docker Desktop from: https://www.docker.com/products/docker-desktop
2. Run the installer (`Docker Desktop Installer.exe`)
3. Follow the installation wizard
4. Restart your computer when prompted
5. Launch Docker Desktop from the Start menu
6. Wait for Docker to start (you'll see a whale icon in your system tray)

**For macOS:**
1. Download Docker Desktop from: https://www.docker.com/products/docker-desktop
2. Open the `.dmg` file and drag Docker to Applications
3. Launch Docker from Applications
4. Complete the setup wizard

**For Linux:**
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install docker.io docker-compose-plugin
sudo systemctl start docker
sudo systemctl enable docker

# Add your user to docker group (optional, to avoid sudo)
sudo usermod -aG docker $USER
```

### 2. Verify Installation

Open a terminal/command prompt and run:

```bash
docker --version
docker-compose --version
```

You should see version numbers. If you get an error, Docker might not be running - make sure Docker Desktop is started.

## Setting Up Your Login Service

### Step 1: Configure Database Credentials

**Yes, you can use ANY username and password you want!** PostGIS (which is PostgreSQL with spatial extensions) will accept any credentials you set.

1. **Create a `.env` file** in the project root (same folder as `docker-compose.yml`)

2. **Copy the example file:**
   ```bash
   # On Windows (PowerShell)
   Copy-Item .env.example .env
   
   # On Linux/Mac
   cp .env.example .env
   ```

3. **Edit `.env` with your preferred credentials:**
   ```env
   DATABASE_NAME=dev
   DATABASE_USERNAME=myuser
   DATABASE_PASSWORD=mypassword123
   ```

   **Important:** 
   - Use any username you want (e.g., `admin`, `dbuser`, `myuser`)
   - Use any password you want (make it secure!)
   - The database name can be anything (e.g., `dev`, `production`, `mydb`)

### Step 2: Build and Start the Services

1. **Open a terminal** in the project directory (where `docker-compose.yml` is located)

2. **Build and start everything:**
   ```bash
   docker-compose up --build
   ```

   What this does:
   - `--build` - Builds the Docker image for your Django app
   - Downloads the PostGIS database image if needed
   - Creates containers for both services
   - Starts the database and Django server

3. **First time setup takes a few minutes** because:
   - Docker downloads the PostGIS image (~500MB)
   - Docker builds your Python application image
   - Database initializes
   - Django runs migrations

4. **You'll know it's ready when you see:**
   ```
   web_1  | Starting development server at http://0.0.0.0:8000/
   web_1  | Quit the server with CONTROL-C.
   ```

### Step 3: Verify It's Working

1. **Open your browser** and go to: `http://localhost:8000`
   - You might see a 404 or Django error page - that's OK! The server is running.

2. **Test an endpoint:**
   - Try: `http://localhost:8000/is_logged_in/`
   - Should return: `{"logged_in": false, "email": null}`

## Common Docker Commands

### Start Services (in background)
```bash
docker-compose up -d
```
The `-d` flag runs containers in "detached" mode (background).

### Stop Services
```bash
docker-compose down
```
Stops and removes containers, but keeps data volumes.

### Stop and Remove Everything (including data)
```bash
docker-compose down -v
```
⚠️ **Warning:** This deletes your database data!

### View Logs
```bash
# All services
docker-compose logs

# Follow logs (live updates)
docker-compose logs -f

# Just the web service
docker-compose logs web

# Just the database
docker-compose logs db
```

### Restart Services
```bash
docker-compose restart
```

### Rebuild After Code Changes
```bash
docker-compose up --build
```

### Access Container Shell
```bash
# Access Django container
docker-compose exec web bash

# Access database container
docker-compose exec db psql -U myuser -d dev
# (Replace 'myuser' and 'dev' with your actual credentials)
```

### Run Django Commands
```bash
# Create superuser
docker-compose exec web python manage.py createsuperuser

# Run migrations manually
docker-compose exec web python manage.py migrate

# Access Django shell
docker-compose exec web python manage.py shell
```

## Understanding docker-compose.yml

Here's what each part does:

```yaml
services:
  db:                    # The database service
    image: postgis/postgis:16-3.4  # Uses PostGIS image
    environment:         # Sets database credentials
      POSTGRES_DB: ${DATABASE_NAME:-dev}
      # Uses DATABASE_NAME from .env, or "dev" if not set
      
  web:                   # Your Django application
    build: .             # Builds from Dockerfile in current directory
    depends_on:          # Waits for database to be healthy
      db:
        condition: service_healthy
```

## Troubleshooting

### "Cannot connect to Docker daemon"
- **Windows/Mac:** Make sure Docker Desktop is running
- **Linux:** Try `sudo systemctl start docker`

### "Port already in use"
- Port 8000 is already used? Change it in `docker-compose.yml`:
  ```yaml
  ports:
    - "8001:8000"  # Now accessible at http://localhost:8001
  ```
- Port 5432 (PostgreSQL) is used? Change it:
  ```yaml
  ports:
    - "5433:5432"  # Now accessible on port 5433
  ```

### "Database connection refused"
- Wait a bit longer - database takes time to initialize
- Check logs: `docker-compose logs db`
- Make sure `.env` file has correct credentials

### "Permission denied" (Linux)
- Add your user to docker group: `sudo usermod -aG docker $USER`
- Log out and back in
- Or use `sudo` (not recommended)

### Reset Everything
```bash
# Stop and remove containers
docker-compose down -v

# Remove all images (optional)
docker-compose down --rmi all

# Start fresh
docker-compose up --build
```

## What Gets Created?

When you run `docker-compose up`, Docker creates:

1. **Volumes** (persistent data storage):
   - `postgres_data` - Your database files
   - `zodb_data` - ZODB data files

2. **Networks** (for containers to communicate):
   - `login_service_default` - Internal network

3. **Containers** (running instances):
   - `login_service_db_1` - PostGIS database
   - `login_service_web_1` - Django application

## Best Practices

1. **Never commit `.env` file** - It contains sensitive credentials
2. **Use strong passwords** in production
3. **Keep Docker updated** - `docker-compose pull` to update images
4. **Backup your data** - Database is in the `postgres_data` volume
5. **Use `.env.example`** - Document what variables are needed

## Next Steps

Once Docker is running:
1. Test the API with Postman (see README.md)
2. Check logs if something goes wrong
3. Customize your `.env` file with your preferred credentials

Enjoy your Docker setup! 🐳

