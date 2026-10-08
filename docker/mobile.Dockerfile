FROM python:3.12-slim AS content-builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

WORKDIR /app
COPY pyproject.toml manage.py ./
COPY src ./src
COPY tools ./tools
COPY schema ./schema
COPY examples/problems ./examples/problems
COPY locales ./locales
COPY overrides ./overrides
RUN pip install --no-cache-dir . && \
    python tools/export_problem_content.py --root examples/problems --out /build/generated/examples/problems


FROM debian:bookworm-slim AS flutter-builder

ARG FLUTTER_VERSION=3.44.8
ARG BACKEND_API_BASE_URL=same-origin

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    git \
    unzip \
    xz-utils \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL "https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/flutter_linux_${FLUTTER_VERSION}-stable.tar.xz" \
    | tar -xJ -C /opt && \
    git config --global --add safe.directory /opt/flutter

ENV PATH="/opt/flutter/bin:/opt/flutter/bin/cache/dart-sdk/bin:${PATH}"

WORKDIR /app/apps/mobile
COPY apps/mobile/pubspec.yaml apps/mobile/pubspec.lock ./
RUN flutter pub get

COPY apps/mobile/ ./
COPY --from=content-builder /build/generated/examples/problems ./generated/examples/problems
RUN flutter build web --release --dart-define=BACKEND_API_BASE_URL=${BACKEND_API_BASE_URL}


FROM nginx:1.27-alpine

COPY docker/nginx-mobile.conf /etc/nginx/conf.d/default.conf
COPY --from=flutter-builder /app/apps/mobile/build/web /usr/share/nginx/html

EXPOSE 3000
