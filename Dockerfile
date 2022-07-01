FROM python:3.10.2-slim as python-base

# https://stackoverflow.com/questions/59812009/what-is-the-use-of-pythonunbuffered-in-docker-file
# writes Python output to stderr and stdout. Has no influence on stdin
ENV PYTHONUNBUFFERED=1
# won't write the .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# useful for (i) when no space on the HD; (ii) avoid unexpected behaviour
ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
# poetry
# https://python-poetry.org/docs/configuration/#using-environment-variables
ENV POETRY_VERSION=1.1.13
ENV POETRY_HOME="/opt/poetry"
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV POETRY_NO_INTERACTION=1
# paths
ENV PYSETUP_PATH="/opt/pysetup"
ENV VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

FROM python-base as builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential

RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

WORKDIR /bot
COPY poetry.lock pyproject.toml /bot/

RUN poetry install --no-dev

COPY ./bot /bot
COPY ./main.py /

ENV PATH="/bot/.venv/bin:$PATH"

WORKDIR /

ENTRYPOINT ["python", "-m", "main"]
