PandaPath
=========

PandaPath is a travel planning platform that combines a Python/Flask backend and an Angular
frontend to build personalized city itineraries. The backend connects to Google Places,
weather forecasts, and Firebase to aggregate attractions, optimizes the route with
OR-Tools, enriches each day with nearby restaurants, and produces a natural-language trip
summary. The frontend guides travellers through preference selection, authentication, and
itinerary review.

Features
--------

- Generates per-day attraction plans tailored to stated preferences and travel dates.
- Scores places with statistical and collaborative models plus aspect-based sentiment.
- Optimizes routes and day splits using OR-Tools with travel-time estimation.
- Surfaces nearby dining options for scheduled meal times.
- Persists user profiles and trip history in Firebase; secures routes with Firebase Auth.
- Calls an external LLaMA-compatible service to narrate the itinerary summary.
- Angular SPA with Tailwind styling and Firebase integration for user flows.

Repository Layout
-----------------

- ``apps/backend`` – Flask API, recommendation engine, data/model layers, and tests.
- ``apps/frontend`` – Angular application presented to travellers.
- ``configs`` / ``docker`` / ``infra`` – placeholders for deployment artefacts.

Backend Setup
-------------

1. **Prerequisites**: Python 3.10+, pip, and access to Google Places & Firebase projects.
2. **Environment**: create ``apps/backend/.env`` (or export variables) with:
   - ``GOOGLE_PLACES_API_KEY`` – Google Places API key.
   - ``PLACES_DB_API_CONFIG`` – JSON string with Firebase service account credentials for place data.
   - ``USERS_DB_API_CONFIG`` – JSON string with Firebase service account credentials for user data.
   - ``USER``, ``PASSWORD``, ``EMAIL`` – Twitter credentials for sentiment bootstrapping via ``twscrape``.
3. **Install**:

   ```bash
   cd apps/backend
   python -m venv .venv
   source .venv/bin/activate  # On Windows use .venv\Scripts\activate
   pip install -r requirements.txt  # or: pip install -e .
   ```

4. **Run the API** (port 5000 by default):

   ```bash
   python -m src.backend.main [--debug] [--from_file] [--no_db]
   ```

   - ``--debug``: emit verbose logs and run quick recommendation sample.
   - ``--from_file``: use cached attraction data from ``outputs``/``data`` instead of Google Places.
   - ``--no_db``: operate without reading/writing Firebase.
5. **Key endpoints** (all served under ``http://localhost:5000``):
   - ``POST /api/recommendation/preferences`` – build itineraries from user profile, dates, and city.
   - ``POST /get_with_text`` – infer preferences from free text and return a recommendation.
   - ``GET /api/restaurants-nearby`` – nearby dining suggestions for a stopover.
   - ``GET /api/trip-history`` / ``GET /api/trip-history/<trip_id>`` – fetch stored trips (Firebase token required).
6. **Testing**:

   ```bash
   pytest
   ```

7. **Docs**: build Sphinx docs for the backend modules.

   ```bash
   cd apps/backend/docs
   make html
   ```

LLaMA Summariser
----------------

The class ``src/api_calls/llama.py`` expects a LLaMA-compatible chat completion endpoint
at ``http://localhost:3001/v1/chat/completions``. Adjust ``Llama.API_URL`` or update the
Angular ``environment`` configuration if you host the summariser elsewhere.

Frontend Setup
--------------

1. **Prerequisites**: Node.js 18+, npm, and Angular CLI (``npm install -g @angular/cli``).
2. **Install**:

   ```bash
   cd apps/frontend
   npm install
   ```

3. **Environment**:
   - Copy ``src/environments/environment.template`` to ``src/environments/environment.ts``.
   - Fill in:
     - ``backendHost`` – base URL of the Flask API (e.g. ``http://localhost:5000/``).
     - ``llamaHost`` – base URL of the summarisation service (e.g. ``http://localhost:3001/``).
     - ``firebase`` config – Firebase web app settings for authentication.
     - ``googlePlacesAPIKey`` – used for client-side maps or autocomplete (if enabled).
4. **Run the dev server**:

   ```bash
   npm start  # opens http://localhost:4200
   ```

5. **Angular tests**:

   ```bash
   npm test
   ```

Development Notes
-----------------

- Restaurant clustering, weather integration, and collaborative filtering models persist
  intermediate artefacts to ``apps/backend/outputs``; ensure the directory remains writable.
- Some tests and utilities expect cached Google Places responses in ``apps/backend/outputs``;
  populate them via ``python -m src.backend.main --from_file`` if working offline.
- The repository contains ``uv.lock`` alongside ``pyproject.toml``; you can also manage the
  backend dependencies with ``uv pip sync`` if you prefer Astral's ``uv`` tooling.

Contributing
------------

- Create feature branches and keep changes scoped to either ``apps/backend`` or ``apps/frontend`` when possible.
- Run the relevant test suites before proposing changes.
- Include updates to this README or the Sphinx docs when adding user-visible behaviour.

License
-------

Project licensing has not been specified. Confirm terms with the maintainers before redistribution.
