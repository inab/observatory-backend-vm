# Software Observatory – Server Configuration

This repository contains the configuration files needed to deploy a working instance of the **Software Observatory** stack.  
It provides a reproducible setup using Docker Compose, including:

- **Nginx** – reverse proxy that routes traffic to APIs and Prefect.
- **Observatory API** – main backend service of the Observatory.
- **GitHub Metadata API** – metadata extraction service for FAIRsoft.
- **Prefect 2** – workflow orchestration (UI, API, and agent).

---

## Repository Structure

```
 docker-compose.yml          # Compose file defining all services
 nginx.conf                  # Nginx reverse proxy configuration
 github-metadata-api-variables/
 ├── metadata-extractor-for-fairsoft..private-key.pem
 └── metadata-updater-for-fairsoft..private-key.pem
 observatory-api-variables/
 └── config_db.ini           # Database connection config for observatory-api
 prefect_data/               # Prefect persistence (SQLite + state)
 ├── memo_store.toml
 └── prefect.db
```

### Notes on contents
- `github-metadata-api-variables/` – contains GitHub App private keys used by the metadata extractor and updater.
- `observatory-api-variables/` – configuration for the Observatory API (e.g., DB connection).
- `prefect_data/` – Prefect's local SQLite database and memo store.  
  This is persisted via a named volume or bind mount so flows and deployments survive restarts.
- `nginx.conf` – routes:
  - `/` → Prefect UI/API
  - `/api/` → Observatory API
  - `/github-metadata-api/` → GitHub Metadata API


## Requirements

- [Docker](https://docs.docker.com/get-docker/) ≥ 20.10  
- [Docker Compose](https://docs.docker.com/compose/) plugin  

## Usage

Clone the repository and bring up the stack:

```bash
git clone <this-repo-url>
docker compose up -d
```

## Access points
- Prefect UI – http://localhost:8080/
- Observatory API – http://localhost:8080/api/
- GitHub Metadata API – http://localhost:8080/github-metadata-api/
