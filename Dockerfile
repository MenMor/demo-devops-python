FROM python:3.11-slim as builder

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

FROM python:3.11-slim

WORKDIR /app
RUN useradd -m appuser && chown -R appuser:appuser /app

COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/* && \
    rm -rf /wheels && \
    mkdir -p /app/static && \
    chown appuser:appuser /app/static

COPY . .

# Recolectamos archivos estáticos ANTES de cambiar al usuario sin privilegios
RUN python manage.py collectstatic --noinput

COPY .env .env  

ENV DJANGO_SETTINGS_MODULE=demo.settings
ENV PORT=8000
EXPOSE $PORT

# Ahora cambiamos al usuario sin privilegios
USER appuser

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:$PORT/api/ || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "demo.wsgi"]
