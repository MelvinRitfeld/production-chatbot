# Deployment Documentatie

## Overview

De UNASAT Campus Support Chatbot draait volledig in Docker-containers met behulp van Docker Compose.
Alle services (frontend, backend en database) kunnen met één commando worden gestart.
Handmatige configuratie van afzonderlijke services is niet nodig.

---

## Requirements

| Requirement | Versie |
|---|---|
| Docker Desktop | 4.0+ |
| Git | Any |
| Groq API Key | Gratis te verkrijgen via console.groq.com |

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

Het installatiescript voert de volgende stappen uit:
1. Controleert of Docker is geïnstalleerd en actief is
2. Maakt het bestand `backend/.env` aan op basis van `backend/.env.example`
3. Vraagt om de `GROQ_API_KEY` (Prompting)
4. Controleert of de key is ingevuld
5. Voert het commando `docker compose up --build -d` uit
6. Toont alle toegang-URL’s wanneer de installatie voltooid is

Total setup time: meestal minder dan 15 minuten bij de eerste uitvoering.

---

## Manual Setup

```bash
cp backend/.env.example backend/.env
# Fill in GROQ_API_KEY in backend/.env
docker compose up --build
```

---

## Environment Variables

Alle gevoelige gegevens worden opgeslagen in `backend/.env.`
Dit bestand is uitgesloten van Git via `.gitignore.`

| Variabele | Beschrijving | Voorbeeld |
|---|---|---|
| `GROQ_API_KEY` | Groq API key voor toegang tot het LLM | `gsk_...` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+psycopg2://app:app@db:5432/app` |

Het bestand `backend/.env.example` bevat voorbeeldwaarden en wordt als template in Git opgeslagen.

---

## Services

| Service | Port | Beschrijving |
|---|---|---|
| frontend | 3000 | Next.js chatinterface |
| backend | 8000 | FastAPI REST API |
| db | 5432 | PostgreSQL 16 database |

De backend wacht totdat de database actief is voordat deze start (via `depends_on: condition: service_healthy`). De frontend wacht totdat de backend beschikbaar is.

---

## Toegang-URL's

| URL | Beschrijving |
|---|---|
| http://localhost:3000 | Chatbot gebruikersinterface |
| http://localhost:3000/admin | Admin dashboard |
| http://localhost:8000/docs | Interactieve API-documentatie |
| http://localhost:8000/health | Health-check endpoint |

---

## Stoppen van het systeem

```bash
# Stoppen zonder data te verwijderen
docker compose down

# Stoppen en alle data verwijderen (volledige reset)
docker compose down -v
```

---

## Troubleshooting

**`connection refused` on backend**
Zorg ervoor dat `DATABASE_URL` `@db:5432` gebruikt en niet `@localhost:5432` wanneer Docker wordt gebruikt.

**`GROQ_API_KEY` missing**
Controleer of `backend/.env` bestaat en of de sleutel is ingesteld. Het bestand `.env.example` bevat alleen plaatsaanduidingen.

**Port conflict**
Stop eventuele services die al gebruik maken van poorten 3000, 8000 of 5432 voordat het systeem wordt gestart.