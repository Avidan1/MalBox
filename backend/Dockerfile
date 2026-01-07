# Use a more modern Python image (3.11) to support newer dependencies
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Set environment variable for Redis
ENV REDIS_HOST=localhost

# Start the worker
CMD ["python", "worker.py"]