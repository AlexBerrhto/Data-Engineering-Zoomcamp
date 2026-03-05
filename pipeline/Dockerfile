FROM python:3.13.10-slim

# Copy uv binary
COPY --from=ghcr.io/astral-sh/uv:0.6.6 /uv /bin/ 

# Set working directory
WORKDIR /app

# Optimization environment variables
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Copy dependency files
COPY pyproject.toml .python-version uv.loc[k] ./

# Install dependencies
RUN uv sync --frozen

# Copy the actual application files
COPY onlinestore.py .

ENTRYPOINT ["python", "onlinestore.py"]