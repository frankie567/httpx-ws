# https://just.systems

install:
    uv sync --locked
    uv run --locked pre-commit install

lint:
    uv run --locked ruff format .
    uv run --locked ruff check --fix .
    uv run --locked ty check

lint-check:
    uv run --locked ruff format --check .
    uv run --locked ruff check .
    uv run --locked ty check

test:
    uv run --locked pytest

test-cov-xml:
    uv run --locked pytest --cov-report=xml

docs-serve:
    uv run --locked zensical serve

docs-build:
    uv run --locked zensical build --strict

build:
    uv sync --locked
    uv build --no-build-isolation

version bump:
    #!/usr/bin/env bash
    set -euo pipefail
    if [[ -n "$(git status --porcelain)" ]]; then
        echo "Commit or stash changes before preparing a release." >&2
        exit 1
    fi
    uv sync --locked
    uv run --no-sync hatchling version {{quote(bump)}}
    release_version="$(uv run --no-sync hatchling version)"
    uv run --no-sync keepachangelog release "$release_version"
    test -n "$(uv run --no-sync keepachangelog show "$release_version")"
    uv lock
    git add httpx_ws/__init__.py CHANGELOG.md uv.lock
    git commit -S -e -m "release: Bump version to $release_version"
    git tag -s "v$release_version" -m "Release $release_version"

release-notes version:
    @uv run --locked keepachangelog show {{quote(version)}}
