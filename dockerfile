FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
COPY src ./src

RUN pip install --no-cache-dir .


ENV PYTHONPATH=/app/src
ENV WORKSPACE_ROOT=/Users/priyanshu/Desktop/agenticWorkflow
ENV LOG_LEVEL=INFO

EXPOSE 8000

CMD ["python", "-m", "filesystem_mcp.server"]