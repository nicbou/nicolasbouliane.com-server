FROM nginx:mainline-alpine
RUN apk add --no-cache openssl && rm -rf /tmp/packages

# Regular stuff
COPY nginx/configs/* /etc/nginx/configs/
COPY nginx/nginx.conf /etc/nginx/nginx.conf

# Let's encrypt stuff
ARG SSL_DOMAIN
ARG SSL_EMAIL
ENV SSL_DOMAIN=${SSL_DOMAIN}
ENV SSL_EMAIL=${SSL_EMAIL}

COPY scripts/start.sh ./start.sh
COPY scripts/reinstall-ssl-cert.sh /etc/periodic/hourly/reinstall-ssl-cert
RUN curl https://get.acme.sh | sh -s email=$SSL_EMAIL

ENTRYPOINT ./start.sh
