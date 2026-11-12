FROM python:3.14

WORKDIR /app/

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

COPY app/main.py ./main.py

CMD [ "uv", "run", "fastapi", "run", "main.py" ]