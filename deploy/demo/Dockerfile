FROM node:24-bookworm-slim AS web

WORKDIR /build
ENV NEXT_TELEMETRY_DISABLED=1 \
    NEXT_PUBLIC_LAYERWISE_SAME_ORIGIN=1
RUN corepack enable
COPY frontend/package.json frontend/pnpm-lock.yaml frontend/pnpm-workspace.yaml ./
RUN pnpm install --frozen-lockfile
COPY frontend/ ./
RUN pnpm build

FROM ghcr.io/astral-sh/uv:0.12.18 AS uv
FROM python:3.13-slim-bookworm AS api

COPY --from=uv /uv /bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
COPY backend/pyproject.toml backend/
RUN uv sync --locked --package layerwise-bokeh --extra api --no-dev --no-install-project
COPY backend/src/ backend/src/
RUN uv sync --locked --package layerwise-bokeh --extra api --no-dev --no-editable
# The regular Linux torch wheels in uv.lock pull in CUDA. Use the CPU build of
# the same release, without changing the workspace's install or lockfile.
RUN uv pip install --python /app/.venv/bin/python \
    --extra-index-url https://download.pytorch.org/whl/cpu 'torch==2.11.0+cpu'

FROM python:3.13-slim-bookworm

RUN sed -i 's|http://deb.debian.org|https://deb.debian.org|g' /etc/apt/sources.list.d/debian.sources \
    && apt-get update \
    && apt-get install -y --no-install-recommends libstdc++6 nginx tini \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --uid 1000 app \
    && mkdir /data \
    && chown app:app /data
COPY --from=web /usr/local/bin/node /usr/local/bin/node
COPY --from=web --chown=1000:1000 /build/.next/standalone /app/web
COPY --from=web /build/.next/static /app/web/.next/static
COPY --from=api /app/.venv /app/.venv
COPY nginx.conf start.sh demo_api.py /app/
COPY backend/data/library_demo/ /app/library/

# Return large frame buffers to the OS between generations.
ENV MALLOC_MMAP_THRESHOLD_=131072 \
    MALLOC_ARENA_MAX=2
ENV HOME=/home/app \
    NODE_ENV=production \
    NEXT_TELEMETRY_DISABLED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    LAYERWISE_BOKEH_DATA_ROOT=/data \
    LAYERWISE_BOKEH_LIBRARY=/app/library \
    LAYERWISE_BOKEH_LAYERED_DEVICE=cpu \
    LAYERWISE_BOKEH_LAYERED_CHUNK=1 \
    OMP_NUM_THREADS=2 \
    MKL_NUM_THREADS=2 \
    OPENBLAS_NUM_THREADS=2 \
    PORT=7860

WORKDIR /app
USER 1000:1000
EXPOSE 7860
ENTRYPOINT ["/usr/bin/tini", "--", "/bin/bash", "/app/start.sh"]
