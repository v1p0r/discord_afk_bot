FROM python:3.11-slim

WORKDIR /app

# Install dependencies first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot source
COPY . .

# -u = unbuffered stdout so logs appear in docker logs immediately
CMD ["python", "-u", "bot.py"]
