FROM python:3.13-alpine AS builder

WORKDIR /app

COPY requirements.txt .

RUN apk add --no-cache --virtual .build-deps gcc musl-dev libffi-dev \
    && pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install --no-cache-dir --target=/install -r requirements.txt \
    && apk del .build-deps

FROM python:3.13-alpine

WORKDIR /app

# Quitamos pip/setuptools/wheel/ensurepip de la imagen final: no hacen
# falta en runtime y traían CVEs (setuptools viejo, msgpack vendorizado
# dentro de pip) que no se limpian con un simple pip install --upgrade.
RUN apk upgrade --no-cache \
    && PYSITE=/usr/local/lib/python3.13/site-packages \
    && rm -rf /usr/local/lib/python3.13/ensurepip \
       "$PYSITE"/pip "$PYSITE"/pip-*.dist-info \
       "$PYSITE"/setuptools "$PYSITE"/setuptools-*.dist-info \
       "$PYSITE"/wheel "$PYSITE"/wheel-*.dist-info \
       "$PYSITE"/pkg_resources "$PYSITE"/_distutils_hack \
    && addgroup -S appgroup \
    && adduser -S appuser -G appgroup

COPY --from=builder /install /usr/local/lib/python3.13/site-packages
COPY app.py .

USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
