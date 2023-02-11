FROM python:3.10-slim-buster

WORKDIR /root

ENV DEBIAN_FRONTEND=noninteractive \
    TERM=xterm

# Create worker user
RUN useradd worker --create-home --shell /bin/bash

# Work in worker users directory
WORKDIR /home/worker

# Switch to worker user
USER worker

# Set user path
ENV PATH /home/worker/.local/bin:$PATH

# Copy rc files
COPY --chown=worker:worker ./docker/common/.bash_aliases ./docker/common/.vimrc /home/worker/

# Copy requirements file
COPY --chown=worker:worker ./server/setup.py ./server/setup.cfg /home/worker/

# Build requirements
RUN pip install --user pip-tools &&\
    pip-compile --quiet setup.py &&\
    pip-sync --user requirements.txt &&\
    pip install --user -e . &&\
    rm -rf /home/worker/.cache

# Copy application files
COPY --chown=worker:worker ./server/ ./etc/worker/supervisord.conf /home/worker/

# Run app.
# Run supervisor
CMD ["supervisord", "-c", "supervisord.conf"]
