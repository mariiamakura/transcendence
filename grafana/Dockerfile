FROM grafana/grafana:latest

ARG PROMETHEUS_PASSWORD

COPY datasource.yaml /etc/grafana/provisioning/datasources/datasource.yaml
COPY rootCA.pem /etc/grafana
COPY certs_grafana/grafana.crt /etc/grafana
COPY certs_grafana/grafana.key /etc/grafana
COPY grafana.ini /etc/grafana

RUN sed -i '/tlsCACert/ r /etc/grafana/rootCA.pem' /etc/grafana/provisioning/datasources/datasource.yaml && \
	sed -i "s/basicAuthPassword: random/basicAuthPassword: ${PROMETHEUS_PASSWORD}/g" /etc/grafana/provisioning/datasources/datasource.yaml

EXPOSE 3000