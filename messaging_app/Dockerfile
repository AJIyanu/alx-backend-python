# Use Python 3.10 as the base image
# This tells Docker to start with a pre-built image that has Python 3.10 installed
# "slim" version is smaller - has Python but fewer extra packages
FROM python:3.10-slim

# Set environment variables
# These control how Python behaves inside the container:
# PYTHONDONTWRITEBYTECODE=1: Prevents Python from writing .pyc files (compiled bytecode)
# PYTHONUNBUFFERED=1: Forces Python output to appear immediately (good for logs)
# DJANGO_SETTINGS_MODULE: Tells Django which settings file to use
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=messaging_app.settings

# Set work directory
# This is like doing "cd /app" - all future commands will run from this directory
# Creates the /app folder if it doesn't exist
WORKDIR /app

# Install system dependencies
# apt-get update: Updates the package list (like refreshing available software)
# apt-get install: Installs system packages needed by some Python libraries:
#   - gcc: Compiler needed for some Python packages
#   - postgresql-client: Tools to connect to PostgreSQL databases
#   - libpq-dev: Development files needed to build PostgreSQL-related Python packages
# --no-install-recommends: Only install essential packages, not suggested ones
# rm -rf /var/lib/apt/lists/*: Clean up package cache to reduce image size
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        postgresql-client \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first (for better Docker layer caching)
# This copies requirements.txt from your computer to the container
# We do this BEFORE copying all code - if requirements don't change,
# Docker can reuse this layer and skip reinstalling packages (saves time!)
COPY requirements.txt .

# Install Python dependencies
# pip install --upgrade pip: Updates pip to latest version
# pip install -r requirements.txt: Installs all packages listed in requirements.txt
# --no-cache-dir: Don't store downloaded packages (reduces image size)
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the entire messaging_app project
# The "." means "copy everything from current directory on your computer"
# The second "." means "copy it to current directory in container" (which is /app)
# This includes your Django code, manage.py, settings, etc.
COPY . .

# Create static and media directories
# mkdir -p: Creates directories (and parent directories if needed)
# /app/static: Where Django stores CSS, JS, images for your website
# /app/media: Where user uploads (like profile pictures, attachments) are stored
RUN mkdir -p /app/static /app/media

# Collect static files (if you have any)
# Django command that gathers all CSS/JS/images into one place
# --noinput: Don't ask for user confirmation
# --clear: Remove old static files first
# || true: If this fails, continue anyway (won't break the build)
RUN python manage.py collectstatic --noinput --clear || true

# Create a non-root user
# Security best practice: don't run apps as root user
# adduser --disabled-password: Creates user without login password
# --gecos '': Skips asking for user info
# chown -R: Changes ownership of /app directory to appuser
# USER appuser: Switch to this user for remaining commands
RUN adduser --disabled-password --gecos '' appuser \
    && chown -R appuser:appuser /app
USER appuser

# Expose port 8000
# This tells Docker that your app will listen on port 8000
# It's like saying "my app will be available on port 8000"
# You still need to map it when running: docker run -p 8000:8000
EXPOSE 8000

# Health check
# Docker periodically runs this command to check if your app is healthy
# --interval=30s: Check every 30 seconds
# --timeout=30s: If check takes longer than 30s, consider it failed  
# --start-period=5s: Wait 5s before starting health checks
# --retries=3: Try 3 times before marking as unhealthy
# The command tries to make a web request to your app
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000')" || exit 1

# Run migrations as part of the image build process
# This is a good practice for production images
RUN python3 manage.py makemigrations && \
    python3 manage.py migrate

# Now, the CMD simply runs the server, as migrations are already handled
CMD ["python3", "manage.py", "runserver"]