# UniGo Backend

This is the backend API for the UniGo student ride sharing platform, built with FastAPI.

## Prerequisites

- Python 3.8+
- PostgreSQL database
- Virtual environment (recommended)

## Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   ```bash
   # On Linux/macOS:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   - For local development, copy `.env.local` to `.env`
   - For remote deployment, update the database configuration in `.env` file with correct credentials
   - Make sure the PostgreSQL database is accessible with the provided credentials

5. Initialize the database:
   ```bash
   python init_db.py
   ```

## Configuration

The project supports different environments through environment files:

- `.env.local` - Configuration for local development with local database
- `.env` - Configuration for deployment (remote database)

To use local development:
```bash
cp .env.local .env
```

To use remote database, update the `.env` file with correct credentials:
```bash
# Update this line with correct password
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD_HERE@101.32.244.111:5432/unigo
```

## Running the Application

### Development Mode

```bash
bash run.sh
```

### Production Mode

```bash
bash start.sh
```

The API will be available at `http://localhost:8001`

## API Documentation

- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

## Health Check

A health check endpoint is available at `/health` to verify the application is running correctly.

## Deployment

For production deployment, make sure to:

1. Set strong secret keys in the environment variables
2. Configure proper CORS origins
3. Use a production-ready database
4. Set up proper logging
5. Use a reverse proxy like Nginx