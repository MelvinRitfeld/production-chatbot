# Monitoring Documentatie

## Overzicht

De chatbot bevat ingebouwde monitoring via gestructureerde logging van verzoeken en een realtime admin-dashboard. Alle gesprekken, berichten en API-aanroepen worden opgeslagen in PostgreSQL en zijn toegankelijk via de admininterface.

---

## Admin Dashboard

**URL:** http://localhost:3000/admin

Het dashboard geeft een live overzicht van de prestaties van het systeem, waaronder:

| Metric | Beschrijving |
|---|---|
| Totaal aantal gesprekken | Aantal unieke chatsessies dat is gestart |
| Totaal aantal berichten | Totaal aantal berichten van gebruiker en chatbot |
| Gemiddelde responstijd | Gemiddelde responstijd van alle verzoeken (ms) |
| Succespercentage | Percentage verzoeken dat zonder fout is afgerond |
| FAQ-matchpercentage | Percentage vragen dat door de FAQ wordt beantwoord versus het LLM |
| Aantal FAQ-matches | Totaal aantal vragen dat direct uit de kennisbank is beantwoord |
| Aantal fouten | Totaal aantal mislukte verzoeken |
| Recente request-logs | Laatste 20 API-aanroepen met status, responstijd en endpoint |

---

## Wat wordt gelogd

### Conversations (`conversations` tabel)

Elke nieuwe chatsessie maakt een record aan in de tabel `conversations` met een unieke UUID en een tijdstempel.

### Messages (`messages` tabel)

Elk bericht van de gebruiker en de chatbot wordt opgeslagen met:

- Conversation ID
- Rol (user / assistant)
- Inhoud (persoonlijke informatie wordt indien nodig verwijderd)
- Tijdstempel

### Request logs (`request_logs` tabel)

Elke API-aanroep naar `/api/chat` wordt gelogd met:

- Endpoint
- HTTP statuscode
- Responstijd in milliseconden
- Foutmelding (indien aanwezig)
- Bron (`faq` of `llm`)
- FAQ match ID en score (indien er een match is)
- Gebruikersvraag (voor analyse van vragen zonder match)

### Feedback (`feedback` tabel)

Elke 👍👎 beoordeling van een student wordt opgeslagen met:

- Conversation ID
- Message ID
- Beoordeling (1 = positief, -1 = negatief)
- Optionele opmerking

---

## Analyse van belangrijke metrics

### FAQ matchpercentage

Een hoog FAQ-matchpercentage (>60%) betekent dat de kennisbank goed aansluit bij de vragen die studenten stellen.  
Een laag percentage betekent dat de FAQ moet worden uitgebreid.

**Huidige actie:**  
Controleer wekelijks vragen zonder match in de request-logs en voeg nieuwe FAQ-items toe voor onderwerpen die vaak terugkomen.

---

### Gemiddelde responstijd

- FAQ-antwoorden: meestal <20 ms  
- LLM-antwoorden: meestal 400–1500 ms, afhankelijk van de belasting van de Groq API

**Drempelwaarde:**  
Als de gemiddelde responstijd regelmatig boven de 2000 ms komt, kan het nuttig zijn om veelvoorkomende LLM-antwoorden te cachen of de FAQ uit te breiden.

---

### Foutpercentage

Een foutpercentage boven 2% moet worden onderzocht. Veel voorkomende oorzaken zijn:

- Groq API-sleutel verlopen of rate-limiting
- Problemen met de databaseverbinding
- Ongeldige API-verzoeken

---

### Feedback beoordelingen

Een negatief feedbackpercentage boven 20% kan wijzen op kwaliteitsproblemen. Vergelijk dit met het veld **source** om te bepalen of FAQ-antwoorden of LLM-antwoorden verbeterd moeten worden.

---

## Verbeteracties

Op basis van de informatie uit het monitoringsysteem wordt de volgende verbetercyclus aanbevolen:

1. **Wekelijks:** controleer vragen zonder match → voeg de 5 meest voorkomende vragen toe aan de FAQ  
2. **Wekelijks:** controleer feedback → verbeter FAQ-antwoorden of de system prompt  
3. **Maandelijks:** controleer trends in responstijden → optimaliseer indien nodig  
4. **Maandelijks:** analyseer foutlogs → los terugkerende fouten op  
5. **Na updates:** vergelijk het FAQ-matchpercentage voor en na de wijziging om verbeteringen te bevestigen

---

## Toegang tot ruwe data

Alle data is toegankelijk via de PostgreSQL-database:

```bash
# Verbinden met de database
docker exec -it production-chatbot-db psql -U app -d app

# Voorbeeld queries
SELECT COUNT(*) FROM conversations;
SELECT role, content, created_at FROM messages ORDER BY created_at DESC LIMIT 20;
SELECT source, COUNT(*) FROM request_logs GROUP BY source;
SELECT rating, COUNT(*) FROM feedback GROUP BY rating;