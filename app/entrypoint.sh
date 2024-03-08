#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

if [ "$REDIS_ENABLED" = "true" ]
then
    echo "Waiting for Redis..."

    while ! nc -z redis 6379; do
      sleep 0.1
    done

    echo "Redis started"
fi

gunicorn pong.wsgi:application --bind 0.0.0.0:8000 & daphne pong.asgi:application -b 0.0.0.0 -p 8001
exec "$@"
