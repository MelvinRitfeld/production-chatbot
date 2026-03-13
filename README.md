# UNASAT Campus Support Chatbot

A production-ready AI chatbot for UNASAT (Universiteit van Suriname) students. Answers questions about enrollment, schedules, Microsoft Teams, exams and general campus information — instantly via FAQ matching or intelligently via LLM fallback.

## 🌐 Live Demo

| | URL |
|---|---|
| **Chatbot** | https://renewed-recreation-production-a5fa.up.railway.app |
| **Admin dashboard** | https://renewed-recreation-production-a5fa.up.railway.app/admin |

---

## Features

- **Hybrid FAQ + AI** — known questions answered in <10ms, unknown questions via Groq LLM (~500ms)
- **Source indicators** — every response shows whether it came from FAQ or AI
- **Conversation memory** — the AI remembers context from earlier in the conversation
- **Multi-language** — detects and responds in Dutch, English or Sranantongo
- **FAQ suggestions** — AI responses show related FAQ questions ("Misschien bedoel je...?")
- **Feedback buttons** — 👍👎 on every bot message, stored in PostgreSQL
- **Security** — prompt injection detection, PII redaction, rate limiting (20 req/60s)
- **Admin dashboard** — live metrics, latency, success rate at `/admin`
- **Logging** — all conversations and requests logged to PostgreSQL

---

## Documentation

All project documentation is available in the `/docs` folder:

| Document | Description |
|---|---|
| [Architecture](docs/Architectuur_Document.docx) | System design, components, data flows, cost estimate |
| [Deployment Plan](docs/Implementatie_Deploymentplan.docx) | Step-by-step deployment & rollback procedures |
| [Prompt Engineering](docs/Prompt_Engineering.docx) | Prompt design, ecosystem analysis, iteration cycles |
| [Monitoring](docs/Monitoring_Documentatie.docx) | Metrics, logging setup, improvement cycle |
| [Security & Privacy](docs/Security_Documentatie.docx) | Injection detection, PII redaction, rate limiting, AVG compliance |
| [User Test Report](docs/testing_report.md) | Test results, user feedback, resolved issues |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js (React) — port 3000 |
| Backend | FastAPI (Python) — port 8000 |
| Database | PostgreSQL 16 |
| LLM | Groq API — llama-3.3-70b-versatile |
| Local deployment | Docker Compose |
| Production hosting | Railway (auto-deploy on push to `main`) |

---

## Quickstart

### Option 1 — Automated setup (recommended)

**Windows:**
```powershell
git clone https://github.com/MelvinRitfeld/production-chatbot
cd production-chatbot
powershell -ExecutionPolicy Bypass -File setup.ps1
```

**Linux / Mac:**
```bash
git clone https://github.com/MelvinRitfeld/production-chatbot
cd production-chatbot
chmod +x setup.sh && ./setup.sh
```

The script will check Docker, create your `.env`, ask for your API key and start everything automatically.

### Option 2 — Manual setup
```bash
git clone https://github.com/MelvinRitfeld/production-chatbot
cd production-chatbot

cp backend/.env.example backend/.env
# Open backend/.env and set GROQ_API_KEY

docker compose up --build
```

Get a free Groq API key at: https://console.groq.com

---

## Access

### Local
| URL | Description |
|---|---|
| http://localhost:3000 | Chatbot interface |
| http://localhost:3000/admin | Admin dashboard |
| http://localhost:8000/docs | Backend API docs |
| http://localhost:8000/health | Health check |

### Production (Railway)
| URL | Description |
|---|---|
| https://renewed-recreation-production-a5fa.up.railway.app | Chatbot interface |
| https://renewed-recreation-production-a5fa.up.railway.app/admin | Admin dashboard |
| https://production-chatbot-production-6f5a.up.railway.app/docs | Backend API docs |
| https://production-chatbot-production-6f5a.up.railway.app/health | Health check |

---

## Project Structure
```
production-chatbot/
├── setup.ps1                  # Automated setup (Windows)
├── setup.sh                   # Automated setup (Linux/Mac)
├── docker-compose.yml
├── docs/                      # All project documentation
├── backend/
│   ├── main.py                # FastAPI app entrypoint
│   ├── .env.example           # Environment template
│   ├── requirements.txt
│   ├── app/
│   │   ├── services/
│   │   │   └── faq_service.py # FAQ matching + LLM fallback + suggestions
│   │   ├── security/
│   │   │   ├── injection.py   # Prompt injection + PII detection
│   │   │   ├── fallbacks.py   # Safe Dutch fallback messages
│   │   │   └── rate_limiter.py # 20 req/60s per IP
│   │   └── data/
│   │       └── answer_bank.py # FAQ knowledge base (50+ entries)
│   ├── routers/
│   │   ├── chat.py            # POST /api/chat
│   │   ├── feedback.py        # POST /api/feedback
│   │   ├── admin.py           # GET /api/admin/metrics
│   │   └── health.py          # GET /health
│   └── db/
│       ├── models.py          # SQLAlchemy models
│       ├── crud.py            # Database operations
│       └── session.py         # DB connection
└── frontend/
    ├── app/
    │   ├── page.tsx           # Main chat interface
    │   └── layout.tsx
    └── lib/
        ├── api.ts             # API client
        └── types.ts           # TypeScript types
```

---

## Security

| Feature | Implementation |
|---|---|
| Prompt injection | Pattern-based detection, 9 attack patterns, blocked with Dutch fallback |
| PII redaction | Email, phone, ID detection — stored as `[PII_REDACTED]` in DB |
| Rate limiting | 20 requests per 60 seconds per IP, 2 minute block on exceed |
| Input validation | Empty input check, max token limits |
| API key safety | Loaded from `.env`, never committed to git |

---

## Stopping the chatbot
```bash
# Stop containers
docker compose down

# Stop and delete all data
docker compose down -v
```

---

## Troubleshooting

**Backend won't start**
Check that `backend/.env` exists and `GROQ_API_KEY` is set correctly.

**Database connection error**
Make sure `DATABASE_URL` in `backend/.env` uses `@db:5432` not `@localhost:5432`.

**Port already in use**
Stop other services on ports 3000, 8000 or 5432, then retry.

**LLM answers are in the wrong language**
The system prompt instructs the model to match the student's language. If responses seem off, check that your GROQ_API_KEY is valid and the backend started correctly.