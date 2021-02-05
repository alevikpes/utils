#!/bin/bash
# https://github.com/odoo/docker/blob/d0360678214b8f70970a2369a5a6b37981ab2c45/11.0/entrypoint.sh

# use custom django settings file, when running django apps
echo "$@ ${APP_NAME}"
exec "$@"
# --settings="${APP_NAME}.settings"
