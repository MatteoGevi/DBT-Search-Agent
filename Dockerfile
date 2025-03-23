FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY pyproject.toml poetry.lock ./

# Install system dependencies and Python packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/* \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev

# Copy application code
COPY src/ ./src/
COPY .env ./

# Set environment variables
ENV PYTHONPATH=/app

# Run the application
CMD ["python", "-m", "src.main"] 