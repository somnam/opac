FROM python:3.7-slim-buster

WORKDIR /root

ENV DEBIAN_FRONTEND=noninteractive \
    TERM=xterm

RUN apt-get update \
    && mkdir -p /usr/share/man/man1 \
    && apt-get install -y --no-install-recommends sqlite3 \
    && apt-get clean && rm -rf /var/lib/apt/lists


# Create server user
RUN useradd server --create-home --shell /bin/bash\
    && su -c "mkdir -p /home/server/.local/bin" server

# Work in server users directory
WORKDIR /home/server

# Switch to server user
USER server

# Set user path
ENV PATH /home/server/.local/bin:$PATH

# Copy rc files
COPY --chown=server:server ./docker/.bash_aliases ./docker/.vimrc /home/server/

# Copy requirements file
COPY --chown=server:server ./server/setup.py /home/server

# Build requirements
RUN pip install --user pip-tools &&\
    pip-compile --quiet setup.py &&\
    pip-sync --user requirements.txt &&\
    pip install --user -e . &&\
    rm -rf /home/server/.cache

# Copy application files
COPY --chown=server:server ./server/ /home/server/

# Expose port
EXPOSE 8888

# Run app.
CMD ["run_app"]
