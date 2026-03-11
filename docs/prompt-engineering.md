# Prompt Ontwerp & Analyse

**Project:** UNASAT Campus Support Chatbot  
**Vak:** Productieklare Chatbot  
**Opleiding:** Bachelor ICT — UNASAT Business School  
**Jaar:** 2025-2026

---

## Inhoudsopgave

- A. Rol van Prompt Engineering in de Use Case
- B. Prompt-Ecosysteem (Gebruiker, Context, Model, Output)
- C. Prompttypes en Ontwerpkeuzes
- D. Promptcyclus & Iteratie
- E. Kwaliteit & Robuustheid van Prompts

---

## A. Rol van Prompt Engineering in de Use Case

*(Beoordelingscategorie: Functionele waarde & probleemdefinitie)*

### A.1 Beschrijving van het probleem en doel

UNASAT (Universiteit van Suriname) heeft een grote, diverse studentenpopulatie die regelmatig directe vragen heeft over campus- en onderwijsgerelateerde zaken. Vaak wenden studenten zich tot de administratie voor informatie over inschrijvingen, roosters, Microsoft Teams, toetsen en studiekosten. Dit resulteert in een hoge werkdruk voor het personeel en lange wachttijden voor de studenten.

De UNASAT Campus Support Chatbot is ontwikkeld om dit op te lossen door 24/7 direct antwoord te geven op veelgestelde vragen. Het systeem maakt gebruik van een hybride architectuur: een FAQ-matching systeem voor bekende vragen en een Large Language Model (LLM) als fallback voor onbekende, complexere vragen. Het doel is het ontlasten van de administratie en het verbeteren van de studentervaring door razendsnelle reacties (<10ms voor FAQ, ~500ms voor LLM) en consistente communicatie.

### A.2 Doel van de AI-ondersteuning

Zonder doordacht prompt-ontwerp zou de chatbot onbruikbaar zijn. Prompt engineering voorkomt dat het systeem:

- Buiten scope antwoorden geeft (bijv. over onderwerpen buiten UNASAT).
- In de verkeerde taal communiceert, zoals Engels in plaats van Nederlands.
- Informatie gaat hallucineren over data, bedragen of namen.
- Een onprofessionele toon aanslaat.

Door middel van een strakke system prompt, instroomregels en gestructureerde FAQ-matching, borgt prompt engineering de effectiviteit en veiligheid van elke gegenereerde respons.

---

## B. Prompt-Ecosysteem (Gebruiker, Context, Model, Output)

*(Beoordelingscategorie: Architectuur & techniek)*

### B.1 Overzicht van het ecosysteem

Het ecosysteem beschrijft hoe de vier kerncomponenten van het systeem elkaar continu beïnvloeden om tot een kwalitatieve output te komen.

| Component | Beschrijving |
|---|---|
| **Gebruiker** | UNASAT-studenten die Nederlandstalig zijn en een wisselend kennisniveau hebben. Zij stellen directe, vrije tekstvragen over de campus en het onderwijs en hebben geen technische achtergrond. |
| **Context** | Bestaat uit twee lagen: de FAQ-kennisbank biedt gestructureerde antwoorden op bekende vragen. Voor onbekende vragen instrueert de system prompt het model over zijn rol, het taalgebruik, de beperkingen en het gewenste gedrag. |
| **Model** | De applicatie gebruikt de Groq API met het llama-3.3-70b-versatile model. Dit is specifiek gekozen vanwege de extreem lage latency (<500ms), de beschikbare gratis tier en sterke meertalige (Nederlandse) capaciteiten. |
| **Output** | Korte, feitelijke antwoorden in het Nederlands van maximaal 3 zinnen. De toon is professioneel en vriendelijk, met een harde fallback naar info@unasat.sr als het antwoord onzeker is. |

### Onderlinge beïnvloeding

Wanneer de gebruiker een vraag stelt, wordt de input genormaliseerd, getokenized en vergeleken met de context (FAQ). Bij een hoge match-score (>= 4) wordt direct een output gegenereerd zonder LLM. Is er geen match, dan stuurt de context (System Prompt) samen met de gebruikersvraag het model (LLM) aan. Parameters zoals `max_tokens=500` en `temperature=0.5` sturen de output aan om voorspelbaar en veilig te blijven.

---

## C. Prompttypes en Ontwerpkeuzes

*(Beoordelingscategorie: Promptontwerp)*

Voor dit systeem zijn drie specifieke prompttypes ontworpen, elk met een uniek doel binnen de architectuur.

### C.1 Role-Based System Prompt

**Doel:** De identiteit, contextuele grenzen en gedragsregels van de chatbot onomstotelijk vastleggen.

**Type prompt:** Role-based prompt (systeem-niveau).

**Verwachte output:** Nederlandstalige, feitelijke, korte antwoorden (max 3 zinnen) over specifieke UNASAT-onderwerpen.

**Implementatie & Onderbouwing:** Het model krijgt de rol "studentenassistent van UNASAT" om out-of-scope gedrag te voorkomen. Expliciete instructies over onderwerpen (Teams, OneDrive, SHL) en de regel om bij twijfel altijd te verwijzen naar info@unasat.sr elimineren de kans op hallucinaties van bedragen of data.

---

### C.2 Instruction Prompt (Algoritmische FAQ Matching)

**Doel:** Gebruikersvragen matchen met de juiste, vooraf gedefinieerde FAQ-entry.

**Type prompt:** Instruction prompt (algoritmisch/impliciet format).

**Verwachte output:** Het FAQ-antwoord met de hoogste tokenscore, mits >= 4.

**Implementatie & Onderbouwing:** De vraag wordt genormaliseerd (leestekens weg, stopwords eruit). Er is gekozen voor een dynamische weging waarbij specifieke "tags" (zoals `teams` of `inschrijving`) dubbel tellen. De drempelwaarde van 4 is bewust gekozen om fout-positieve matches bij vage vragen te voorkomen.

---

### C.3 Few-Shot Fallback Prompt

**Doel:** Het model sturen in de exacte opmaak en structuur wanneer een vraag via de LLM (buiten de FAQ om) beantwoord moet worden.

**Type prompt:** Few-shot prompt gecombineerd met user-input.

**Verwachte output:** Een veilig antwoord dat exact de opmaak volgt van de gegeven voorbeelden.

**Implementatie & Onderbouwing:** Om te garanderen dat de "maximaal 3 zinnen" regel echt gerespecteerd wordt bij complexe vragen, worden er in de achtergrond twee voorbeeldinteracties (Q&A's) meegegeven aan het LLM via de Groq API. Dit verhoogt de betrouwbaarheid en zorgt voor een consistente tone of voice. Parameters `max_tokens=500` en `temperature=0.5` zorgen voor een goede balans tussen efficiëntie en een natuurlijke, maar niet te creatieve (hallucinerende) output.

---

## D. Promptcyclus & Iteratie

*(Beoordelingscategorie: Vibe coding & verbeteren)*

Om tot een robuust systeem te komen, zijn de kernprompts iteratief ontwikkeld. Hieronder de analyse van minimaal twee iteratiecycli per prompt.

### D.1 Iteratie: System Prompt

| Fase | Inhoud |
|---|---|
| **Versie 1 (prompt)** | `"Je bent een assistent van UNASAT. Beantwoord vragen van studenten."` |
| **Output v1** | `"The first year costs $2,000..."` (Engels, bedrag verzonnen) |
| **Analyse** | Geen taalregel, geen scope-beperking. Het model hallucineerde en wisselde van taal. |
| **Versie 2 (prompt)** | Toegevoegd: `"Antwoord altijd in het Nederlands"` en `"Verzin geen informatie..."` |
| **Output v2** | `"Voor specifieke informatie raad ik je aan..."` (correct Nederlands, geen verzonnen bedrag) |
| **Analyse** | Veiligheid en taal waren opgelost, maar antwoorden werden soms omslachtig en te lang voor een chat-interface. |
| **Versie 3 (prompt)** | Toegevoegd: `"Wees kort en duidelijk (max 3 zinnen)"` en specifieke fallback naar info@unasat.sr |
| **Output v3** | Beknopt, direct antwoord van maximaal 3 zinnen met de juiste contactgegevens. |
| **Analyse** | Deze iteratie bracht de prompt naar productie-kwaliteit. |

---

### D.2 Iteratiecyclus: FAQ Instruction Matching

| Fase | Inhoud |
|---|---|
| **Versie 1 (logica)** | Match drempelwaarde ingesteld op score >= 2 |
| **Output v1** | Op input `"Ik heb een vraag"`: verkeerde FAQ getriggerd over "benodigde literatuur" |
| **Analyse** | De drempel was te laag, wat leidde tot fout-positieven op basis van stopwoorden en vage zinnen. |
| **Versie 2 (logica)** | Drempelwaarde verhoogd naar score >= 4 en tags tellen dubbel |
| **Output v2** | Op input `"Ik heb een vraag"`: geen FAQ match (score 1), correct doorgestuurd naar LLM |
| **Analyse** | Fout-positieven verholpen, maar algemene Nederlandse lidwoorden (`de`, `het`, `een`) vervuilden scores nog steeds lichtelijk. |
| **Versie 3 (logica)** | Integratie van Dutch stopwords filtering vóór de tokenisatie |
| **Output v3** | Extreem zuivere matching, uitsluitend gebaseerd op de semantische kern van de vraag. |
| **Analyse** | Het systeem is nu uiterst accuraat en robuust. |

---

## E. Kwaliteit & Robuustheid van Prompts

*(Beoordelingscategorie: Kwaliteit & Evaluatie)*

De prompts en het ecosysteem scoren als volgt op de belangrijkste kwaliteitscriteria:

- **Effectiviteit (Goed):** De gestructureerde system prompt zorgt ervoor dat de LLM-fallback zinvolle en veilige antwoorden genereert op onbekende vragen, terwijl de FAQ-matching bekende vragen feilloos afvangt.
- **Efficiëntie (Excellent):** Door de FAQ-query als "first line of defense" te gebruiken (kosten: gratis, latency: <10ms) wordt de API enorm ontlast. LLM-aanroepen zijn hard gelimiteerd op `max_tokens=500`, wat zowel kosten als wachttijden minimaliseert.
- **Consistentie (Goed):** De restricties op taal (Nederlands), toon (professioneel) en lengte (max 3 zinnen) zorgen voor een uniforme gebruikerservaring, ongeacht of het antwoord uit de FAQ of het LLM komt.
- **Foutgevoeligheid & Veiligheid (Goed):** Lege inputs worden direct afgevangen (0 tokens = geen match). API-fouten resulteren in een elegante fallback-boodschap in plaats van een crash. De strikte roldefinitie verkleint het risico op prompt-injections.

### Geïmplementeerde beveiligingsmaatregelen

De volgende maatregelen zijn reeds actief in het systeem:

1. **Rate Limiting** — 20 verzoeken per 60 seconden per IP-adres, beschermt tegen spam en API-misbruik.
2. **Prompt Injection detectie** — invoer wordt gescreend op 9 aanvalspatronen (o.a. `"ignore all previous instructions"`). Geblokkeerde berichten worden gelogd en krijgen een veilige fallback.
3. **Periodieke FAQ-analyse** — ongematchte vragen worden gelogd in `request_logs` zodat gaten in de kennisbank wekelijks geïdentificeerd en aangevuld kunnen worden.

---

*Einde document — UNASAT Campus Support Chatbot — Prompt Engineering*