# first stage
FROM python:3.10-slim as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install virtualenv

RUN virtualenv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

# another stage
FROM python:3.10-slim

COPY --from=builder /opt/venv /opt/venv
WORKDIR /app
COPY app.py /app
ENV PATH="/opt/venv/bin:$PATH"

CMD ["python", "app.py"] 
