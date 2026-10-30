FROM debian:bookworm-slim AS flutter-builder

ARG FLUTTER_VERSION=3.44.8
ARG BACKEND_API_BASE_URL=same-origin

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    git \
    python3 \
    unzip \
    xz-utils \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL "https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/flutter_linux_${FLUTTER_VERSION}-stable.tar.xz" \
    | tar -xJ -C /opt && \
    git config --global --add safe.directory /opt/flutter

ENV PATH="/opt/flutter/bin:/opt/flutter/bin/cache/dart-sdk/bin:${PATH}"

WORKDIR /app/apps/mobile

# Prepare project without offline problem assets or answer bundles
COPY apps/mobile/pubspec.yaml apps/mobile/pubspec.lock ./
# Remove offline generated problem asset declarations from student build
RUN sed -i '/- generated\//d' pubspec.yaml && \
    flutter pub get

COPY apps/mobile/lib ./lib
COPY apps/mobile/web ./web
COPY apps/mobile/assets/i18n ./assets/i18n
COPY apps/mobile/assets/characters ./assets/characters
COPY apps/mobile/scripts/prepare_student_build.py ./scripts/prepare_student_build.py

# Build student release app targeting lib/main_student.dart without authored problem answers
RUN flutter build web --release \
    --target lib/main_student.dart \
    --dart-define=BACKEND_API_BASE_URL=${BACKEND_API_BASE_URL} && \
    python3 scripts/prepare_student_build.py --verify-dir build/web && \
    chmod -R a+rX build/web


FROM nginx:1.27-alpine

COPY docker/nginx-mobile.conf /etc/nginx/conf.d/default.conf
COPY --from=flutter-builder /app/apps/mobile/build/web /usr/share/nginx/html

EXPOSE 3000
