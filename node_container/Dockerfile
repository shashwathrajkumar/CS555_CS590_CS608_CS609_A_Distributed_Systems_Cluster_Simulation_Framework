FROM python:3.10-slim

WORKDIR /app

COPY node_script.py .

RUN pip install requests

CMD ["python", "node_script.py"]
