# Architectuur Document

**Groepsnaam:** Project X  
**Docent:** R. Christian  
**Groepsleden:**  
- Bindya Kewalapat — SE/1123/034  
- Dharandjai Patan — SE/1123/056  
- Masjermi Waakzaam — SE/1123/101  
- Melvin Ritfeld — SE/1123/075  
- Wasil Nanhekhan — SE/1123/052  

**Datum:** 7 maart 2026



---



## Inhoudsopgave

1. Systeemoverzicht & Architectuurdiagram
2. Gebruikte Componenten
3. Onderbouwing van Keuzes
4. Datastromen
5. Afhankelijkheden
6. Schaalbaarheid
7. Risico's en Beperkingen
8. Globale Kosteninschatting

---

## 1. Systeemoverzicht & Architectuurdiagram

Het systeem is een hybride FAQ-chatbot voor studenten. Het combineert een statische FAQ-kennisbank met een Large Language Model (LLM). Wanneer een vraag niet in de FAQ staat, wordt het LLM gebruikt om alsnog een antwoord te geven.

### Architectuurdiagram (Flow)

Hieronder is de datastroom visueel weergegeven, van de student tot aan de onderliggende services:
```
       [Student]
           │
           ▼
  [Next.js :3000] (Frontend)
           │
           ▼
  [FastAPI :8000] (Backend) ────────► [Groq API] (LLM Fallback)
           │
           ▼
 [PostgreSQL :5432] (Database)
```

### Overzicht van Systeemcomponenten

| Component | Technologie | Poort / Locatie | Verantwoordelijkheid |
|---|---|---|---|
| Frontend | Next.js 14 (React) | localhost:3000 | Chatinterface voor studenten, admin-dashboard op /admin, en realtime communicatie met de backend. |
| Backend | FastAPI (Python 3.11) | localhost:8000 | REST API, verzorgt FAQ-matching, LLM-aanroepen, logging en beheert admin-endpunten. |
| Database | PostgreSQL 16 | localhost:5432 (intern) | Persistentie van conversations, messages en request_logs. |
| LLM API | Groq Cloud (llama-3.3-70b-versatile) | api.groq.com (extern) | Generatieve AI-antwoorden wanneer de FAQ-kennisbank geen match oplevert. |
| Containerisatie | Docker + Docker Compose | — | Enkelvoudige deployment via het commando `docker compose up --build`. |

---

## 2. Gebruikte Componenten

**Frontend:** De frontend is gebouwd met Next.js 14 en vormt de gebruikersinterface van de applicatie. Studenten kunnen via deze interface vragen stellen aan de chatbot. Daarnaast bevat het een administratief dashboard dat inzicht geeft in prestatie-indicatoren, zoals gemiddelde latentie, succespercentages en de verhouding tussen FAQ- en LLM-antwoorden. Communicatie met de backend verloopt via REST-API calls naar FastAPI.

**Backend:** De belangrijkste logica van de chatbot zit in de FastAPI-backend. Bij een inkomende vraag splitst het systeem deze op in woorden en verwijdert het de algemene Nederlandse stopwoorden. Vervolgens berekent het een match-score ten opzichte van de FAQ-database, waarbij specifieke 'tags' extra zwaar wegen. Pas als deze score onder de drempelwaarde van 4 valt, wordt de vraag als fallback naar de Groq LLM API gestuurd. Hierdoor worden onnodige API-aanroepen voorkomen.

**Database:** De PostgreSQL-database beheert drie cruciale tabellen:
- `conversations`: Slaat de unieke chatsessies van gebruikers op.
- `messages`: Bewaart individuele berichten inclusief timestamps en de bron van het antwoord (FAQ of AI).
- `request_logs`: Registreert technische metadata zoals responstijden, statuscodes en tokengebruik ten behoeve van het admin-dashboard.

**LLM API:** Groq Cloud wordt gebruikt om antwoorden te genereren wanneer een vraag niet in de FAQ staat, gebruikmakend van het llama-3.3-70b-versatile model om snel en accuraat complexe vragen te beantwoorden.

**Containerisatie:** Alle services draaien in geïsoleerde Docker-containers, gedefinieerd in een `docker-compose.yml` bestand. Met het commando (`docker compose up --build`) kunnen alle onderdelen van het systeem tegelijk worden gestart. De interne communicatie verloopt via een Docker-netwerk, waarbij enkel poort 3000 (Frontend) en 8000 (Backend) extern bereikbaar zijn gesteld.



---

## 3. Onderbouwing van Keuzes

### Waarom Groq in plaats van OpenAI?

- **Snelheid:** De speciale LPU-hardware van Groq levert responstijden van minder dan 300 milliseconden, in contrast met de 1 tot 3 seconden van OpenAI's GPT-4o.
- **Kosten:** Groq biedt een zeer royale gratis tier (ongeveer 14.400 tokens per minuut), terwijl OpenAI directe betaling vereist.
- **Open-weight model:** Het gebruikte llama-3.3-70b model is publiek beschikbaar, wat de applicatie beschermt tegen vendor lock-in.

### Waarom een Hybride (FAQ & LLM) Model?

- Veelgestelde vragen (zoals over inschrijvingen of openingstijden) worden direct en kosteloos beantwoord via de FAQ-kennisbank.
- Het LLM biedt de benodigde context en nuance voor uitzonderlijke of complexe vragen.
- De gekozen matching-drempelwaarde (4 punten) is empirisch vastgesteld: dit is laag genoeg om valide FAQ-vragen te herkennen, maar hoog genoeg om irrelevante matches (false positives) uit te sluiten.

### Waarom Docker?

- **Reproduceerbaarheid:** Elke ontwikkelaar kan via één commando exact dezelfde stack lokaal opstarten.
- **Isolatie:** Het voorkomt conflicten tussen configuraties van Python, Node.js of PostgreSQL op het host-systeem.
- **Schaalbaarheid:** Containers kunnen later eenvoudig meerdere keren worden gestart of worden verplaatst naar systemen zoals Kubernetes.


---

## 4. Datastromen

Hieronder is het stapsgewijze verloop van een chatbericht uitgewerkt:

| Stap | Actie | Actor | Detail |
|---|---|---|---|
| 1 | Student stuurt bericht | Browser (Next.js) | Maakt een `POST /api/chat` aanroep met `{ message, conversation_id }`. |
| 2 | Backend ontvangt verzoek | FastAPI endpoint | Valideert de payload en slaat het bericht op in PostgreSQL. |
| 3 | FAQ-matching | Token-scoring engine | Tokeniseert de vraag, filtert Dutch stopwords, en berekent een score waarbij tags dubbel (×2) tellen. De drempelwaarde is 4. |
| 4a | FAQ-hit (Score ≥ 4) | Backend | Retourneert direct het opgeslagen FAQ-antwoord. Dit vereist geen LLM-aanroep en brengt geen kosten met zich mee. |
| 4b | Geen match (Score < 4) | Groq API (extern) | Stuurt een POST-verzoek naar api.groq.com met de systeemprompt en de gestelde gebruikersvraag. |
| 5 | LLM-antwoord genereren | Groq llama-3.3-70b | Creëert een passend antwoord (gelimiteerd op max 500 tokens met een temperature van 0.5). |
| 6 | Logging | PostgreSQL | Het volledige request wordt gelogd (inclusief latentie, successtatus, gebruikte model en tokenaantal). |
| 7 | Respons afleveren | Frontend | De JSON-respons wordt teruggestuurd en gevisualiseerd in het chatvenster van de student. |



---

## 5. Afhankelijkheden

- **Groq API (api.groq.com):** Een actieve internetverbinding en API-sleutel zijn vereist. Bij een storing vallen LLM-antwoorden weg, maar blijft de FAQ operationeel.
- **Docker Engine (≥ 24.0):** Noodzakelijk op de hostmachine voor de applicatie-deployment.
- **PostgreSQL 16:** Voor het veilig bewaren van persistente data is een correct gemount volume vereist in het `docker-compose.yml` bestand.
- **Interne verbindingen:**
  - *Backend → PostgreSQL:* Uitval van de database zorgt ervoor dat de backend niet meer kan loggen en gesprekken niet opgeslagen worden.
  - *Frontend → Backend:* Omdat de frontend een pure UI is zonder interne businesslogica, is de chatbot onbruikbaar indien de backend down is.
  - *Admin-dashboard → Logs:* Het dashboard functioneert alleen wanneer de loggingstabel (`request_logs`) actief en benaderbaar is.


---

## 6. Schaalbaarheid

De huidige Docker Compose architectuur is ruim voldoende voor tientallen gelijktijdige gebruikers. Mogelijke beperkingen liggen vooral bij de limieten van de Groq API en het aantal gelijktijdige PostgreSQL-connecties.

Om horizontaal te schalen, kunnen er meerdere stateless backend-instanties achter een load balancer geplaatst worden. Read-replica's kunnen worden ingezet om zware admin-dashboard queries op te vangen en de frontend kan via een Content Delivery Network (CDN) worden verspreid voor nog lagere latenties.

Verticale schaalbaarheid is mogelijk door te upgraden naar een betaald Groq-plan (voor hogere tokenlimieten) en door connection pooling toe te passen op de PostgreSQL-database. Tot slot kunnen de gebruikte Docker-images zonder dat de code aangepast hoeft te worden, worden gemigreerd naar Kubernetes om automatische schaalvergroting (Horizontal Pod Autoscaler) te faciliteren.


---

## 7. Risico's en Beperkingen

### Risicoanalyse

| Risico | Impact | Gevolg | Maatregel |
|---|---|---|---|
| Groq API onbereikbaar | Hoog | Chatbot functioneert niet meer voor onbekende LLM-vragen. | Fallback-bericht tonen; FAQ blijft gewoon werken. |
| Geen internetverbinding | Hoog | Alle LLM-aanroepen mislukken direct. | De lokale FAQ blijft basisvragen afvangen. |
| Onjuist FAQ-antwoord | Middel | Een student ontvangt foutieve informatie door een verkeerde match. | Matchingsdrempel verhogen en de FAQ secuur beheren via de admin. |
| Tokenlimiet Groq (gratis tier) | Middel | Bij piekgebruik ontstaan er "429 Too Many Requests" fouten. | Een betaald API-plan aanschaffen of rate-limiting implementeren. |
| PostgreSQL overbelasting | Laag | Het systeem wordt traag of valt uit bij extreem hoge loads. | Implementatie van connection pooling, bijvoorbeeld via PgBouncer. |

### Bekende Beperkingen

- **Antwoordlengte:** Door de configuratie `max_tokens=500` kunnen uiterst complexe vragen soms te beknopt beantwoord worden.
- **Taaloptimalisatie:** Het stopwords-filter is geoptimaliseerd voor het Nederlands. Engelstalige vragen kunnen resulteren in een suboptimale FAQ-match.
- **FAQ-onderhoud:** De effectiviteit van de chatbot valt of staat met handmatig beheer. Verouderde of slecht beheerde FAQ-entries resulteren in foutieve antwoorden voor studenten.


---

## 8. Globale Kosteninschatting

Doordat de architectuur leunt op efficiënte tooling, zijn de lopende kosten extreem laag gehouden:

| Component | Maandelijkse kosten | Opmerking |
|---|---|---|
| Groq API | €0 | Gratis tier biedt ~14.400 tokens/minuut, voldoende voor studentvolume. |
| Lokale ontwikkeling (Docker) | €0 | Geen limieten. |
| Productie hosting (Cloud VPS) | ~€5 – €20 | Bijvoorbeeld DigitalOcean of Hetzner. |
| **Totaal** | **~€0 – €20/maand** | Afhankelijk van hosting keuze. |