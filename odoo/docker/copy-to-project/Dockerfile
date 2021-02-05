ARG custom_image=None
FROM $custom_image
MAINTAINER company

USER root

# Most of the required packages have been installed in the `custom-odoo` image
# Only install tools required for your project
# Run `docker build --no-cache .` to update dependencies
RUN apt-get update \
    && apt-get upgrade -y --no-install-recommends \
    && pip3 install pip --upgrade --force-reinstall \
    && mkdir /app

# TODO: make a script to collect all requirements.txt files
# and install from them with pip
#COPY ./custom-addons/requirements.txt /app/custom-addons
#RUN pip3 install -r /app/custom-addons/requirements.txt --ignore-installed

COPY ./odoo.conf /etc/odoo
COPY ./enterprise /app/enterprise

# change user
USER odoo
ENTRYPOINT ["/entrypoint.sh"]
# This command will be executed when a container starts.
CMD ["odoo", "-c", "/etc/odoo/odoo.conf"]
