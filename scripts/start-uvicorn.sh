#! /usr/bin/env sh
set -e

if [ -f /app/app/main.py ]; then
    DEFAULT_MODULE_NAME=app.main
elif [ -f /app/main.py ]; then
    DEFAULT_MODULE_NAME=main
fi
MODULE_NAME=${MODULE_NAME:-$DEFAULT_MODULE_NAME}
APPLICATION_NAME=${APPLICATION_NAME:-app}
export APP_MODULE=${APP_MODULE:-"$MODULE_NAME:$APPLICATION_NAME"}

HOST=${API_HOST:-0.0.0.0}
PORT=${API_PORT:-8000}
LOG_LEVEL=${LOG_LEVEL:-info}

# If there's a prestart.sh script in the /app directory, run it before starting
PRE_START_PATH=${PRE_START_PATH:-"scripts/prestart.sh"}
echo "Checking for script in $PRE_START_PATH"
if [ -f "$PRE_START_PATH" ] ; then
    echo "Running script $PRE_START_PATH"
    . "$PRE_START_PATH"
else
    echo "There is no script $PRE_START_PATH"
fi

IS_USE_NGINX=${1:-false}

if [ "$IS_USE_NGINX" = "true" ]; then
    echo "Starting Nginx..."
    nginx

    echo "Started Nginx... ##################################"
fi

echo "Starting Uvicorn..."

ENVIRONMENT=${ENVIRONMENT:-local}

if [ "$ENVIRONMENT" = "local" ]; then
    # Start Uvicorn with live reload
    ARGS="--reload"
else
    ARGS="--workers=4"
fi

exec uvicorn --host $HOST --port $PORT --log-level $LOG_LEVEL "$APP_MODULE" --forwarded-allow-ips '*' --proxy-headers --timeout-keep-alive 65 "$ARGS"
