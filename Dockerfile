FROM python:3.12-slim

LABEL org.opencontainers.image.title="receita-tools" \
      org.opencontainers.image.description="Tools to manipulate Receita's company data." \
      org.opencontainers.image.source="https://github.com/leads2b/receita-tools" \
      org.opencontainers.image.licenses="MIT"

WORKDIR /app
COPY . /app/
RUN pip install --no-cache-dir .

# Run as a non-root user and keep data in a mounted working directory.
RUN useradd --create-home --uid 1000 receita
USER receita
WORKDIR /data

ENTRYPOINT ["receita"]
