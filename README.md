
docker run --name zink -e POSTGRES_PASSWORD=zink -e POSTGRES_USER=zink -d -p 7777:5432 postgres

.env


TAILWIND

https://github.com/tailwindlabs/tailwindcss/releases/download/v3.2.7/tailwindcss-linux-arm64

❯ ./tailwindcss -i render/static/tailwind/input.css -o render/static/tailwind/output.css --watch
❯ ./tailwindcss -i render/static/tailwind/input.css -o render/static/tailwind/output.css --minify
