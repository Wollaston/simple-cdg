FROM ghcr.io/astral-sh/uv:trixie
WORKDIR /app

COPY . .

RUN uv sync --locked

EXPOSE 8000

CMD ["uv", "run", "fastapi", "run", "--host=0.0.0.0", "--port=8000"]
