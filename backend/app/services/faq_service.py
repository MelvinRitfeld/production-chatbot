import re
from typing import Optional, Dict, Any, Tuple, List

from app.data.answer_bank import FAQ_ENTRIES


class FAQService:
    def __init__(self) -> None:
        self.entries = FAQ_ENTRIES

        # Dutch + common filler words that should NOT count in matching
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
        text = re.sub(r"[^\w\s]", " ", text)      # punctuation -> space
        text = re.sub(r"\s+", " ", text).strip()  # collapse spaces
        return text

    # 2) Tokenize (remove stopwords + very short tokens)
    def _tokenize(self, text: str) -> set:
        tokens = set(text.split())
        tokens = {t for t in tokens if len(t) >= 3 and t not in self.stopwords}
        return tokens

    # 3) Score
    def _score(self, user_tokens: set, question_tokens: set, tags: List[str]) -> int:
        # meaningful overlap only
        question_overlap = len(user_tokens & question_tokens)

        tag_set = {t.lower() for t in tags} if tags else set()
        tag_overlap = len(user_tokens & tag_set)

        # weight tags a bit heavier
        return int(question_overlap + (tag_overlap * 2))

    # 4) Find best match (+score)
    def find_best_match(self, user_input: str) -> Tuple[Optional[Dict[str, Any]], int]:
        normalized_input = self._normalize(user_input)
        user_tokens = self._tokenize(normalized_input)

        # If user question has almost no meaningful tokens -> never match
        if len(user_tokens) == 0:
            return None, 0

        best_match = None
        highest_score = 0
        best_overlap = 0

        for entry in self.entries:
            q_norm = self._normalize(entry.get("question", ""))
            q_tokens = self._tokenize(q_norm)

            # Require at least 1 meaningful overlap, otherwise skip
            overlap = len(user_tokens & q_tokens)
            if overlap == 0:
                continue

            score = self._score(user_tokens, q_tokens, entry.get("tags", []))

            # Pick highest score; tie-breaker by higher overlap
            if (score > highest_score) or (score == highest_score and overlap > best_overlap):
                highest_score = score
                best_overlap = overlap
                best_match = entry

        # ✅ Threshold: stricter, so random questions don't match
        # You can tune this, but 4 is a good safe start after stopwords filtering.
        if best_match and highest_score >= 4:
            return best_match, highest_score

        return None, 0