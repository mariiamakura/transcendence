FROM quay.io/prometheus/alertmanager:latest

COPY alertmanager.yml /etc/alertmanager/alertmanager.yml

COPY web-config.yml /etc/alertmanager/web-config.yml
COPY certs_alert/alert.key /etc/alertmanager/alert.key
COPY certs_alert/alert.crt /etc/alertmanager/alert.crt

CMD ["--config.file=/etc/alertmanager/alertmanager.yml", \
	"--web.config.file=/etc/alertmanager/web-config.yml"]