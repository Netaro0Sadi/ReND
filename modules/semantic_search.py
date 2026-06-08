import os
import json

os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from sentence_transformers import (
    SentenceTransformer,
    util
)


ALIASES_FILE = "data/aliases.json"
PACKS_FOLDER = "data/knowledge_packs"

print("Loading ReND semantic model...")

model = SentenceTransformer(
    "paraphrase-multilingual-MiniLM-L12-v2"
)

print("Semantic model loaded.")


def load_aliases():

    if os.path.exists(ALIASES_FILE):

        with open(
            ALIASES_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    return {}


def important_words(text):

    stopwords = {
        "what", "is", "the", "a", "an", "of", "in", "on",
        "who", "was", "were", "are", "do", "does", "did",
        "to", "for", "and", "or", "how", "many", "there",
        "tell", "me", "about", "exactly",

        "qual", "quem", "que", "o", "a", "de", "da", "do",
        "em", "no", "na", "um", "uma", "foi", "é", "e",
        "me", "fale", "sobre", "exatamente"
    }

    words = (
        text.lower()
        .replace("?", "")
        .replace(".", "")
        .replace(",", "")
        .split()
    )

    return {
        word for word in words
        if word not in stopwords
    }


def confidence_label(score):

    if score >= 0.85:
        return "high"

    if score >= 0.70:
        return "medium"

    if score >= 0.45:
        return "low"

    return "very low"


def find_question_pack(question):

    if not os.path.exists(PACKS_FOLDER):
        return None

    for file_name in os.listdir(PACKS_FOLDER):

        if not file_name.endswith(".json"):
            continue

        file_path = os.path.join(
            PACKS_FOLDER,
            file_name
        )

        try:

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            if question in data:

                return file_name.replace(
                    ".json",
                    ""
                )

        except:

            pass

    return None


class SemanticSearch:

    def __init__(self, knowledge_base):

        self.knowledge_base = knowledge_base
        self.aliases = load_aliases()

        self.last_matches = []
        self.last_successful_match = None
        self.last_question = None
        self.last_confidence = None
        self.last_answered = False

        self.update()

    def update(self):

        self.aliases = load_aliases()

        self.search_items = []

        for question in self.knowledge_base.all_questions():

            self.search_items.append(
                {
                    "text": question,
                    "main_question": question,
                    "type": "main"
                }
            )

            if question in self.aliases:

                for alias in self.aliases[question]:

                    self.search_items.append(
                        {
                            "text": alias,
                            "main_question": question,
                            "type": "alias"
                        }
                    )

        self.questions = [
            item["text"]
            for item in self.search_items
        ]

        if self.questions:

            self.embeddings = model.encode(
                self.questions,
                convert_to_tensor=True
            )

        else:

            self.embeddings = None

    def get_top_matches(
        self,
        question,
        limit=5
    ):

        if not self.questions:
            return []

        question_embedding = model.encode(
            question,
            convert_to_tensor=True
        )

        similarities = util.cos_sim(
            question_embedding,
            self.embeddings
        )[0]

        top_results = similarities.topk(
            k=min(
                limit,
                len(self.questions)
            )
        )

        matches = []

        for score, index in zip(
            top_results.values,
            top_results.indices
        ):

            item = self.search_items[
                index.item()
            ]

            score_value = score.item()

            matches.append(
                {
                    "matched_text": item["text"],
                    "main_question": item["main_question"],
                    "type": item["type"],
                    "score": score_value,
                    "confidence": confidence_label(
                        score_value
                    ),
                    "pack": find_question_pack(
                        item["main_question"]
                    )
                }
            )

        return matches

    def accepted_match(
        self,
        question,
        match
    ):

        question_words = important_words(
            question
        )

        main_words = important_words(
            match["main_question"]
        )

        matched_words = important_words(
            match["matched_text"]
        )

        common_main_words = question_words.intersection(
            main_words
        )

        common_matched_words = question_words.intersection(
            matched_words
        )

        question_entities = {
            word for word in question_words
            if len(word) > 3
        }

        matched_entities = {
            word for word in matched_words
            if len(word) > 3
        }

        main_entities = {
            word for word in main_words
            if len(word) > 3
        }

        alias_entity_overlap = question_entities.intersection(
            matched_entities
        )

        main_entity_overlap = question_entities.intersection(
            main_entities
        )

        if match["type"] == "alias":

            if match["score"] < 0.45:

                return False

            if alias_entity_overlap:

                return True

            return False

        if match["score"] >= 0.85:

            return True

        if (
            match["score"] >= 0.70
            and len(common_main_words) >= 2
        ):

            return True

        if (
            match["score"] >= 0.65
            and main_entity_overlap
        ):

            return True

        return False

    def search(
        self,
        question
    ):

        self.last_question = question
        self.last_successful_match = None
        self.last_confidence = None
        self.last_answered = False

        matches = self.get_top_matches(
            question,
            limit=5
        )

        self.last_matches = matches

        if not matches:
            return None

        self.last_confidence = matches[0][
            "confidence"
        ]

        for candidate in matches:

            if self.accepted_match(
                question,
                candidate
            ):

                self.last_successful_match = candidate
                self.last_answered = True
                self.last_confidence = candidate[
                    "confidence"
                ]

                return self.knowledge_base.get(
                    candidate["main_question"]
                )

        return None

    def explain_search(
        self,
        question,
        limit=3
    ):

        matches = self.get_top_matches(
            question,
            limit
        )

        if not matches:
            return "No knowledge available."

        result = "\nClosest matches:\n\n"

        for index, match in enumerate(
            matches,
            start=1
        ):

            result += (
                f"{index}. "
                f"{match['matched_text']} "
                f"→ {match['main_question']} "
                f"({match['type']}) "
                f"- score: {match['score']:.2f} "
                f"- confidence: {match['confidence']}\n"
            )

        return result

    def why(self):

        if not self.last_question:

            return "No search has been made yet."

        if not self.last_matches:

            return (
                "Last Match Information\n\n"
                f"Question:\n{self.last_question}\n\n"
                "No matches found."
            )

        result = "Last Match Information\n\n"

        result += (
            f"User Question:\n"
            f"{self.last_question}\n\n"
        )

        if self.last_successful_match:

            match = self.last_successful_match

            result += (
                "Selected Match:\n"
                f"{match['matched_text']}\n\n"
                "Main Question:\n"
                f"{match['main_question']}\n\n"
                f"Type: {match['type']}\n"
                f"Score: {match['score']:.2f}\n"
                f"Confidence: {match['confidence']}\n"
                f"Pack: {match['pack']}\n\n"
            )

        else:

            best_match = self.last_matches[0]

            result += (
                "Selected Match:\n"
                "None\n\n"
                "Best Rejected Match:\n"
                f"{best_match['matched_text']}\n\n"
                "Main Question:\n"
                f"{best_match['main_question']}\n\n"
                f"Type: {best_match['type']}\n"
                f"Score: {best_match['score']:.2f}\n"
                f"Confidence: {best_match['confidence']}\n"
                f"Pack: {best_match['pack']}\n\n"
            )

        result += "Top Matches:\n"

        for index, match in enumerate(
            self.last_matches,
            start=1
        ):

            result += (
                f"{index}. "
                f"{match['matched_text']} "
                f"→ {match['main_question']} "
                f"({match['type']}) "
                f"- score: {match['score']:.2f} "
                f"- confidence: {match['confidence']} "
                f"- pack: {match['pack']}\n"
            )

        return result