FROM python:3.12-slim
WORKDIR /app
COPY backend/pyproject.toml backend/pyproject.toml
COPY backend/satclip backend/satclip
RUN pip install --no-cache-dir "./backend[redis]"
COPY config config
ENV SATCLIP_CONFIG=/app/config/satclip.yaml PYTHONUNBUFFERED=1
WORKDIR /app/backend
EXPOSE 8000
CMD ["uvicorn", "satclip.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
