# Development

This project has two toolchains working side by side:

- **Python** runs the Django app itself.
- **Node** (via yarn/gulp) compiles the frontend CSS: a vendored copy of the Canvas template's Bootstrap-based SCSS (`core/static/scss/`) into plain CSS (`core/static/css/style.css`).

In production (Render, via the `Dockerfile`), the Node toolchain only runs once at image build time to produce the compiled CSS; the running container only needs Python. Locally, you'll want both running while you work — see [Running everything together](#running-everything-together).

## Prerequisites

### Python

- Python 3.14 (see `requires-python` in `pyproject.toml`).
- [uv](https://docs.astral.sh/uv/) to manage the virtualenv and dependencies (not pip/poetry):
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

### Node, nvm, yarn

The frontend build needs Node and [yarn](https://yarnpkg.com/) 4.0.2 (pinned in `package.json`'s `packageManager` field and used in the `Dockerfile`'s build stage).

1. Install [nvm](https://github.com/nvm-sh/nvm) (Node Version Manager):
   ```bash
   curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
   ```
   Restart your shell (or re-source your `~/.bashrc`/`~/.zshrc`) afterwards.
2. Install and use the latest Node LTS:
   ```bash
   nvm install --lts
   nvm use --lts
   ```
   The Canvas template (vendored into `core/static/scss/`) requires **Node ≥ 20.19.0** to build from SCSS (`canvas/UPGRADE.md` §1.5, §5; also pinned as `canvas/package.json`'s `engines.node`) — `nvm install --lts` satisfies this comfortably (the current Node LTS is **v22.16.0**).
3. Enable [corepack](https://nodejs.org/api/corepack.html) (ships with Node, manages yarn/pnpm versions for you) and activate the pinned yarn version:
   ```bash
   corepack enable
   corepack prepare yarn@4.17.1 --activate
   ```
   You shouldn't need to `yarn install` yarn itself or install it via npm — corepack handles invoking the right yarn version automatically based on `package.json`.

### Docker (for local Postgres)

The app needs Postgres. The easiest local option is running it in Docker — see [Database](#database) below.

## Setup

```bash
# Python deps
uv sync

# Node deps (gulp, sass, autoprefixer, etc. — see package.json devDependencies)
yarn install

# Environment variables
cp .env-example .env
# then edit .env — see .env-example for what each variable means
```

### Database

Start a local Postgres container:

```bash
docker run --name zink -e POSTGRES_PASSWORD=zink -e POSTGRES_USER=zink -d -p 7777:5432 postgres
```

Match the `POSTGRES_*` values in `.env` to whatever you used above (the example command uses `zink`/`zink` on port `7777`).

Then run migrations:

```bash
uv run manage.py migrate
```

## The CSS build (gulp)

`core/static/scss/` is a vendored copy of the Canvas template's SCSS. It's compiled to plain CSS by [gulp](https://gulpjs.com/) tasks defined in `gulpfile.js`, driven through yarn scripts in `package.json`:

| yarn script | gulp task(s) | What it does |
|---|---|---|
| `yarn build:canvas-css` | `scsscompile` (= `compileSCSS` then `convertRTL`) | One-off build: compiles `core/static/scss/style.scss` → `core/static/css/style.css` (with sourcemaps and autoprefixer), then generates `style-rtl.css` from it via `gulp-rtlcss` for right-to-left locales. |
| `yarn watch:canvas-css` | `watch` | Watches `core/static/scss/**/*.scss` for changes and re-runs `compileSCSS` + `convertRTL` on each save. Use this while developing. |

Details on what `compileSCSS` does, in order:
1. Reads `core/static/scss/style.scss` with `gulp-sass` (backed by the `sass` package), silencing a specific list of Dart Sass deprecation warnings (see `silencedSassDeprecations` in `gulpfile.js` — these come from the vendored Canvas SCSS itself, not our code).
2. Concatenates the result into a single `style.css` via `gulp-concat`.
3. Runs it through `autoprefixer` (via `gulp-postcss`) to add vendor prefixes.
4. Writes `core/static/css/style.css` (plus a sourcemap) via `gulp.dest`.

`gulp-plumber` wraps each pipeline so a Sass syntax error doesn't crash the whole watcher — it logs the error and keeps watching.

There's also a `cssminify` gulp task (minifies `style.css` into `style.min.css` via `gulp-clean-css`) that exists in `gulpfile.js` but isn't wired into either yarn script or the Docker build — it's unused currently.

Note: `core/static/css/style.css` (and `style-rtl.css`, `code.css`) are gitignored — they're build output, not committed source. You must run the CSS build at least once before the site will have working styles.

## Running everything together

```bash
./dev.sh
```

This runs `yarn watch:canvas-css` and `uv run manage.py runserver` concurrently in one terminal (see `dev.sh`), so SCSS edits are picked up live alongside the Django dev server. `Ctrl-C` stops both.

To run them separately instead (e.g. in two terminals):

```bash
uv run manage.py runserver
yarn watch:canvas-css
```

## Linting and formatting

Enforced both locally and as pre-commit hooks: `isort`, `black`, `flake8`.

```bash
uv run pre-commit run --all-files
```

## Tests

```bash
uv run manage.py test
```

Tests should be written/extended in each app's `tests.py` alongside the implementation (TDD) — see `CLAUDE.md` for the full workflow and commit conventions used in this repo.

## Deployment

The site deploys to [Render](https://render.com/) via the `Dockerfile`, which:
1. Builds the frontend assets in a Node stage (`corepack prepare yarn@4.17.1`, `yarn install --immutable`, `yarn build:canvas-css`).
2. Installs Python dependencies with `uv` in a separate stage.
3. Copies the compiled CSS from the Node stage into the final Python image.
4. On container start: runs `collectstatic`, `migrate`, loads the `blog` fixture, then serves via `uvicorn`.

See `deployment/` for how the deployed version/tag/timestamp is tracked and surfaced via the `version` template tag.
