FROM python:3.9-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Instala o uv
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /app

COPY pyproject.toml .

RUN uv venv
RUN uv pip compile pyproject.toml > requirements.txt
RUN uv pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["uv", "run", "python", "app.py"]
