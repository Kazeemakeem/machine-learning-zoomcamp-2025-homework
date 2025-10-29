FROM agrigorev/zoomcamp-model:2025

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# ENV PATH="/code/.venv/bin:$PATH"

COPY ".python-version" "pyproject.toml" "uv.lock" "./"

RUN uv sync --locked

COPY "predict.py" "marketing.py" "./"

EXPOSE 9696

ENTRYPOINT ["uv", "run", "uvicorn", "predict:app", "--host", "0.0.0.0", "--port", "9696"]
