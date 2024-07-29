FROM python:3.12.4-alpine

WORKDIR /backend

RUN apt-get update

RUN pip install --upgrade pip \
    pip install --no-cache-dir --upgrade poetry

COPY pyproject.lock pyproject.toml ./

COPY . .

RUN poetry install

EXPOSE 8000

CMD poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

