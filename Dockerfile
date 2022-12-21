FROM python:3.11

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100

RUN pip install --upgrade pip
RUN pip install poetry

RUN apt-get update && apt-get install -y swig zbar-tools

WORKDIR /app
COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

COPY . ./

CMD [ "poetry", "run", "run" ]