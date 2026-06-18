FROM python:3.10-slim
WORKDIR /app
COPY pyproject.toml poetry.lock* /app/
RUN pip install --upgrade pip && pip install fastapi uvicorn "python-multipart" "pydantic" rapidfuzz requests
COPY api /app/api
ENV PYTHONPATH=/app
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
