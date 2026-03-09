# Monitoring Documentation

## Overview

The chatbot includes built-in monitoring through structured request logging and a real-time admin dashboard. All conversations, messages and API requests are stored in PostgreSQL and accessible via the admin interface.

---

## Admin Dashboard

**URL:** http://localhost:3000/admin

The dashboard provides a live overview of system performance including:

| Metric | Description |
|---|---|
| Total conversations | Number of unique chat sessions started |
| Total messages | Total user + assistant messages exchanged |
| Average latency | Mean response time across all requests (ms) |
| Success rate | Percentage of requests that completed without error |
| FAQ match rate | Percentage of questions answered by FAQ vs LLM |
| FAQ matches | Total questions answered directly from knowledge base |
| Error count | Total failed requests |
| Recent request logs | Last 20 API calls with status, latency and endpoint |

---

## What Gets Logged

### Conversations (`conversations` table)
Every new chat session creates a conversation record with a unique UUID and timestamp.

### Messages (`messages` table)
Every user and assistant message is stored with:
- Conversation ID
- Role (user / assistant)
- Content (PII-redacted if applicable)
- Timestamp

### Request logs (`request_logs` table)
Every API call to `/api/chat` is logged with:
- Endpoint
- HTTP status code
- Latency in milliseconds
- Error message (if any)
- Source (`faq` or `llm`)
- FAQ match ID and score (if matched)
- User input (for unmatched question analysis)

### Feedback (`feedback` table)
Every 👍👎 rating submitted by a student is stored with:
- Conversation ID
- Message ID
- Rating (1 = positive, -1 = negative)
- Optional comment

---

## Key Metrics Analysis

### FAQ match rate
A high FAQ match rate (>60%) indicates the knowledge base is well-aligned with what students actually ask. A low rate indicates the FAQ needs expansion.

**Current action:** Monitor unmatched questions in request logs weekly and add new FAQ entries for recurring topics.

### Average latency
- FAQ responses: typically <20ms
- LLM responses: typically 400–1500ms depending on Groq API load

**Threshold:** If average latency exceeds 2000ms consistently, consider caching frequent LLM responses or expanding the FAQ.

### Error rate
Any error rate above 2% warrants investigation. Common causes:
- Groq API key expired or rate limited
- Database connection issues
- Invalid request payloads

### Feedback ratings
A negative feedback rate above 20% signals quality issues. Cross-reference with the source field to determine whether FAQ answers or LLM answers are underperforming.

---

## Verbeteracties (Improvement Actions)

Based on what the monitoring system can reveal, the following improvement cycle is recommended:

1. **Weekly:** Review unmatched questions → add top 5 recurring questions to FAQ
2. **Weekly:** Check feedback ratings → identify low-rated responses → improve FAQ answer or system prompt
3. **Monthly:** Review average latency trends → optimize if degrading
4. **Monthly:** Review error logs → fix recurring error patterns
5. **After updates:** Compare FAQ match rate before/after to validate improvements

---

## Accessing Raw Data

All data is accessible via the PostgreSQL database:

```bash
# Connect to the database
docker exec -it production-chatbot-db psql -U app -d app

# Example queries
SELECT COUNT(*) FROM conversations;
SELECT role, content, created_at FROM messages ORDER BY created_at DESC LIMIT 20;
SELECT source, COUNT(*) FROM request_logs GROUP BY source;
SELECT rating, COUNT(*) FROM feedback GROUP BY rating;
```