

# prometheus-server

This is a repository for setting up and configuring a server to run
*Prometheus* instance. It can be installed on a local machine or a remote
host. This set up is made for Linux.

### Setting up
Install *Prometheus* for Linux via https://prometheus.io.

**Note**: Currently used Prometheus version is 1.7, since version 2.0 has some
breaking / incompatible changes and the config must be updated accordingly.

Install *[Grafana]*(https://grafana.com/) and follow
[the instructions](http://docs.grafana.org/installation/debian/) to run the
server.

### Start Prometheus server as a systemd daemon
In order to run *Prometheus* at system start up, it can be set as a systemd
daemon:
```bash
sudo systemctl enable /path/to/your/prometheus-server.service
```
This will create a soft link in `/etc/systemd/system/`. Reload all services:
```bash
sudo systemctl daemon-reload
```
and start *prometheus*:
```bash
sudo systemctl start prometheus-server.service
```
You can check the status of the service by executing
```bash
sudo systemctl status prometheus-server.service
```
You can stop the service by executing
```bash
sudo systemctl stop prometheus-server.service
```
You can reload the service by executing
```bash
sudo systemctl reload prometheus-server.service
```
