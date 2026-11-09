# Use official Python 3.12 slim image (Django 6 requires Python >= 3.12)
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# OpenShift runs containers as an arbitrary non-root UID in the root group (GID 0)
# so we give GID 0 group ownership on needed dirs
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install gunicorn whitenoise

# Copy project source
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Give the root group (GID 0) write access — required by OpenShift arbitrary UID policy
RUN chown -R 0:0 /app && chmod -R g=u /app

# Create media directory
RUN mkdir -p /app/media && chmod -R g=u /app/media

# OpenShift assigns a random UID; the container must NOT declare a specific USER
# but we ensure we're not explicitly root
EXPOSE 8080

# Copy and use entrypoint script (runs migrations + starts Gunicorn)
COPY entrypoint.sh /app/entrypoint.sh
RUN sed -i 's/\r$//' /app/entrypoint.sh && chmod +x /app/entrypoint.sh && chown 0:0 /app/entrypoint.sh

EXPOSE 8080

CMD ["/app/entrypoint.sh"]
