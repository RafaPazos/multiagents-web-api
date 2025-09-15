FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install -r requirements.txt

# Create necessary directories
RUN mkdir -p data

# Copy application code
COPY . .

# Expose the port
EXPOSE 8282

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8282"]