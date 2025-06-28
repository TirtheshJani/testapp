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
3. **Database migrations**
   ```bash
   flask db upgrade
   ```
4. **Run the server**
   ```bash
   flask run
   ```

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

## Docker

A `Dockerfile` and `docker-compose.yml` are provided. To run the app with PostgreSQL using Docker:
```bash
docker-compose up --build
```
This starts the Flask server on port `5000` and a Postgres database on `5432`.

