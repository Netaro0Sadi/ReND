def normalize_text(text):

    if not text:
        return ""

    return text.lower().strip()


def text_contains(text, value):

    if not text or not value:
        return False

    return normalize_text(value) in normalize_text(text)


def get_rule_based_related_questions(
    current_question,
    all_questions,
    find_question_pack,
    current_entity=None,
    current_subject=None,
    current_topic=None,
    max_results=3
):

    if not current_question:
        return []

    current_pack = find_question_pack(
        current_question
    )

    current_norm = normalize_text(
        current_question
    )

    candidates = []

    for question in all_questions:

        question_norm = normalize_text(
            question
        )

        if question_norm == current_norm:
            continue

        question_pack = find_question_pack(
            question
        )

        score = 0

        if current_entity and text_contains(
            question,
            current_entity
        ):

            score += 10

        if current_subject and text_contains(
            question,
            current_subject
        ):

            score += 6

        if current_topic and text_contains(
            question,
            current_topic
        ):

            score += 2

        if (
            current_pack
            and question_pack == current_pack
        ):

            score += 1

        if score <= 0:
            continue

        candidates.append(
            {
                "question": question,
                "pack": question_pack,
                "score": score
            }
        )

    candidates.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return [
        item["question"]
        for item in candidates[:max_results]
    ]


def get_semantic_related_questions(
    current_question,
    search_engine,
    find_question_pack,
    current_entity=None,
    current_subject=None,
    current_topic=None,
    max_results=3,
    semantic_limit=25
):

    if not current_question:
        return []

    if not search_engine:
        return []

    current_norm = normalize_text(
        current_question
    )

    current_pack = find_question_pack(
        current_question
    )

    matches = search_engine.get_top_matches(
        current_question,
        limit=semantic_limit
    )

    candidates = {}

    for match in matches:

        main_question = match.get(
            "main_question"
        )

        matched_text = match.get(
            "matched_text"
        )

        match_type = match.get(
            "type"
        )

        semantic_score = match.get(
            "score",
            0
        )

        if not main_question:
            continue

        main_norm = normalize_text(
            main_question
        )

        if main_norm == current_norm:
            continue

        if match_type == "alias":

            if normalize_text(
                matched_text
            ) == current_norm:

                continue

        question_pack = find_question_pack(
            main_question
        )

        score = semantic_score * 10

        if current_entity and text_contains(
            main_question,
            current_entity
        ):

            score += 10

        if current_subject and text_contains(
            main_question,
            current_subject
        ):

            score += 6

        if current_topic and text_contains(
            main_question,
            current_topic
        ):

            score += 2

        if (
            current_pack
            and question_pack == current_pack
        ):

            score += 1

        if score <= 0:
            continue

        existing = candidates.get(
            main_question
        )

        if (
            not existing
            or score > existing["score"]
        ):

            candidates[
                main_question
            ] = {
                "question": main_question,
                "pack": question_pack,
                "score": score
            }

    ordered = sorted(
        candidates.values(),
        key=lambda item: item["score"],
        reverse=True
    )

    return [
        item["question"]
        for item in ordered[:max_results]
    ]


def get_related_questions(
    current_question,
    all_questions,
    find_question_pack,
    current_entity=None,
    current_subject=None,
    current_topic=None,
    max_results=3,
    search_engine=None
):

    semantic_related = []

    if search_engine:

        semantic_related = get_semantic_related_questions(
            current_question=current_question,
            search_engine=search_engine,
            find_question_pack=find_question_pack,
            current_entity=current_entity,
            current_subject=current_subject,
            current_topic=current_topic,
            max_results=max_results
        )

    if semantic_related:

        return semantic_related

    return get_rule_based_related_questions(
        current_question=current_question,
        all_questions=all_questions,
        find_question_pack=find_question_pack,
        current_entity=current_entity,
        current_subject=current_subject,
        current_topic=current_topic,
        max_results=max_results
    )