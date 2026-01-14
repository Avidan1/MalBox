# Use a modern Python image
FROM python:3.13-slim

# Install uv inside the container
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy dependency files first for caching
COPY pyproject.toml uv.lock ./

# Install dependencies using uv (fast and reliable)
RUN uv sync --frozen --no-cache

# Copy the rest of the application
COPY . .

# Set environment variable for Redis
ENV REDIS_HOST=redis

# Start the worker using uv to ensure the correct environment
CMD ["uv", "run", "worker.py"]