FROM python:3.12

WORKDIR /app

ENV POETRY_VERSION=1.8.2 \
    POETRY_HOME=/opt/poetry \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

RUN apt-get update && apt-get install -y --no-install-recommends make \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry==$POETRY_VERSION
COPY poetry.lock pyproject.toml /app/
RUN poetry install --no-root

RUN groupadd -r appuser && useradd --no-log-init -r -g appuser appuser

COPY . /app/
RUN chown -R appuser:appuser /app/

RUN mkdir -p /var/log/myapp \
    && chown -R appuser:appuser /var/log/myapp \
    && chmod -R 755 /var/log/myapp

USER appuser

CMD ["bash", "-c", "./start.sh"]