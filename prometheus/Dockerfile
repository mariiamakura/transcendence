FROM prom/prometheus:latest

COPY prometheus.yml /etc/prometheus/
COPY rules.yml /etc/prometheus/
COPY web-config.yml /etc/prometheus/

COPY certs_prometheus/prometheus.crt /etc/prometheus/
COPY certs_prometheus/prometheus.key /etc/prometheus/

# RUN chmod 777 /etc/prometheus/prometheus.crt && \
# 	chmod 777 /etc/prometheus/prometheus.key


EXPOSE 9090

CMD ["--config.file=/etc/prometheus/prometheus.yml", \ 
	"--web.config.file=/etc/prometheus/web-config.yml"]