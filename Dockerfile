# Zero-dependency demo image: the demo server uses only the stdlib.
FROM python:3.12-slim
WORKDIR /srv/recon-agent
COPY app ./app
COPY demo_server.py ./
# PaaS hosts inject $PORT; demo_server.py binds 0.0.0.0 when it is set.
CMD ["python3", "demo_server.py"]
