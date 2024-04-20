FROM python:3.11-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends git rsync \
    && rm -rf /var/lib/apt/lists/* \

COPY ./watch-for-updates.py /watch-for-updates.py

CMD /watch-for-updates.py