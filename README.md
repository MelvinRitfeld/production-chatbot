# UNASAT Campus Support Chatbot

Een productieklare AI-chatbot voor studenten van UNASAT (Universiteit van Suriname).  
De chatbot beantwoordt vragen over inschrijving, roosters, Microsoft Teams, kosten en algemene campusinformatie.

## Tech Stack

| Laag | Technologie |
|---|---|
| Frontend | Next.js (React) — poort 3000 |
| Backend | FastAPI (Python) — poort 8000 |
| Database | PostgreSQL 16 |
| LLM | Groq API (llama-3.3-70b-versatile) |
| Containerisatie | Docker & Docker Compose |

## Vereisten

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) geïnstalleerd en actief
- Git

## Quickstart

### 1. Clone de repository

```bash
git clone https://github.com/MelvinRitfeld/production-chatbot.git
cd production-chatbot
git checkout melvin-backup
```

### 2. Maak het `.env` bestand aan

```bash
cp backend/.env.example backend/.env
```

Open `backend/.env` en vul de waarden in:

```env
DATABASE_URL=postgresql+psycopg2://app:app@db:5432/app
GROQ_API_KEY=jouw_groq_api_key_hier
```

> Een gratis Groq API key is aan te maken op [console.groq.com](https://console.groq.com)

### 3. Start de applicatie

```bash
docker compose up --build
```

De eerste keer duurt dit ~5 minuten. Daarna is de chatbot beschikbaar op:

| Service | URL |
|---|---|
| Chatbot (frontend) | http://localhost:3000 |
| Admin dashboard | http://localhost:3000/admin |
| Backend API | http://localhost:8000 |
| API docs | http://localhost:8000/docs |

## Hoe werkt het?

1. Student stuurt een bericht via de frontend
2. Backend controleert eerst de FAQ-database (token scoring, drempel = 4)
3. **FAQ match** → direct antwoord (~10ms)
4. **Geen match** → Groq LLM met UNASAT systeemprompt (~500ms)
5. Alles wordt gelogd in PostgreSQL (gesprekken, berichten, latency)

## Projectstructuur

```
production-chatbot/
├── docker-compose.yml
├── backend/
│   ├── main.py                      # FastAPI applicatie
│   ├── .env                         # Secrets (niet in git)
│   ├── .env.example                 # Template voor .env
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── app/
│   │   ├── services/faq_service.py  # FAQ matching + LLM fallback
│   │   └── data/answer_bank.py      # FAQ kennisbank
│   ├── db/
│   │   ├── session.py               # Database verbinding
│   │   ├── crud.py
│   │   └── models.py
│   └── routers/
│       ├── chat.py
│       ├── health.py
│       └── admin.py
└── frontend/
    ├── Dockerfile
    └── app/                         # Next.js pagina's
```

## Stoppen

```bash
docker compose down
```

Om ook de database data te verwijderen:

```bash
docker compose down -v
```

## Troubleshooting

**Backend start niet op**  
Controleer of `backend/.env` bestaat en `DATABASE_URL` de hostnaam `db` bevat (niet `localhost`).

**Poort al in gebruik**  
Zorg dat poorten 3000, 8000 en 5432 vrij zijn voordat je start.

**Docker build duurt lang**  
Normaal bij de eerste build. Daarna zijn layers gecached en gaat het sneller.

**Groq API geeft een fout**  
Controleer of de `GROQ_API_KEY` in `backend/.env` geldig is via [console.groq.com](https://console.groq.com).