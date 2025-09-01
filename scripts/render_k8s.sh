#!/usr/bin/env bash
set -euo pipefail

# Renders k8s/deployment.yaml by replacing placeholders and applies it using kubectl.
# Requires KUBECONFIG to be set in the environment (the workflow writes the secret to a file).

if [ -z "${DOCKER_IMAGE:-}" ]; then
  echo "DOCKER_IMAGE must be provided"
  exit 1
fi

TMP_DEPLOY=./k8s/deployment.rendered.yaml
cp k8s/deployment.yaml "$TMP_DEPLOY"

echo "Replacing image placeholder with $DOCKER_IMAGE"
sed -i "s|REPLACE_WITH_IMAGE|$DOCKER_IMAGE|g" "$TMP_DEPLOY"

if [ -n "${DATABASE_URL:-}" ]; then
  sed -i "s|REPLACE_WITH_DATABASE_URL|$DATABASE_URL|g" "$TMP_DEPLOY"
fi

kubectl apply -f "$TMP_DEPLOY"
echo "Applied $TMP_DEPLOY"
