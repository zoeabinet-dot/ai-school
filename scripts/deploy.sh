#!/usr/bin/env bash
# Example deploy script to run on your remote server after pulling the image.
# Customize these steps to match your setup.
set -euo pipefail

# Example variables (override on remote or via environment)
APP_DIR=${APP_DIR:-/srv/ai-school}
DOCKER_COMPOSE_FILE=${DOCKER_COMPOSE_FILE:-/srv/ai-school/docker-compose.yml}

# Stop old containers, pull new image, and bring up services
cd "$APP_DIR"
if [ -f "$DOCKER_COMPOSE_FILE" ]; then
  echo "Using docker-compose to update the stack..."
  docker-compose -f "$DOCKER_COMPOSE_FILE" pull web
  docker-compose -f "$DOCKER_COMPOSE_FILE" up -d --no-deps --build web
else
  echo "No docker-compose file found at $DOCKER_COMPOSE_FILE, please provide deploy steps."
  exit 1
fi

echo "Deploy completed."
