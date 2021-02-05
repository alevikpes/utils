ARG odoo_version=None
# the next line must be first in case of manual creation
#FROM odoo:11@<image digest here>
FROM odoo$odoo_version
MAINTAINER name

USER root
# Install tools required for project
# Run `docker build --no-cache .` to update dependencies
RUN set -ex; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
        apt-utils \
        ca-certificates \
        curl \
        fontconfig \
        fontconfig-config \
        fonts-dejavu-core \
        gcc \
        gnupg \
        libc6 \
        libfontconfig1 \
        libfontenc1 \
        libfreetype6 \
        libjpeg-dev \
        libjpeg62-turbo \
        libldap2-dev \
        libpng16-16 \
        libpq-dev \
        libpython-dev \
        libsasl2-dev \
        libssl-dev \
        libssl1.1 \
        libstdc++6 \
        libtiff5-dev \
        libx11-6 \
        libxext6 \
        libxfont1 \
        libxml2-dev \
        libxrender1 \
        libxslt1-dev \
        node-clean-css \
        node-less \
        python3-dev \
        python3-libxml2 \
        python3-pip \
        python3-renderpm \
        python3-setuptools \
        wget \
        x11-common \
        xfonts-75dpi \
        xfonts-base \
        xfonts-encodings \
        xfonts-utils \
        xz-utils \
        zlib1g \
        zlib1g-dev; \
    curl -o wkhtmltox.tar.xz \
        -SL https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz; \
    echo '3f923f425d345940089e44c1466f6408b9619562 wkhtmltox.tar.xz' \
        | sha1sum -c -; \
    tar xvf wkhtmltox.tar.xz; \
    cp wkhtmltox/lib/* /usr/local/lib/; \
    cp wkhtmltox/bin/* /usr/local/bin/; \
    cp -r wkhtmltox/share/man/man1 /usr/local/share/man/; \
    ln -s /usr/bin/python3.5 /usr/bin/python

# Install Postgres 9.5 client
RUN set -ex; \
    echo 'deb http://apt.postgresql.org/pub/repos/apt/ xenial-pgdg main' 9.5 \
        > /etc/apt/sources.list.d/pgdg.list; \
    # getting the key in this way does not work correctly with docker,
    # since it requires stdin to be open
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc \
        | apt-key add -; \
    apt-get update; \
    apt-get install -y postgresql-client-9.5 pgadmin3

# Copy modified entrypoint script
# This file contains all required configuration, modify it if needed
COPY ./entrypoint.sh /
