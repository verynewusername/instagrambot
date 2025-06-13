FROM python:3.11-slim

WORKDIR /app

# Install git and git-lfs
RUN apt-get update && \
    apt-get install -y git git-lfs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Pull LFS files to get the actual pi.txt content
RUN git lfs pull || echo "No LFS files found"

# Explicitly set permissions for pi.txt and make sure it's readable
RUN chmod 644 pi.txt && \
    useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app

USER app

ENV PYTHONUNBUFFERED=1
CMD ["python", "main.py"]
