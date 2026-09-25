FROM python:3.13-slim-bookworm

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY pyproject.toml uv.lock ./
COPY README.md ./
COPY src ./src

RUN pip install --no-cache-dir uv \
    && uv sync --frozen --no-dev

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

CMD ["uv", "run", "--no-dev", "uvicorn", "auth.main:app", "--host", "0.0.0.0", "--port", "8000"]
