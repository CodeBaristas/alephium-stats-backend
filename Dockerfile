FROM python:3.11-slim

################################################################################
# PYTHON INIT
ENV PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  LANG=C.UTF-8 \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100

################################################################################
# SSH SETUP
RUN apt update && apt install -y curl openssh-client git gcc expect
RUN mkdir -p -m 0600 /root/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts

################################################################################
# POETRY
RUN pip3 install --upgrade pip \
  && pip3 install poetry \
  && poetry config virtualenvs.create false

################################################################################
# INSTALL
RUN apt install -y pkg-config libmariadb3 libmariadb-dev default-mysql-client
WORKDIR /alephium_stats
COPY ./pyproject.toml ./poetry.lock ./
RUN --mount=type=ssh poetry install --no-dev --no-interaction --no-ansi -vvv

# RUN pip install poetry

################################################################################
# APP
COPY . .
EXPOSE 8000
ENTRYPOINT ./entrypoint.sh
