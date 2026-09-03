# zink (elevenbits.com)

Django site for elevenbits.com. Python backend, Tailwind/daisyUI frontend, deployed to Render via Docker.

## Stack

- Python 3.14, Django 6.1, managed with **uv** (not poetry/pip).
- Postgres (local dev via Docker), `whitenoise` serves static files in prod, `gunicorn`/`uvicorn` for serving.
- Tailwind CSS + daisyUI (theme currently `wireframe`, set in `core/templates/base.html`), built with **yarn** (yarn 3.4.1 via corepack).
- VCS: **jj** (Jujutsu), git backend. Use `jj`, not `git`, for day-to-day work in this repo.

## Commands

```bash
# Python deps / running
uv sync
uv run manage.py runserver
uv run manage.py test
uv run manage.py makemigrations / migrate

# CSS build (watch mode while developing)
yarn tailwindcss -i core/static/tailwind/input.css -o core/static/tailwind/output.css --watch

# Local Postgres
docker run --name zink -e POSTGRES_PASSWORD=zink -e POSTGRES_USER=zink -d -p 7777:5432 postgres

# Lint / format (also runs as pre-commit hooks)
uv run pre-commit run --all-files
```

`.env` holds local secrets (`SECRET_KEY`, DB settings) — see `.env-example`. Never commit `.env`.

## Workflow

- **jj, not git.** `jj describe -m "..."`, `jj new`, `jj log`. Don't reach for `git commit`/`git checkout` here.
- **Gitmoji commits.** Every `jj describe` / commit message starts with a gitmoji per https://gitmoji.dev/, one line: `<gitmoji> <description>` (e.g. `:sparkles: Add contact form`, `:bug: Fix footer link`). Match existing history style (`git log`/`jj log` show this pattern already).
- **Small commits.** One logical change per commit, not batched-up work.
- **TDD.** Write/extend a test in the relevant app's `tests.py` before or alongside the implementation, using Django's `TestCase`. Run `uv run manage.py test` before describing a commit.

## Architecture

- `elevenbits/` — Django project config: `settings.py`, root `urls.py` (includes `core.urls`), `asgi.py`/`wsgi.py`.
- `core/` — the main site app: static pages (index, about, cookies, and the page-in-progress: contact) live in `core/views.py` / `core/urls.py` / `core/templates/*.html`. `core/templatetags/` has the `version` tag used in `base.html`'s footer.
- `blog/` — the blog app, namespaced under `/blog/` (`app_name = "blog"`), own `models.py`/`views.py`/`urls.py`.
- `deployment/` — tracks deployment metadata (tag/version/timestamp/deployer) shown via the `version` templatetag; not a page, no URLs.
- `core/static/tailwind/` — Tailwind input/output CSS (`output.css` is gitignored, built via yarn, not committed).
- `canvas/` and `examples/` — **reference-only, gitignored, never edited or shipped.** `canvas/` is a vendored copy of the Canvas HTML template (docs: https://docs.canvastemplate.com/) used as a source of markup/visuals to port into Tailwind/daisyUI templates. `examples/` holds Wayback Machine dumps of the old elevenbits.com site (welcome/blog/contact pages) used for real copy/content reference. Treat both as design/content source material to read from, not as code to include or link to directly.

## Template conventions

- All page templates `{% extends "base.html" %}` and fill `{% block content %}` (see `core/templates/about.html` for the minimal pattern). `base.html` defines the `<head>`, the shared `{% block footer %}`, and loads `code.css` + the built `tailwind/output.css`.
- Styling: Tailwind utility classes + daisyUI components. When porting a Canvas template page, translate its markup/visual structure into Tailwind/daisyUI classes rather than including Canvas's own CSS/JS or copying its class names verbatim.
- One view per page in `core/views.py` (function-based, matches existing `index`/`about`/`cookies` pattern), registered in `core/urls.py`.

## Code style (enforced by pre-commit: isort, black, flake8)

- Double-quoted strings, 120-char line length.
- Type annotations expected on function args/returns (flake8-annotations), except `self`/`cls` and except in `views.py` and `tests.py`/`test_*` files (see `.flake8` `per-file-ignores`).
- No relative imports (`ban-relative-imports`).
