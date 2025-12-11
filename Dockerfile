FROM python:3.9-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirement.txt
RUN pip install --no-cache-dir -r requirement.txt

COPY . /app

EXPOSE 5000

CMD ["python", "app.py"]