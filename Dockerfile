FROM	ubuntu:18.04
ENV	OBFS=http_simple \
	PROTOCOL=origin  \
	CIPHER=chacha20	
COPY 	install.sh shadowsocks.json.template ./
RUN 	bash install.sh
RUN	apt-get update && apt-get install -y gettext-base
CMD     envsubst < shadowsocks.json.template > /shadowsocks.json && /usr/local/shadowsocks/server.py -c /shadowsocks.json
