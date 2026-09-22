FROM python:3.12-slim AS builder

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 PIP_NO_CACHE_DIR=1
WORKDIR /build
RUN python -m venv /opt/venv
COPY requirements.lock .
RUN /opt/venv/bin/pip install --no-cache-dir --no-compile -r requirements.lock \
    && rm -rf /opt/venv/lib/python3.12/site-packages/pip* \
              /opt/venv/lib/python3.12/site-packages/setuptools* \
              /opt/venv/bin/pip*

FROM python:3.12-slim AS runtime

ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MUWAJJIH_ENVIRONMENT=production \
    MUWAJJIH_MODEL_PATH=/app/src/muwajjih/adapters/model/artifacts/classifier.joblib \
    MUWAJJIH_LOG_LEVEL=INFO
WORKDIR /app
RUN addgroup --system app && adduser --system --ingroup app --uid 10001 app
COPY --from=builder /opt/venv /opt/venv
COPY --chown=app:app src ./src
USER app
EXPOSE 8000
HEALTHCHECK --interval=10s --timeout=3s --start-period=20s --retries=3 CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/ready', timeout=2)"]
CMD ["uvicorn", "muwajjih.api.app:app", "--app-dir", "src", "--host", "0.0.0.0", "--port", "8000"]
