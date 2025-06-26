# Frontend

This directory contains the React application built with Vite. The app connects to the Flask API in the repository root.

## Development server

Install dependencies once using npm (or yarn):

```bash
cd frontend
npm install
```

Then start the Vite development server:

```bash
npm run dev
```

The server proxies API requests to `http://localhost:5000` so make sure the Flask backend is running locally on port 5000.
