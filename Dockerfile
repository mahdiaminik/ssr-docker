FROM python:3.9-alpine

ARG SSR_URL=https://github.com/winterssy/shadowsocksr/archive/manyuser.zip
ENV PASSWORD=password \
    METHOD=chacha20 \
    PROTOCOL=origin \
    OBFS=http_simple \
    LIMIT_PER_CON=8192 \
    LIMIT_PER_USER=81920

RUN set -ex && \
    apk add --no-cache libsodium gettext && \
    pip --no-cache-dir install requests $SSR_URL

COPY shadowsocks.json.template .

CMD envsubst < shadowsocks.json.template > /shadowsocks.json && ssserver -c /shadowsocks.json
