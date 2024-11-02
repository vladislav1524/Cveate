FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libgdk-pixbuf2.0-0 \
    libcairo2 \
    libpango1.0-0 \
    libgdk-pixbuf2.0-dev \
    libgtk-3-dev \
    && apt-get clean
    
WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8000"]
