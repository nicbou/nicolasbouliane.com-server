FROM python:3.10-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/* \
    && git config --global pull.rebase false

COPY ./watch-for-updates.sh /watch-for-updates.sh

CMD /watch-for-updates.sh