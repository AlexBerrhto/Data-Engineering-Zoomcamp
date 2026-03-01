FROM python:3.13.10-slim

# Copy uv binary
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH"

# Copy dependency files (using wildcard for uv.lock)
COPY pyproject.toml .python-version uv.loc[k] ./
RUN uv sync

# --- THE FIX ---
# Note the DOTS at the end of both lines
COPY onlinestore.py .
COPY online_retail_II.xlsx .
# ---------------

ENTRYPOINT ["python", "onlinestore.py"]