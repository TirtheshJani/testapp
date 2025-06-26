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

See `frontend/README.md` for running the React development server.
