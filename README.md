# MallNav

MallNav helps shoppers find stores and staff keep listings accurate, providing the directory and mall operations API for planned indoor navigation and amenity discovery.

## Core Features & Current Status

**Implemented**

- Visitors can browse `/directory` without an account and filter store cards by name, category, and accessibility. The public API also returns zones, amenities, two coordinates, and a schedule by day.
- Tenants and operators sign in through the API. Operators can create, update, and delete stores. A tenant can propose changes to opening hours only for their assigned store.
- Operators can list pending proposals and approve or reject them with optional review notes. Submission leaves published hours intact. Approval merges the proposed days into the store schedule.

**In progress / roadmap**

- Staff sign-in, proposal submission, and review are API workflows. The web app currently provides a landing page and a visitor directory.
- The data model supports location and amenity information. A floor map, indoor pathfinding, and a shopper-facing amenity view are pending.

## System Architecture

```text
Next.js dev server (:3000)
           |
           | serves /directory
           v
Shopper's browser ---- GET store list ----+
                                         |
Staff API client ---- login / review ----+--> FastAPI (:8000)
                                                |
                                      routes and role checks
                                                |
                                      synchronous services
                                                |
                                      SQLAlchemy / psycopg
                                                |
                                                v
                                      PostgreSQL 16 (Docker)
                                      host :5433 -> db :5432
                                      stores, users,
                                      store_change_requests
```

The browser calls FastAPI directly and receives JSON. Each database-backed request gets a SQLAlchemy session that closes when the request finishes. Alembic applies schema changes to the same database. Compose starts PostgreSQL and persists its data in the `postgres_data` volume. The API and web server run on the host.

The migrations use standard PostgreSQL types. The current application has no pgvector extension, Redis cache, Celery worker, or message broker. Reviews execute within the HTTP request.

## Tech Stack & Design Choices

| Layer | Technology | Role in the implementation |
| --- | --- | --- |
| API | FastAPI, Pydantic, Uvicorn | Typed request and response models enforce the API contract and generate interactive documentation. |
| Persistence | PostgreSQL 16, SQLAlchemy, psycopg, Alembic | Foreign keys link accounts and proposals to stores. Versioned migrations reproduce the schema. |
| Authentication | PyJWT, pwdlib with Argon2 | Password hashes support staff sign-in and signed, expiring bearer tokens identify subsequent requests. |
| Web | Next.js App Router, React, TypeScript, Tailwind CSS | A typed API client feeds a responsive directory with local filter state. |
| Local infrastructure and CI | Docker Compose, GitHub Actions, ESLint | Compose supplies the database. CI installs frontend dependencies and runs lint on pushes to `main`. |

## Engineering Highlights & Trade-offs

- **Concurrent review.** Approval locks the proposal row and its store row with `SELECT ... FOR UPDATE`. It merges the proposed days into the current schedule and commits the store update and review decision together. A second review of a completed proposal receives `409 Conflict`. Concurrent approvals for the same store wait for the store lock. [Review service](backend/app/services/change_request_service.py)
- **Current permissions.** Each protected request verifies the token and looks up its subject in the database. Role and store checks use the current account, so a reassignment takes effect even while an older token is valid. This costs one account lookup per protected request. [Authorization dependencies](backend/app/api/deps.py)
- **Structured proposals.** A change request links its author and store through foreign keys and stores its payload in JSONB. The input schema permits only an `hours` change with at least one day. Unspecified days survive approval, while a submitted day replaces that day's entry. [Proposal schema](backend/app/schemas/change_request.py)
- **Directory search.** The browser downloads one page of stores and filters it locally, keeping each keystroke off the API. The default page holds up to 100 stores. API clients can search across the database and paginate with `skip` and `limit`. [Directory page](frontend/mall_nav/app/directory/page.tsx) · [Store queries](backend/app/services/store_service.py)

## API Overview

Paths below use the default API prefix. Protected operations accept `Authorization: Bearer <access_token>`. Interactive documentation is available at `/docs` and the OpenAPI schema at `/openapi.json`.

| Method | Route | Access | Purpose |
| --- | --- | --- | --- |
| GET | `/health` | Public | Return API status and environment. Database connectivity is checked separately. |
| GET | `/api/v1/stores/` | Public | List stores. Supports `name` (case-insensitive partial match), `category`, `accessible`, `zone`, `skip`, and `limit`. |
| GET | `/api/v1/stores/{id}` | Public | Read one store or return 404. |
| POST | `/api/v1/auth/login` | Staff credentials | Exchange a JSON email and password for a bearer token and account details. |
| POST | `/api/v1/stores/` | Operator | Create a store and return 201. |
| PATCH | `/api/v1/stores/{id}` | Operator | Update supplied fields directly. |
| DELETE | `/api/v1/stores/{id}` | Operator | Delete a store and return 204. |
| POST | `/api/v1/stores/{store_id}/change-requests` | Assigned tenant | Submit proposed hours and return a pending request (201). |
| GET | `/api/v1/change-requests/pending` | Operator | List proposals awaiting review. |
| POST | `/api/v1/change-requests/{request_id}/approve` | Operator | Apply proposed hours and record the review. |
| POST | `/api/v1/change-requests/{request_id}/reject` | Operator | Record the rejection and preserve published hours. |

For example, a tenant can submit the following body to change Monday's hours. Both review endpoints accept a JSON object with optional `review_notes`, so `{}` is sufficient.

```json
{
  "proposed_changes": {
    "hours": {
      "monday": { "open": "09:00", "close": "20:00", "is_closed": false }
    }
  }
}
```

## Project Structure

```text
.
|-- backend/
|   |-- app/
|   |   |-- main.py            FastAPI entry point and CORS settings
|   |   |-- api/               Database and auth dependencies, v1 routers and endpoints
|   |   |-- core/              Settings, password hashing and token handling
|   |   |-- db/                SQLAlchemy base, engine and session lifecycle
|   |   |-- models/            Store, user and change-request tables
|   |   |-- schemas/           Request validation and response models
|   |   `-- services/          Queries, writes and review transactions
|   |-- alembic/versions/      Database migration history
|   |-- alembic.ini            Migration configuration
|   |-- tests/                 Login and store permission tests
|   |-- .env.example           Backend settings template
|   `-- requirements.txt       Python dependencies
|-- frontend/mall_nav/
|   |-- app/                   Landing page, directory, layout and styles
|   |-- services/api.ts        Typed store client
|   |-- public/                Static assets
|   `-- package.json           Frontend scripts and dependencies
|-- .github/workflows/         Frontend lint workflow
`-- docker-compose.yml         PostgreSQL service and persistent volume
```

## Getting Started (Local Setup)

Use Docker with Compose, Python 3.11 (used for the tested local environment), and Node.js with npm. The locked Next.js package requires Node.js 20.9 or later. The commands below use PowerShell and start at the repository root containing `docker-compose.yml`.

### 1. Start PostgreSQL and prepare the backend

```powershell
docker compose up -d db
cd backend
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
if (!(Test-Path .env)) { Copy-Item .env.example .env }
```

Edit `backend/.env`. For the supplied local Compose service, set `DATABASE_URL` to the following value. It uses the host port and explicitly selects the installed psycopg driver. Set `JWT_SECRET` to a private random signing key.

```dotenv
DATABASE_URL=postgresql+psycopg://postgres:postgrespassword@localhost:5433/mallnav_db
```

| Backend variable | Requirement or default |
| --- | --- |
| `DATABASE_URL`, `JWT_SECRET` | Both required at application startup. Alembic imports the same settings. |
| `APP_ENV` | Defaults to `development`. |
| `PROJECT_NAME`, `API_V1_STR` | Default to `MallNav Backend` and `/api/v1`. |
| `JWT_ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES` | Default to `HS256` and `30`. |
| `OAUTH_CLIENT_ID`, `OAUTH_CLIENT_SECRET` | Default to empty strings. Reserved settings with no mounted OAuth flow. |

### 2. Apply migrations and start the API

From `backend/`, once PostgreSQL is ready:

```powershell
.\.venv\Scripts\python.exe -m alembic upgrade head
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

Open [API documentation](http://localhost:8000/docs) to try the endpoints. On a fresh database, [the store list](http://localhost:8000/api/v1/stores/) returns an empty array. Migrations create the schema. Staff operations require an existing tenant or operator account. The repository has no seed command, demo credentials, or public registration route.

### 3. Start the frontend

Create `frontend/mall_nav/.env.local` with the following setting. Include the API prefix because the client appends `/stores/`.

```dotenv
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

In a second terminal, from the repository root:

```powershell
cd frontend/mall_nav
npm ci
npm run dev
```

Open the [store directory](http://localhost:3000/directory). The API allows local browser requests from both `localhost:3000` and `127.0.0.1:3000` over HTTP.

## Running Tests

From `backend/` with the environment above:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests
```

The suite covers staff login, public store reads, operator-only writes, expired tokens, missing accounts, and role changes after token issuance. The tests mock database access. They can run with PostgreSQL stopped and do not exercise row locking or migrations.

From `frontend/mall_nav/`, run `npm run lint` for the same check used by GitHub Actions. The frontend package defines no test script.

## Roadmap

- Connect staff sign-in, tenant proposals, and operator review to the web app.
- Expose stored amenities and zones in the directory and add a floor map for indoor navigation.
- Add PostgreSQL integration coverage for approval, rejection, and concurrent reviews, followed by a browser test of the tenant-to-operator workflow.
