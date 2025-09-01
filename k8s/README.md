Kubernetes deployment template

This folder contains a minimal `deployment.yaml` that you should adapt before use.

Placeholders to replace:
- `REPLACE_WITH_IMAGE`: the container image to deploy, e.g. `docker.io/yourorg/ai-school:latest`
- `REPLACE_WITH_DATABASE_URL`: the DATABASE_URL environment variable value (or use a Kubernetes Secret)

Secrets:
- Create a Kubernetes Secret named `ai-school-secrets` containing `SECRET_KEY` and other sensitive values:

```bash
kubectl create secret generic ai-school-secrets --from-literal=SECRET_KEY='<your-secret-key>'
```

Usage (example):

```bash
kubectl apply -f k8s/deployment.yaml
kubectl rollout status deployment/ai-school-web
```

This is a template; adapt replicas, resources, probes, and additional env vars as needed.
