# Railway Deployment Configuration

## Python Version

Railway defaults to Python 3.13 which may not be compatible with some packages (e.g., pydantic-core).

Create `runtime.txt` in backend root:
```
python-3.11.9
```

## Procfile

Railway needs explicit start command for FastAPI:

```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## Dockerfile (Alternative)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose port
EXPOSE 8000

# Start command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Common Issues

### "No start command detected"
Create `Procfile` with web command.

### "Failed to build pydantic-core"
Python 3.13 not compatible. Use `runtime.txt` with python-3.11.9.

### Build timeout
Railway has build time limits. Use Dockerfile for complex builds.

## CLI Commands

```bash
# Login
railway login

# Create project
railway init --name project-name

# Deploy
railway up --service service-name --detach

# Check status
railway status

# View logs
railway logs --service service-name

# Get domain
railway domain

# Link to project
railway link
```
