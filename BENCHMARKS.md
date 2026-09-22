# Benchmarks

All results are from local runs using synthetic training data

## Model

- Records: 12,000
- Accuracy: 1.0000
- Macro F1: 1.0000

## Tests

- 26 passed
- Branch coverage: 97.33%
- Test time: 1.25 s

## API

Verified:

- `POST /v1/predict`
- `GET /health`
- `GET /ready`
- `422` validation response

## Docker

Initial image:

- Build time: 180.1 s
- Size: 789.5 MB

Optimized image:

- Size: 442.13 MB
- Container startup: passed
- Docker Compose: healthy
- Smoke test: passed
