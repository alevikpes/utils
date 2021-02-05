#!/bin/sh
# wait-for-postgres.sh

set -e

until PGCONNECT_TIMEOUT=5 PGPASSWORD=$DATABASE_PASSWORD psql -h "$DATABASE_HOST" -U "dbuser" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
