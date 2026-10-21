# Software Observatory – Server Configuration

This repository contains the configuration files needed to deploy the **Software Observatory** backend, that is, the services the front-end needs in order to work. 
It provides a reproducible setup using Docker Compose, including:

- **Nginx** – reverse proxy that routes traffic to the APIs.
- **Observatory API** – main backend service of the Observatory.
- **GitHub Metadata API** – metadata extraction service for FAIRsoft.


This repository also contains:  

- **Licenses Mapping API** – license mapping service. It is not needed by the front-end; it is used by the data pipeline and can be used by other clients.

This repository DOES NOT contain the data pipeline of the software observatory. 

---

## Repository Structure

```
 docker-compose.yml          # Compose file defining all services
 nginx.conf                  # Nginx reverse proxy configuration
 github-metadata-api-variables/
 ├── check_installations_extractor.py   # GitHub App diagnostic scripts (see below)
 ├── check_installations_updater.py
 ├── check_total_repos_extractor.py
 └── check_total_repos_updater.py
```

`nginx.conf` routes:
- `/api/` → Observatory API (`observatory-api:3500`)
- `/licenses-mapping/` → Licenses Mapping API (`licenses-mapping:8000`)
- `/github-metadata-api/` → GitHub Metadata API (`github-metadata-api:8080`)

## Production directories (not in Git)

The services need some directories that are **not tracked in this repository** because they contain secrets (`*.pem`, `*.ini` and `*.env` are gitignored). They must be created next to `docker-compose.yml` on the server before starting the stack:

```
 github-metadata-api-variables/      # mounted at /app/variables in github-metadata-api
 ├── .env                            # environment variables for the GitHub Metadata API
 ├── metadata-extractor-for-fairsoft.<date>.private-key.pem
 └── metadata-updater-for-fairsoft.<date>.private-key.pem
 licenses-mapping-env/
 └── .env                            # env_file for licenses-mapping
 observatory-api-variables/          # mounted at /api-variables in observatory-api
 ├── config_db.ini                   # database connection config
 └── dev_config_db.ini               # database connection config (dev database)
 observatory-dev-variables/          # same layout as observatory-api-variables, for a dev instance
 ├── config_db.ini
 └── dev_config_db.ini
```

- `github-metadata-api-variables/` – a `.env` file and the private keys of the two GitHub Apps used by the metadata extractor and updater. The directory already exists in the repo (it holds the diagnostic scripts); only these secret files need to be added.
- `licenses-mapping-env/.env` – environment variables for the Licenses Mapping API.
- `observatory-api-variables/` – database configuration for the Observatory API.
- `observatory-dev-variables/` – database configuration for a development instance of the Observatory API. It is not referenced by the current `docker-compose.yml`.

For the details of each variable (which keys the `.env` and `.ini` files must contain and what they mean), see the repository of the corresponding service: 

- Observatory API – https://github.com/inab/observatory-api
- GitHub Metadata API – https://github.com/inab/github-metadata-api
- Licenses Mapping API – https://github.com/inab/license-mapping-api

In addition, the `licenses-mapping` service mounts the host's `/home/user/.ssh/` at `/root/.ssh/`, so the SSH keys it needs must be present there.

## GitHub App diagnostic scripts

`github-metadata-api-variables/` contains two scripts for each of the two GitHub Apps used by the GitHub Metadata API: the metadata extractor (App ID `983558`) and the metadata updater (App ID `983619`). Each script signs a JWT with its app's private key and queries the GitHub API:

- `check_installations_<app>.py` – lists the app's installations (installation ID and account).
- `check_total_repos_<app>.py` – for each installation, creates an installation token and counts the repositories the app can access, then prints the total across all installations.

The scripts load the private key from a path relative to the current directory, so run them from inside the directory:

```bash
cd github-metadata-api-variables
pip install "pyjwt[crypto]" requests
python check_total_repos_extractor.py
```

If a private key is rotated, update `PRIVATE_KEY_PATH` in the matching scripts.

## Requirements

- [Docker](https://docs.docker.com/get-docker/) ≥ 20.10  
- [Docker Compose](https://docs.docker.com/compose/) plugin  

## Usage

Clone the repository, add the production directories described above, and bring up the stack:

```bash
git clone <this-repo-url>
docker compose up -d
```

The Docker network MTU defaults to `1442`; override it with the `MTU` environment variable if needed.

## Access points
- Observatory API – http://localhost:8080/api/
- Licenses Mapping API – http://localhost:8080/licenses-mapping/
- GitHub Metadata API – http://localhost:8080/github-metadata-api/
