FROM python:3.9-alpine

WORKDIR /app

COPY requirements.txt .

RUN apk add --no-cache --virtual .build-deps gcc musl-dev libffi-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps \
    && addgroup -S appgroup \
    && adduser -S appuser -G appgroup

COPY app.py .

USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
