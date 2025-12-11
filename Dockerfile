FROM python:3.9-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    curl \
    && rm -rf /var/lib/apt/lists/*

# copy requirements file (you provided "requirement.txt")
COPY requirement.txt /app/requirement.txt

RUN pip install --no-cache-dir -r /app/requirement.txt

COPY . /app

EXPOSE 5000

CMD ["python", "app.py"]