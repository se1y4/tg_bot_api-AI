FROM python:3.13.1 as base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

WORKDIR /app

FROM base as builder

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.8.5

RUN pip install "poetry==$POETRY_VERSION"
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

COPY ./chat_bot/pyproject.toml .
COPY ./chat_bot/poetry.lock .
RUN . /venv/bin/activate && poetry install --no-root --no-dev

FROM base as final
COPY --from=builder /venv /venv

ENV PATH="/venv/bin:$PATH"
COPY ./scripts/bot-entrypoint.sh /scripts/bot-entrypoint.sh
COPY ./chat_bot/bot ./bot

RUN chmod a+x /scripts/bot-entrypoint.sh

ENTRYPOINT ["/bin/sh", "/scripts/bot-entrypoint.sh"]