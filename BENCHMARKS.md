# Benchmarks

All measurements below are from local runs using synthetic training data.

## Model

- Records: 12,000
- Accuracy: 1.0000
- Macro F1: 1.0000

These model scores are from synthetic data and are not a claim of real-world government performance.

## Tests

Latest local verification:

- 41 passed
- Branch coverage: 88.10%
- Test time: 5.15 s
- Required coverage gate: 80%

## API

Verified:

- `POST /v1/predict`
- `GET /health`
- `GET /ready`
- unified `422` validation response
- trace ID propagation

## Docker

Initial image:

- Build time: 180.1 s
- Size: 789.5 MB

Optimized image:

- Size: 442.13 MB
- Container startup: passed
- Docker Compose: healthy
- Smoke test: passed

The optimized image is below the 500 MB capstone limit.

## CI/CD

The pipeline verifies linting, type-checking, coverage, secret scanning, Docker smoke testing, and GHCR publishing on `main`.
