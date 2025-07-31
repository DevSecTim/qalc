# syntax=docker/dockerfile:1
FROM python:3.13
COPY . /app
WORKDIR /app
RUN pip install uv && uv pip install --system --no-cache-dir .
ENTRYPOINT ["python", "-m", "qalc.mcp.main"]
