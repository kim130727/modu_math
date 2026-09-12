FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir .

EXPOSE 8000
CMD ["gunicorn", "modu_math_web.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
