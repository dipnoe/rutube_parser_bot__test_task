FROM python:3.12

WORKDIR /app

ENV POETRY_VERSION=1.8.0
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true

RUN apt-get update && apt-get install -y curl

RUN curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s $POETRY_HOME/bin/poetry /usr/local/bin/poetry

COPY poetry.lock pyproject.toml /app/

RUN poetry install --no-root

CMD ["bash", "-c", "start.sh"]