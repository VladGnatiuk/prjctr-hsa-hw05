FROM python:3.11-slim

WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements to temp folder and install Python dependencies
COPY ../src/requirements.txt /tmp/
COPY ../src/requirements.dev.txt /tmp/

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r /tmp/requirements.txt \
    && pip install --no-cache-dir -r /tmp/requirements.dev.txt \
    && rm /tmp/requirements.txt \
    && rm /tmp/requirements.dev.txt

# Keep container alive
CMD ["sleep", "infinity"]