FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
COPY scripts/ ./scripts/
RUN python scripts/check_imports.py
CMD ["tail", "-f", "/dev/null"]
# CMD ["python","src/main.py"]