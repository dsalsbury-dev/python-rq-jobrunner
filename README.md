# python-rq-jobrunner

This repository is a **planned demonstration project**. The items below describe the target system and what will be built (not what is already implemented).

## Project goal

A small, production-minded system that demonstrates:

- Python service design (FastAPI API surface)
- Distributed execution (Redis queue + separate worker)
- Postgres as the source of truth for job state/history
- Automation (Makefile + scripts to provision/deploy/scale)
- Reliability patterns (idempotency, retries, state machine)
- Observability (structured logs + correlation IDs)
- Security/config hygiene (Secrets/ConfigMaps, API key)

## MVP features (planned)

### API (FastAPI)

- `POST /v1/jobs` — create job (supports `Idempotency-Key`)
- `GET /v1/jobs/{id}` — status + timestamps + error/result
- `POST /v1/jobs/{id}/cancel` — cancel before it runs
- `GET /healthz` and `GET /readyz`

### Worker (RQ)

- Separate process/container running `rq worker`
- Executes job by `job_id`
- Updates DB job state:
  - `QUEUED -> RUNNING -> SUCCEEDED | FAILED | CANCELLED`
- Retries on failure (bounded; stores attempt count)

### Storage

- Postgres for canonical job history/status
- Redis for queue (RQ)

## Automation + deployment (planned)

- Local: `docker compose up` for `api + worker + redis + postgres`
- Minikube deploy:
  - `make k8s-up`
  - `make k8s-deploy`
  - `make k8s-scale-worker r=5`
  - `make smoke`
- Basic CI that runs lint + tests (optional Docker build)
