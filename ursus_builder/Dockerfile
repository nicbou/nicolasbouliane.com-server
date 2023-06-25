FROM python:3.10-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends git rsync \
    && rm -rf /var/lib/apt/lists/* \
    && git config --global pull.rebase false \
    && mkdir -p /var/ursus/output

COPY ./watch-for-updates.py /watch-for-updates.py

CMD /watch-for-updates.py