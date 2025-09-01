.PHONY: help build-frontend generate-secret lint test deploy

help:
	@echo "Targets:"
	@echo "  build-frontend   - build the frontend production bundle"
	@echo "  generate-secret  - print a secure Django SECRET_KEY"
	@echo "  lint             - run frontend type-check and lint"
	@echo "  test             - run frontend tests"
	@echo "  deploy           - run example deploy script (local only)"

build-frontend:
	cd frontend && npm ci && npm run build

generate-secret:
	python scripts/generate_secret.py

lint:
	cd frontend && npm run type-check && npm run lint

test:
	cd frontend && npm test -- --watchAll=false --passWithNoTests

deploy:
	./scripts/deploy.sh

run-local:
	@echo "Run local minimal stack using docker-compose (requires .env.compose)"
	./scripts/run_local.sh
