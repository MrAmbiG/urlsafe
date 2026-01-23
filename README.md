# urlsafe

Microservice to check and categorize URLs (Porn/Adult, Social, Gambling, Ad/Malware).

*note: This does not need constant update, as this is a wrapper around StevenBlack's hostfiles and gets updated every hour.*

## API

### Check URL
`GET /check?url=<url>`

Current Categories:
- `porn` (includes adult content)
- `social`
- `gambling`
- `admalware`

## Quick Start (Makefile)

- **Install**: `make install`
- **Run Locally**: `make run`
- **Run Tests**: `make test`
- **Docker**: `make docker-up`

## Development

1. Install `uv`: `curl -LsSf https://astral.sh/uv/install.sh | sh`
2. Run local server:
   ```bash
   make run
   # or
   uv run uvicorn app.main:app --reload
   ```

## Docker

```bash
docker-compose up --build
```

## Kubernetes

Deploy to K8s:
```bash
kubectl apply -f k8s/
```