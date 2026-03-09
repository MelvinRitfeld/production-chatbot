# Deployment Documentation

## Overview

The UNASAT Campus Support Chatbot is fully containerized using Docker Compose. All services (frontend, backend, database) start with a single command. No manual configuration of individual services is required.

---

## Requirements

| Requirement | Version |
|---|---|
| Docker Desktop | 4.0+ |
| Git | Any |
| Groq API key | Free at console.groq.com |

---

## Automated Setup

### Windows
```powershell
git clone https://github.com/MelvinRitfeld/production-chatbot
cd production-chatbot
powershell -ExecutionPolicy Bypass -File setup.ps1
```

### Linux / Mac
```bash
git clone https://github.com/MelvinRitfeld/production-chatbot
cd production-chatbot
chmod +x setup.sh && ./setup.sh
```

The setup script:
1. Checks if Docker is installed and running
2. Creates `backend/.env` from `backend/.env.example`
3. Prompts for the GROQ_API_KEY
4. Validates the key is filled in
5. Runs `docker compose up --build -d`
6. Prints all access URLs when done

Total setup time: under 15 minutes on first run.

---

## Manual Setup

```bash
cp backend/.env.example backend/.env
# Fill in GROQ_API_KEY in backend/.env
docker compose up --build
```

---

## Environment Variables

All secrets are stored in `backend/.env` which is excluded from git via `.gitignore`.

| Variable | Description | Example |
|---|---|---|
| `GROQ_API_KEY` | Groq API key for LLM access | `gsk_...` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+psycopg2://app:app@db:5432/app` |

The `backend/.env.example` file contains safe placeholder values and is committed to git as a template.

---

## Services

| Service | Port | Description |
|---|---|---|
| frontend | 3000 | Next.js chat interface |
| backend | 8000 | FastAPI REST API |
| db | 5432 | PostgreSQL 16 database |

The backend waits for the database to be healthy before starting (via `depends_on: condition: service_healthy`). The frontend waits for the backend.

---

## Access URLs

| URL | Description |
|---|---|
| http://localhost:3000 | Chatbot interface |
| http://localhost:3000/admin | Admin dashboard |
| http://localhost:8000/docs | Interactive API docs |
| http://localhost:8000/health | Health check endpoint |

---

## Stopping

```bash
# Stop without deleting data
docker compose down

# Stop and delete all data (full reset)
docker compose down -v
```

---

## Troubleshooting

**`connection refused` on backend**
Ensure `DATABASE_URL` uses `@db:5432` not `@localhost:5432` inside Docker.

**`GROQ_API_KEY` missing**
Check `backend/.env` exists and the key is set. The `.env.example` contains placeholder values only.

**Port conflict**
Stop any services running on ports 3000, 8000 or 5432 before starting.