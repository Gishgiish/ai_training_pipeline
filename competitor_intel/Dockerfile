FROM python:3.12-slim

WORKDIR /app

# Intall system dependencies required for Playwright (chromium)
RUN apt-get update && apt-get install -y \
    wget \
    libnss3 \
    libatk-bridge2.0-0 \
    libdrm2 \
    libxkbcommon0 \
    libgbm1 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

# Copy and install python dependencies 
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers and their OS dependencies
RUN playwright install chromium
RUN playwright install-deps chromium

# Copy the rest of the application code
COPY . .

# Create the data directory for output
RUN mkdir -p data

# The command to run when the container starts
CMD ["python", "run_pipeline.py"]