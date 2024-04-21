FROM python:3.12-slim as builder

WORKDIR /tech-scout

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc


COPY requirements.txt .

RUN pip wheel --no-cache-dir --no-deps --wheel-dir /tech-scout/wheels -r requirements.txt


FROM python:3.12-slim

WORKDIR /tech-scout

COPY --from=builder /tech-scout/wheels /wheels
COPY --from=builder /tech-scout/requirements.txt .

RUN pip install --no-cache /wheels/*

COPY tech-scout-scraper .

EXPOSE 8000

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
