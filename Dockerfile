FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Explicitly set permissions for pi.txt and make sure it's readable
RUN chmod 644 pi.txt && \
    useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app

USER app

ENV PYTHONUNBUFFERED=1
CMD ["python", "main.py"]
