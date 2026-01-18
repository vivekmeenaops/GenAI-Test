FROM python:3.9-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

RUN pip check && flake8 && mypy app.py

FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY --from=builder /app/* .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
