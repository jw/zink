
# ElevenBits

This is the elevenbits website project.

## Development

Both Python and Node are used.  Python runs the Django, the Javascript is used to create the css files (the css is based on tailwindcss and daisyui).
The system runs on a render.com Dockerfile environment.

### Database

Make sure to start the database on your local machine:

```bash
❯ docker run --name zink -e POSTGRES_PASSWORD=zink -e POSTGRES_USER=zink -d -p 7777:5432 postgres
```

Several environment variables need to be added to the `.env` file.  This `.env` file needs to remain private to you.  It should not be part of the repo!  See the `.env-example` for more information.

### CSS

Best to automatically generate the tailwind/daisy css via [yarn](https://yarnpkg.com/):

```bash
❯ yarn tailwindcss -i core/static/tailwind/input.css -o core/static/tailwind/output.css --watch
```

Yarn 3.4.1 is used.  First make sure you're using the latest Node LTS (use [nvm](https://github.com/nvm-sh/nvm) to do so).  Best to install yarn via:

```bash
❯ corepack enable
❯ corepack prepare yarn@3.4.1 --activate
```
