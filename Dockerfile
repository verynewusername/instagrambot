FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install with better ARM support
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --prefer-binary -r requirements.txt

# Copy source code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

ENV PYTHONUNBUFFERED=1
CMD ["python", "main.py"]
