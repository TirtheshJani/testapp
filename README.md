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


## Logs

Application logs are written to `logs/app.log` inside the project directory.
=======
## Local Development with Docker

1. Ensure you have [Docker](https://docs.docker.com/get-docker/) installed.
2. Build and start the containers:

   ```bash
   docker-compose up --build
   ```
3. Visit `http://localhost:5000` to access the application.
4. PostgreSQL is exposed on port `5432` with default credentials `postgres/postgres` and the database `sport_agency_dev`.

Application code is mounted into the container for live reloading during development.
