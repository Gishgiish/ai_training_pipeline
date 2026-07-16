FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

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


RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers and their OS dependencies
RUN playwright install chromium
RUN playwright install-deps chromium

# Copy the rest of the application code
COPY . .

# Create the data directory for output
RUN mkdir -p data

# Expose the port that streamlit uses
EXPOSE 8501

# The command to run when the container starts
CMD ["streamlit", "run", "competitor_intel/dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]