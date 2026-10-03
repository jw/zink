
# ElevenBits

This is the elevenbits website project.

## Development

Both Python and Node are used.  Python runs the Django, the JavaScript is used to create the CSS files (a vendored copy of the Canvas template's Bootstrap-based SCSS, compiled with gulp/sass).
The system runs on a render.com Dockerfile environment.

### Database

Make sure to start the database on your local machine:

```bash
❯ docker run --name zink -e POSTGRES_PASSWORD=zink -e POSTGRES_USER=zink -d -p 7777:5432 postgres
```

Several environment variables need to be added to the `.env` file.  This `.env` file needs to remain private to you.  It should not be part of the repo!  See the `.env-example` for more information.

### CSS

Best to automatically generate the CSS via [yarn](https://yarnpkg.com/):

```bash
❯ yarn watch:canvas-css
```

Yarn 4.17.1 is used. First, make sure you're using the latest Node LTS (use [nvm](https://github.com/nvm-sh/nvm) to do so).  Best to install yarn via:

```bash
❯ corepack enable
❯ corepack prepare yarn@4.17.1 --activate
```
