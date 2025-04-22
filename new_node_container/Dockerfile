# Dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY new_node.py .

RUN pip install requests

ENTRYPOINT ["python", "new_node.py"]
