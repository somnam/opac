FROM python:3.11-slim-buster

WORKDIR /root

ENV DEBIAN_FRONTEND=noninteractive \
    TERM=xterm \
    PIPX_VERSION=1.2.0 \
    POETRY_VERSION=1.5.1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true

# Create local user
RUN useradd opac --create-home --shell /bin/bash

# Work in users directory
WORKDIR /home/opac

# Switch to user
USER opac

# Set user path
ENV PATH="/home/opac/.local/bin:$PATH"

# Copy requirements file
COPY --chown=opac:opac ./server/pyproject.toml ./server/poetry.lock /home/opac/
COPY --chown=opac:opac ./server/src/__init__.py /home/opac/src/__init__.py

# Install pipx and poetry
RUN pip install "pipx==$PIPX_VERSION"
RUN pipx install "poetry==$POETRY_VERSION"
# Install python dependencies
RUN poetry install --no-interaction --no-ansi

# Copy application files
COPY --chown=opac:opac ./server/ /home/opac/

# Expose port
EXPOSE 8888

# Run app
CMD scripts/run-app
