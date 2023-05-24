FROM python:3.10.4-bullseye
LABEL authors="sigae"

ENV POETRY_VERSION=1.4.2 POETRY_HOME=/poetry
ENV PATH=/poetry/bin:$PATH
RUN curl -sSL https://install.python-poetry.org | python3 -
COPY . .

RUN poetry install --no-root

EXPOSE 8000

CMD poetry run uvicorn main:app --host 0.0.0.0