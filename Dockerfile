FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 80

CMD ["gunicorn", "--bind", "0.0.0.0:80", "--workers", "3", "--timeout", "120", "movie_api.wsgi:application"]
