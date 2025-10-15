# Dockerfile for Base.vn Candidate API Wrapper

FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY api_server.py .
COPY api_client.py .
COPY data_processor.py .
COPY app.py .

# Expose port
EXPOSE 8000

# Environment variables (can be overridden)
ENV API_HOST=0.0.0.0
ENV API_PORT=8000

# Run the API server
CMD ["python", "api_server.py"]
