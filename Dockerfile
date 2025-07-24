# Base image - always start with this
FROM python:3.9-slim
# Metadata about your container (optional but professional)
LABEL maintainer="your-email@example.com"
LABEL description="Cryptocurrency analysis environment"
LABEL version="1.0"
# Set working directory inside container
WORKDIR /app
# Install system dependencies first (for caching efficiency)
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*
# Copy requirements file first (Docker layer caching optimization)
COPY requirements.txt .
# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Copy application code
COPY src/ ./src/
COPY data/ ./data/
# Create output directory
RUN mkdir -p output
# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
# Expose port (documentation, doesn't actually open ports)
EXPOSE 8000
# Create non-root user (security best practice)
RUN useradd -m -u 1000 analyst
USER analyst
# Default command to run
CMD ["python", "src/analyzer.py"] 