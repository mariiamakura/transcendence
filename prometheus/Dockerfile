FROM prom/prometheus:latest

ARG PROMETHEUS_USER
ARG PROMETHEUS_PASSWORD

COPY prometheus.yml /etc/prometheus/
COPY rules.yml /etc/prometheus/
COPY web-config.yml /etc/prometheus/

RUN sed -i "s/username: random/username: ${PROMETHEUS_USER}/g" /etc/prometheus/prometheus.yml && \
	sed -i "s/password: random/password: ${PROMETHEUS_PASSWORD}/g" /etc/prometheus/prometheus.yml

COPY certs_prometheus/prometheus.crt /etc/prometheus/
COPY certs_prometheus/prometheus.key /etc/prometheus/
COPY rootCA.pem /etc/prometheus

EXPOSE 9090

CMD ["--config.file=/etc/prometheus/prometheus.yml", \ 
	"--web.config.file=/etc/prometheus/web-config.yml", \
	"--storage.tsdb.retention.time=10d", \
	"--storage.tsdb.retention.size=3GB"]