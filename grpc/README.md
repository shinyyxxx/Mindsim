## Django + PostGIS + ZODB starter

This project uses ZODB as the main object store and PostGIS (GeoDjango) for spatial indexing.

### Requirements
- Python 3.11+
- PostgreSQL 14+ with PostGIS
- macOS: `brew install postgresql postgis gdal geos proj`

### Install
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file (same directory as `manage.py`) with:
```env
DEBUG=true
SECRET_KEY=dev-secret-key-change-me

POSTGRES_DB=gis
POSTGRES_USER=gis
POSTGRES_PASSWORD=gis
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

ZODB_FILE_PATH=./var/zodb.fs
```

Enable PostGIS in your database:
```sql
CREATE EXTENSION IF NOT EXISTS postgis;
```

### Run
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### API
- POST `/api/places/create` JSON: `{ "name": str, "description": str, "lat": float, "lng": float }`
- GET `/api/places/nearby?lat=..&lng=..&km=5`

ZODB stores the rich object; `PlaceIndex` keeps coordinates for spatial queries.

