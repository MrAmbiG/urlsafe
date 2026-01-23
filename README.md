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

### Install with Helm

#### From GitHub Packages (OCI Registry)
```bash
helm install urlsafe oci://ghcr.io/mrambig/charts/urlsafe --version 0.1.x
```

#### From Local Chart
```bash
helm install urlsafe k8s/urlsafe
```

### Customize Installation

Create a `values.yaml` file to override defaults:
```yaml
replicaCount: 5
image:
  tag: "sha256-abc123"
resources:
  limits:
    memory: "1Gi"
    cpu: "1000m"
```

Then install with custom values:
```bash
helm install urlsafe k8s/urlsafe -f values.yaml
```

### Upgrade Release
```bash
helm upgrade urlsafe k8s/urlsafe
```

### Uninstall
```bash
helm uninstall urlsafe
```

### EOF ###