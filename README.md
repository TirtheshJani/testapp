# Pro Sports - Talent Agency

## API Endpoints

### Search Athletes
`GET /api/athletes/search`

Query parameters:
- `q` – text search across athlete name, position and current team
- `sport` – sport code or id
- `min_age` / `max_age` – filter by age range
- `min_height` / `max_height` – filter by height in centimeters
- `min_weight` / `max_weight` – filter by weight in kilograms

The endpoint returns a JSON object containing the matched athletes ordered by overall rating.


## Frontend Development

The project ships with Jinja templates under `templates/main` that render a
basic HTML/CSS interface. You can use these built-in pages without touching the
React code. For a richer client-side experience, the React app in
`frontend/` is available—see its README for development instructions.

## Logs

Application logs are written to `logs/app.log` inside the project directory.
## Local Development with Docker

1. Ensure you have [Docker](https://docs.docker.com/get-docker/) installed.
2. Build and start the containers:

   ```bash
   docker-compose up --build
   ```
3. Visit `http://localhost:5000` to access the application.
4. PostgreSQL is exposed on port `5432` with default credentials `postgres/postgres` and the database `sport_agency_dev`.

Application code is mounted into the container for live reloading during development.


## Maintenance Scripts

The `scripts` directory contains simple utilities for working with the project.

### backup_db.sh
Dumps the PostgreSQL database defined in `DATABASE_URL` to a timestamped file. A backup directory may be supplied as the first argument (defaults to `backups`).

```bash
DATABASE_URL=postgresql://user:pass@host/dbname bash scripts/backup_db.sh [backup_dir]
```

### check_storage.py
Checks that a path exists and has at least the specified free space in megabytes (defaults to `100` MB).

```bash
python scripts/check_storage.py /path/to/dir [required_mb]
```
