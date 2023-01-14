# ElevenBits website

## Development setup

Make sure there is a database:

```bash
$ docker run --name zink -e POSTGRES_PASSWORD=s3cr3t -e POSTGRES_USER=zink -p 43210:5432 -d postgres
```
Also make sure there is a `.env`, containing the required environment variables.  See the `.env.example` for information.

Run the website via:

```bash
$ python manage.py migrate
$ python manage.py runserver
```
