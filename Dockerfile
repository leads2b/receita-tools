FROM python:3.12-slim

LABEL org.opencontainers.image.title="receita-tools" \
      org.opencontainers.image.description="Tools to manipulate Receita's company data." \
      org.opencontainers.image.source="https://github.com/leads2b/receita-tools" \
      org.opencontainers.image.licenses="MIT"

WORKDIR /app

# Install the pinned dependency set first, then the package itself without
# re-resolving, so the image contents are reproducible.
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/
RUN pip install --no-cache-dir --no-deps .

# Run as a non-root user and keep data in a mounted working directory.
RUN useradd --create-home --uid 1000 receita
USER receita
WORKDIR /data

ENTRYPOINT ["receita"]
