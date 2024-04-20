FROM python:3.13-alpine

RUN apk update \
    && apk add --no-cache \
        git \
        rsync \
    && git config --global pull.rebase false \
    && mkdir -p /var/ursus/output

COPY ./watch-for-updates.py /watch-for-updates.py

CMD /watch-for-updates.py