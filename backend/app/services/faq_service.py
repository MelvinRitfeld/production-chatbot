import re
import os
from typing import Optional, Dict, Any, Tuple, List
from groq import Groq
from app.data.answer_bank import FAQ_ENTRIES

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """Je bent een behulpzame studentenassistent van UNASAT (Universiteit van Suriname). 
Je helpt studenten met vragen over inschrijving, roosters, toetsen, studiebegeleiding, 
Microsoft Teams, OneDrive, SHL en algemene campusinformatie.

Regels:
- Antwoord altijd in het Nederlands
- Wees kort en duidelijk (max 3 zinnen)
- Als je het antwoord niet zeker weet, verwijs naar info@unasat.sr
- Verzin geen informatie over specifieke data, bedragen of namen
- Blijf altijd vriendelijk en professioneel"""


class FAQService:
    def __init__(self) -> None:
        self.entries = FAQ_ENTRIES

        self.stopwords = {
            "de", "het", "een", "en", "of", "van", "voor", "naar", "op", "in", "aan", "bij", "met", "zonder",
            "ik", "jij", "je", "u", "uw", "wij", "we", "jullie", "ze", "zij", "mijn", "mij", "me",
            "wat", "waar", "wanneer", "hoe", "wie", "welke", "welk", "waarom",
            "is", "zijn", "was", "waren", "word", "wordt", "kun", "kan", "kunnen", "moet", "moeten",
            "heb", "hebt", "heeft", "hebben", "doe", "doen", "gaat", "gaan",
            "dat", "dit", "deze", "die", "daar", "hier", "er",
            "als", "dan", "maar", "ook", "nog", "niet", "wel",
            "tot", "t/m", "om", "via",
        }

    # 1) Normalize
    def _normalize(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r"[^\w\s]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    # 2) Tokenize
    def _tokenize(self, text: str) -> set:
        tokens = set(text.split())
        tokens = {t for t in tokens if len(t) >= 3 and t not in self.stopwords}
        return tokens

    # 3) Score
    def _score(self, user_tokens: set, question_tokens: set, tags: List[str]) -> int:
        question_overlap = len(user_tokens & question_tokens)
        tag_set = {t.lower() for t in tags} if tags else set()
        tag_overlap = len(user_tokens & tag_set)
        return int(question_overlap + (tag_overlap * 2))

    # 4) Find best FAQ match
    def find_best_match(self, user_input: str) -> Tuple[Optional[Dict[str, Any]], int]:
        normalized_input = self._normalize(user_input)
        user_tokens = self._tokenize(normalized_input)

        if len(user_tokens) == 0:
            return None, 0

        best_match = None
        highest_score = 0
        best_overlap = 0

        for entry in self.entries:
            q_norm = self._normalize(entry.get("question", ""))
            q_tokens = self._tokenize(q_norm)

            overlap = len(user_tokens & q_tokens)
            if overlap == 0:
                continue

            score = self._score(user_tokens, q_tokens, entry.get("tags", []))

            if (score > highest_score) or (score == highest_score and overlap > best_overlap):
                highest_score = score
                best_overlap = overlap
                best_match = entry

        if best_match and highest_score >= 4:
            return best_match, highest_score

        return None, 0

    # 5) LLM fallback via Groq
    def llm_fallback(self, user_input: str) -> str:
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=200,
                temperature=0.5,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return "Ik kan je vraag momenteel niet beantwoorden. Neem contact op via info@unasat.sr."

    # 6) Main entry point
    def get_answer(self, user_input: str) -> Tuple[str, str]:
        """Returns (answer, source) where source is 'faq' or 'llm'"""
        match, score = self.find_best_match(user_input)
        if match:
            return match["answer"], "faq"
        
        llm_answer = self.llm_fallback(user_input)
        return llm_answer, "llm"