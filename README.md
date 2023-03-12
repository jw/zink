
# ElevenBits

## Development

Both Python and Node are used.  Python runs the Django, the Javascript is used to create the css files (the css is based on tailwindcss and daisyui).
The system runs on a render.com blueprint envrinonment.

### Database

Make sure to start the database on your local machine:

```bash
❯ docker run --name zink -e POSTGRES_PASSWORD=zink -e POSTGRES_USER=zink -d -p 7777:5432 postgres
```

Several environment variables need to be added to the `.env` file.  This `.env` file needs to remain private to you.  It should not be part of the repo!  See the `.env-example` for mare information.

### CSS

Best to automatically generate the tailwind/daisy css.

```bash
❯ ./tailwindcss -i render/static/tailwind/input.css -o render/static/tailwind/output.css --watch
```
