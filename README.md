# Kubernetes Deploy: FastAPI Backend

Small FastAPI backend packaged for Docker and deployable to Kubernetes using Helm.

## Quick Start (local)
- Install Python 3.11+, Docker, and (for K8s) kubectl + Helm.
- Install deps: `python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
- Run locally: `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
- Visit `http://localhost:8000/docs` for the interactive API (endpoints: `/`, `/healthz`, `POST /items`).

## Build and Run with Docker
```bash
# From repo root
docker build -t fastapi-app:latest .
docker run --rm -p 8000:8000 fastapi-app:latest
```
Browse to `http://localhost:8000/docs` and try `POST /items`.

## Deploy to Docker Desktop Kubernetes (no registry push)
Docker Desktop shares its image cache with the Kubernetes cluster, so you can deploy the local image directly.
1) Make sure Kubernetes is enabled in Docker Desktop and that your context points to it:
```bash
kubectl config use-context docker-desktop
kubectl cluster-info
```
2) Build the image locally (tag matches the chart defaults):
```bash
docker build -t fastapi-app:latest .
```
3) Install/upgrade with Helm (namespace defaults to `default`):
```bash
helm upgrade --install fastapi helm/fastapi \
  --set image.repository=fastapi-app \
  --set image.tag=latest
```
4) Reach the service via port-forward:
```bash
kubectl --namespace default port-forward svc/fastapi-fastapi-app 8000:8000
```
Then open `http://localhost:8000/docs` and try the API.

## Deploy to other Kubernetes clusters (push to a registry)
1) Build and push to your registry (Docker Hub/GHCR/etc.):
```bash
docker build -t YOUR_REPO/fastapi-app:0.1.0 .
docker push YOUR_REPO/fastapi-app:0.1.0
```
2) Install/upgrade the release:
```bash
helm upgrade --install fastapi helm/fastapi \
  --set image.repository=YOUR_REPO/fastapi-app \
  --set image.tag=0.1.0
```
3) Port-forward or expose via Ingress/LoadBalancer as needed:
```bash
kubectl port-forward svc/fastapi-app 8000:8000
```

### Optional tweaks
- Enable an Ingress (set host accordingly):
  ```bash
  helm upgrade --install fastapi helm/fastapi \
    --set image.repository=YOUR_REPO/fastapi-app \
    --set ingress.enabled=true \
    --set ingress.hosts[0].host=fastapi.local
  ```
- Adjust replicas/resources/autoscaling in `helm/fastapi/values.yaml`.

## Project Layout
- `app/main.py` – FastAPI app (health + echo endpoint).
- `requirements.txt` – Python dependencies.
- `Dockerfile` / `.dockerignore` – Container build context.
- `helm/fastapi` – Helm chart (deployment, service, optional ingress/HPA).
