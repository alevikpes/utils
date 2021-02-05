#!/usr/bin/env bash

sudo locale-gen

sudo apt-get update

# Use python 3.5 and above, on stretch we have 3.5.3: https://www.odoo.com/documentation/11.0/setup/install.html
# Use debian packages especially for node-less and node-clean-css.
# There was python-xlrd and python-psycopg2 in the list below.
# It was installed, but in odoo/requirements.txt we need to install a
# newer version. There was a problem of uninstalling them to install
# the newer version. So removing these packages from here helped to
# solve the problem. Removed also python-werkzeug, since it will
# be installed with the good version from odoo/requirements.txt
sudo apt-get install -y \
    curl \
    fontconfig \
    fontconfig-config \
    fonts-dejavu-core \
    gcc \
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
    postgresql \
    python3-dev \
    python3-libxml2 \
    python3-pip \
    x11-common \
    xfonts-75dpi \
    xfonts-base \
    xfonts-encodings \
    xfonts-utils \
    zlib1g \
    zlib1g-dev

# from nightly what is missing in requirements.txt
#sudo apt-get install python3-dateutil, python3-pil, python3-serial, python3-tz, python3-usb, python3-yaml, adduser, lsb-base, python3-suds -y

# from dockerfile of odoo repo odoo 11
#sudo apt-get install python3-setuptools python3-renderpm -y

#from odoo11 cookbook
#sudo apt-get install libevent-dev node-clean-css xz-utils 


# The following from the docker file:
# https://github.com/odoo/docker/blob/master/11.0/Dockerfile.
# It is compatible with odoo 11, debian stretch. 
curl -o wkhtmltox.tar.xz -SL \
        https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
echo '3f923f425d345940089e44c1466f6408b9619562 wkhtmltox.tar.xz' | sha1sum -c -
tar xvf wkhtmltox.tar.xz
cp wkhtmltox/lib/* /usr/local/lib/
cp wkhtmltox/bin/* /usr/local/bin/
cp -r wkhtmltox/share/man/man1 /usr/local/share/man/

# insert user vagrant under postgres
sudo -u postgres createuser --createdb --username postgres \
    --no-createrole --no-superuser vagrant

# Upgrade pip to latest version
sudo pip3 install --upgrade --force-reinstall pip

#install pip modules
sudo pip3 install -r /app/odoo/requirements.txt
sudo pip3 install -r /app/custom-addons/requirements.txt
