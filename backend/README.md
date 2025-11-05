# Login Service

A minimal Django REST API service for user authentication with email and password only.

## Features

- User registration with email and password
- User login with email and password
- Session-based authentication
- PostgreSQL database integration
- ZODB (Zope Object Database) support
- CORS enabled for cross-origin requests
- Docker and Docker Compose support

## Quick Start with Docker

> **New to Docker?** Check out the detailed [DOCKER_SETUP.md](DOCKER_SETUP.md) guide for step-by-step instructions!

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop) installed and running
- Verify installation: `docker --version` and `docker-compose --version`

### Step 1: Create Environment File

Create a `.env` file in the project root with your database credentials:

**You can use ANY username and password you want!** PostGIS will accept any credentials.

```env
DATABASE_NAME=dev
DATABASE_USERNAME=myuser
DATABASE_PASSWORD=mypassword123
```

**Example options:**
- `DATABASE_USERNAME=admin` and `DATABASE_PASSWORD=securepass123`
- `DATABASE_USERNAME=dbuser` and `DATABASE_PASSWORD=mysecretpass`
- Or keep defaults: `DATABASE_USERNAME=postgres` and `DATABASE_PASSWORD=postgres`

### Step 2: Start the Services

```bash
docker-compose up --build
```

**What happens:**
- First time: Downloads PostGIS image (~500MB) and builds your app
- Creates database with your credentials
- Runs Django migrations automatically
- Starts both database and web server

**Wait for this message:**
```
web_1  | Starting development server at http://0.0.0.0:8000/
```

### Step 3: Verify It's Working

- Open: `http://localhost:8000/is_logged_in/`
- Should return: `{"logged_in": false, "email": null}`

### Common Commands

```bash
# Start services (background)
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Stop and remove everything (⚠️ deletes data)
docker-compose down -v
```

**Need help?** See [DOCKER_SETUP.md](DOCKER_SETUP.md) for detailed troubleshooting and explanations.

## Manual Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure database settings in `api/settings.py` or set environment variables:
   - `DATABASE_NAME`
   - `DATABASE_USERNAME`
   - `DATABASE_PASSWORD`
   - `DATABASE_HOST`
   - `DATABASE_PORT`

3. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```

## Testing with Postman

### Prerequisites
1. Make sure the service is running (see Quick Start with Docker above)
2. Open Postman or any HTTP client tool

### Important Notes
- All POST requests use **form-data** or **x-www-form-urlencoded** (not JSON)
- The API uses **session-based authentication**, so cookies are important
- Make sure to enable cookies in your HTTP client

### Step-by-Step Testing Guide

#### 1. Test Register Endpoint

**Request:**
- **Method:** `POST`
- **URL:** `http://localhost:8000/register/`
- **Body Type:** `form-data` or `x-www-form-urlencoded`
- **Body:**
  - `email`: `test@example.com`
  - `password`: `testpass123`

**Expected Response (201 Created):**
```json
{
  "message": "User registered successfully",
  "email": "test@example.com"
}
```

**Test Cases:**
- ✅ Valid email and password → Should return 201
- ❌ Missing email → Should return 400 with error
- ❌ Missing password → Should return 400 with error
- ❌ Invalid email format (no @) → Should return 400
- ❌ Duplicate email → Should return 400 with "User with this email already exists"

#### 2. Test Login Endpoint

**Request:**
- **Method:** `POST`
- **URL:** `http://localhost:8000/login/`
- **Body Type:** `form-data` or `x-www-form-urlencoded`
- **Body:**
  - `email`: `test@example.com`
  - `password`: `testpass123`
- **Important:** Make sure cookies are enabled/saved from previous requests

**Expected Response (200 OK):**
```json
{
  "message": "Login successful",
  "email": "test@example.com",
  "is_admin": false
}
```

**Test Cases:**
- ✅ Valid credentials → Should return 200
- ❌ Wrong password → Should return 401 with "Invalid credentials"
- ❌ Non-existent user → Should return 401 with "Invalid credentials"
- ❌ Missing email or password → Should return 400

#### 3. Test Is Logged In Endpoint

**Request:**
- **Method:** `GET`
- **URL:** `http://localhost:8000/is_logged_in/`
- **Important:** Include cookies from login request

**Expected Response (200 OK) - When logged in:**
```json
{
  "logged_in": true,
  "email": "test@example.com",
  "is_admin": false
}
```

**Expected Response (200 OK) - When NOT logged in:**
```json
{
  "logged_in": false,
  "email": null
}
```

**Test Cases:**
- ✅ After login with cookies → Should return `logged_in: true`
- ✅ Without cookies/new session → Should return `logged_in: false`

### Complete Testing Flow

1. **Register a new user:**
   ```
   POST http://localhost:8000/register/
   Body: email=user1@example.com&password=mypassword123
   ```

2. **Check if logged in (should be false):**
   ```
   GET http://localhost:8000/is_logged_in/
   Expected: {"logged_in": false, "email": null}
   ```

3. **Login:**
   ```
   POST http://localhost:8000/login/
   Body: email=user1@example.com&password=mypassword123
   Save cookies from response
   ```

4. **Check if logged in (should be true):**
   ```
   GET http://localhost:8000/is_logged_in/
   (Include cookies from login)
   Expected: {"logged_in": true, "email": "user1@example.com", "is_admin": false}
   ```

### Postman Tips

1. **Enable Cookies:** Go to Postman Settings → General → Enable "Automatically follow redirects" and ensure cookies are enabled
2. **Use Postman's Cookie Manager:** View cookies sent/received in the Cookies section
3. **Save Cookies:** After login, Postman should automatically save session cookies
4. **Use Collection:** Create a Postman collection with all three endpoints for easy testing

### Testing with cURL (Alternative)

If you prefer command line:

```bash
# Register
curl -X POST http://localhost:8000/register/ \
  -d "email=test@example.com" \
  -d "password=testpass123" \
  -c cookies.txt

# Login
curl -X POST http://localhost:8000/login/ \
  -d "email=test@example.com" \
  -d "password=testpass123" \
  -b cookies.txt \
  -c cookies.txt

# Check logged in
curl -X GET http://localhost:8000/is_logged_in/ \
  -b cookies.txt
```

## API Endpoints Reference

### POST /register/
Register a new user with email and password.

**Request Body (form-data):**
- `email`: string (required)
- `password`: string (required)

**Response (201 Created):**
```json
{
  "message": "User registered successfully",
  "email": "user@example.com"
}
```

**Response (400 Bad Request):**
```json
{
  "error": "email and password required"
}
```
or
```json
{
  "error": "User with this email already exists"
}
```

### POST /login/
Login endpoint that accepts email and password.

**Request Body (form-data):**
- `email`: string (required)
- `password`: string (required)

**Response (200 OK):**
```json
{
  "message": "Login successful",
  "email": "user@example.com",
  "is_admin": false
}
```

**Response (401 Unauthorized):**
```json
{
  "error": "Invalid credentials"
}
```

### GET /is_logged_in/
Check if user is currently logged in.

**Response (200 OK) - Logged in:**
```json
{
  "logged_in": true,
  "email": "user@example.com",
  "is_admin": false
}
```

**Response (200 OK) - Not logged in:**
```json
{
  "logged_in": false,
  "email": null
}
```

## Project Structure

```
login_service/
├── api/                # Django project settings
│   ├── settings.py     # Django configuration
│   ├── urls.py         # URL routing
│   ├── wsgi.py         # WSGI configuration
│   └── asgi.py         # ASGI configuration
├── app_auth/           # Authentication app
│   ├── models.py       # User model (email/password only)
│   ├── views.py        # Register, Login, and status views
│   ├── admin.py        # Django admin configuration
│   └── migrations/     # Database migrations
├── zodb/               # ZODB management utilities
│   └── zodb_management.py
├── zodb_data/          # ZODB data storage
├── manage.py           # Django management script
├── Dockerfile          # Docker image configuration
├── docker-compose.yml  # Docker Compose configuration
├── entrypoint.sh       # Container startup script
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

