# Container Mode Sample - Dockerfile
# This demonstrates how to containerize a dtPyAppFramework application

# Use Python 3.12 slim image for smaller size
FROM python:3.12-slim

# Set metadata
LABEL maintainer="dtPyAppFramework Team"
LABEL description="Container Mode Sample Application"
LABEL version="1.0.0"

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV CONTAINER_MODE=true
ENV PYTHONPATH=/app

# Create application directory
WORKDIR /app

# Create a non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy main project requirements first for better Docker layer caching
COPY requirements.txt ./

# Install system dependencies and Python packages in a single layer
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt

# Copy sample-specific requirements if they exist (for additional dependencies)
COPY samples/container_mode/requirements.txt* ./sample-requirements.txt*
RUN if [ -f sample-requirements.txt ]; then \
        # Filter out comments and empty lines, install only uncommented dependencies
        grep -v '^#' sample-requirements.txt | grep -v '^$' | xargs -r pip install --no-cache-dir; \
    fi

# Copy the framework source code
COPY ./src/dtPyAppFramework ./dtPyAppFramework/

# Copy the sample application
COPY ./samples/container_mode/container_app.py ./sample/

# Create required directories with proper permissions
RUN mkdir -p /app/config /app/data /app/logs /app/temp && \
    chown -R appuser:appuser /app && \
    chmod -R 755 /app

# Switch to non-root user
USER appuser

# Health check to ensure the application can start
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python sample/container_app.py --task config --container || exit 1

# Default command - runs the sample with demonstration mode
CMD ["python", "sample/container_app.py", "--container", "--demo-mode"]