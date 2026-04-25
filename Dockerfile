# Use a lightweight Python base image
FROM python:3.9-slim

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies (for building or running scripts)
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Set permissions for the startup script
RUN chmod +x start.sh

# Environment variables for Cloud Run
# Cloud Run sets the $PORT variable (usually 8080)
ENV PORT=8080
ENV API_URL=http://localhost:8000

# Expose the ports (for documentation purposes)
EXPOSE 8080
EXPOSE 8000

# Execute the startup script
CMD ["./start.sh"]
