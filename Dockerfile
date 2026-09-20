FROM node:20-alpine AS editor-builder

WORKDIR /build/editor_next
COPY src/modu_math_web/editor_next/package.json src/modu_math_web/editor_next/package-lock.json ./
RUN npm ci
COPY src/modu_math_web/editor_next/ ./
RUN npm run build


FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

WORKDIR /app
COPY . /app
COPY --from=editor-builder /build/editor_next/static/editor_next/konva_assets/ /app/src/modu_math_web/editor_next/static/editor_next/konva_assets/
RUN pip install --no-cache-dir .

EXPOSE 8000
CMD ["gunicorn", "modu_math_web.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
