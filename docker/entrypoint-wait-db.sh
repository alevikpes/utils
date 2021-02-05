#!/bin/sh

# waiting for the db container to start

echo "Preparing server"
if [ -n "$DATABASE_HOST" ]; then
    echo "Preparing server"
    sh script/wait-for-postgres.sh
    make migrate collectstatic
else
    if [ -n "$DEBUG" ]; then
        make migrate collectstatic
    fi
fi

echo "Starting Webserver"

echo "$@"

exec "$@"
