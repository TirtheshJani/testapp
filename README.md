# Pro Sports - Talent Agency

This repository contains a Flask API backend and a React frontend used to manage athlete data for a sports talent agency.

## Backend setup (Flask)

1. **Python environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. **Environment variables** – create a `.env` file in the project root and set:
   - `SECRET_KEY` – Flask session secret
   - `DATABASE_URL` – SQLAlchemy database URI
   - `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET`
   - `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET`
   - `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET` and `AZURE_TENANT_ID`
   - `NBA_API_TOKEN` optional access token for NBA stats API
   - `NBA_API_BASE_URL` override base URL for NBA API (optional)
### Initialize the database
Run database migrations to create all tables:

```bash
flask db upgrade
```

The latest migrations add indexes on stat tables for faster lookups. Run the
above command whenever pulling new code to ensure these indexes exist.
The July 15 migration also enforces unique season and game stats and
checks that game scores are non-negative.

3. **Run the server**
   ```bash
   flask run
   ```

4. **Scheduled jobs** (optional)
   Set `ENABLE_SCHEDULER=true` in your `.env` to start APScheduler with nightly
   and weekly sync tasks when the Flask app launches. Game results are pulled
   each night at 2 AM and player stats update every Sunday at 3 AM.

## Frontend setup (React)

```bash
cd frontend
npm install
npm run dev
```
The Vite dev server proxies API requests to `http://localhost:5000`, so run the Flask backend first.

## Running tests

Install Python dependencies as above and then install the test packages:
```bash
pip install -r requirements-dev.txt
pytest
```

## User authentication

Local accounts can be created directly in the app. Visit `/auth/register` to
sign up. New users are automatically logged in and assigned the default `viewer`
role. Existing users can log in at `/auth/login` using their username or email
address and password. OAuth logins for Google, GitHub and Microsoft remain
available when configured.

## Docker

A `Dockerfile` and `docker-compose.yml` are provided. To run the app with PostgreSQL using Docker:
```bash
docker-compose up --build
```
This starts the Flask server on port `5000` and a Postgres database on `5432`.


## Supported browsers

The React frontend is regularly tested on the latest versions of Chrome, Firefox, Safari and Edge. Other modern browsers that support ES2015+ features should also work.

## Checking layout on mobile vs. desktop

To verify the responsive design manually:
1. Start the Flask backend with `flask run` and the frontend with `npm run dev`.
2. Open the app in a browser and use developer tools to emulate devices.
3. Test common viewport widths (e.g., 375px and 1280px) and ensure navigation and forms render correctly.

For automated cross-browser or cross-device testing, you can integrate a service like BrowserStack or add Playwright and run `npx playwright test`.

## Documentation

Additional technical documentation is available in the `docs/` directory:

- `database_schema.md` – overview of the database tables and relationships
- `api_endpoints.md` – list of API endpoints with parameters
- `user_guide_athletes.md` – instructions for managing athlete profiles

The dashboard also shows a **Client Satisfaction** percentage. This metric is a
placeholder value (set to 98.7%) for the demo. In Phase 3 the client may provide
a formula or survey data to calculate it dynamically.

An **📊 View Analytics** button now links to `/analytics`. This page simply states "Coming soon" until full reporting features arrive in Phase 5.
A **📁 Upload Media** button in the dashboard directs to `/media/upload` where administrators can attach files to athlete profiles.
The API exposes a `/api/rankings/top` endpoint returning five placeholder athletes with an overall score. These values remain static until a real ranking system is implemented.
The rankings page also includes a **⚙️ Customize Metrics** button. Clicking it opens a modal explaining that ranking weight adjustments are coming in a future phase.
