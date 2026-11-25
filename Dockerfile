FROM python:3.12-slim
# Install curl for AWS CLI installer
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Install AWS CLI v2 using the official AWS install script
RUN curl -fsSL https://awscli.amazonaws.com/v2/install.sh \
    | bash -s -- --system

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
COPY scripts/ ./scripts/
RUN python scripts/check_imports.py
# keep the container running indefinitely without actually running an application
CMD ["tail", "-f", "/dev/null"]
# CMD ["python","src/main.py"]