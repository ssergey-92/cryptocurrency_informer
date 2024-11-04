FROM python:3.12

ENV PYTHONUNBUFFERED=1

RUN apt-get update && pip install --upgrade pip && pip install poetry==1.8.4

WORKDIR /cryptocurrency_informer/cryptocurrency_app

ENV PYTHONPATH="/cryptocurrency_informer:${PYTHONPATH}"

COPY . .

RUN poetry config virtualenvs.create false --local && poetry install --without test

CMD ["/usr/local/bin/gunicorn", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:80", "main:app"]

