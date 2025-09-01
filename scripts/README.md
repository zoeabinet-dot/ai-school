This folder contains small helper scripts for local maintenance.

generate_secret.py
- Purpose: Print a secure Django SECRET_KEY suitable for production.
- Usage:

```bash
python scripts/generate_secret.py
```

Copy the output and store it in your environment (e.g., `.env`) or as a GitHub Secret named `SECRET_KEY`.

gh_set_secret.sh
- Purpose: Convenience wrapper to set GitHub repository secrets via the `gh` CLI.
- Usage (locally):

```bash
./scripts/gh_set_secret.sh SECRET_KEY "$(python scripts/generate_secret.py)"
```

Note: `gh` must be installed and authenticated (`gh auth login`) and the user must have repo admin permissions to set secrets.

Run local stack
--------------

1. Copy `.env.compose.example` to `.env.compose` and fill in `SECRET_KEY` (generate with `python scripts/generate_secret.py`).
2. Run the local stack:

```bash
./scripts/run_local.sh
# iterative dev (default uses `web-dev` which mounts source code for live edits)
./scripts/run_local.sh --with-nginx
```

This starts a minimal set of services (web, db, redis, nginx) via docker-compose. Stop with Ctrl-C.
