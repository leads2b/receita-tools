# Publishing

`receita-tools` is packaged with a PEP 621 `pyproject.toml` and published two ways on
every release: as a wheel/sdist to **PyPI** and as a container image to **Docker Hub**.
Both happen automatically from GitHub Actions when a `v*` tag is pushed
(`.github/workflows/release.yml`).

## Cutting a release

1. Bump the version in `receita/__init__.py` (single source of truth — `pyproject.toml`
   reads it via `[tool.setuptools.dynamic]`).
2. Add a matching section to `CHANGELOG.md`.
3. Commit, then tag and push:

   ```sh
   git tag v3.0.0
   git push origin v3.0.0
   ```

The `release.yml` workflow then runs the test suite, builds the package, publishes to PyPI
via Trusted Publishing, and builds + pushes the Docker image tagged `3.0.0` and `latest`.

## Building locally (optional sanity check)

```sh
python -m pip install build twine
python -m build            # writes sdist + wheel to dist/
twine check dist/*         # validates metadata + README rendering
```

## One-time setup (already done, documented for reference)

### PyPI — Trusted Publishing (OIDC, no API tokens)

On <https://pypi.org> → the `receita-tools` project → *Publishing*, add a **GitHub
publisher** (a "pending publisher" if the project does not exist yet):

- Owner: `leads2b`
- Repository: `receita-tools`
- Workflow: `release.yml`
- Environment: `pypi`

Then, in the GitHub repo, create an Environment named `pypi` (Settings → Environments). No
secrets are needed — the workflow authenticates with a short-lived OIDC token
(`permissions: id-token: write`).

### Docker Hub

- Create the `leads2b/receita-tools` repository on Docker Hub.
- Create a Docker Hub access token and add two GitHub Actions secrets (Settings → Secrets
  and variables → Actions):
  - `DOCKERHUB_USERNAME`
  - `DOCKERHUB_TOKEN`

## Why this layout

- **`pyproject.toml` (PEP 621)** is the modern standard; `setup.py`/`setup.cfg` are no
  longer needed. The version stays in `receita/__init__.py` and is read without importing
  the package.
- **Trusted Publishing** removes long-lived PyPI API tokens from the repo entirely.
- **`python -m build`** produces both an sdist and a wheel using the declared build backend.
