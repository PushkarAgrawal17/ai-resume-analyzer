from sklearn.metrics.pairwise import cosine_similarity

def split_into_sentences(text, min_length=20):
    lines = text.split("\n")
    sentences = []
    buffer = ""

    continuations = ("and ", "or ", "with ", "using ", "the ", "a ", "an ", "to ", "of ", "in ")

    for line in lines:
        line = line.strip()
        if not line:
            if buffer and len(buffer) >= min_length:
                sentences.append(buffer)
            buffer = ""
            continue

        line_lower = line.lower()

        prev_ends_with_comma = buffer.endswith(",")
        is_continuation = line_lower.startswith(continuations)
        starts_lowercase = line and line[0].islower()

        if buffer and (prev_ends_with_comma or is_continuation or starts_lowercase):
            buffer += " " + line
        else:
            if buffer and len(buffer) >= min_length:
                sentences.append(buffer)
            buffer = line

    if buffer and len(buffer) >= min_length:
        sentences.append(buffer)

    return sentences


def get_top_matches(resume_text, jd_text, embedder, top_n=5):
    """
    Finds top matching sentence pairs between resume and JD.
    Returns a list of (resume_sentence, jd_sentence, score) tuples.
    """
    resume_sentences = split_into_sentences(resume_text)
    jd_sentences = split_into_sentences(jd_text)

    # Embed all sentences at once (faster than one by one)
    resume_embeddings = embedder.encode(resume_sentences)
    jd_embeddings = embedder.encode(jd_sentences)

    # Compute full similarity matrix (resume x jd)
    sim_matrix = cosine_similarity(resume_embeddings, jd_embeddings)

    # Collect all pairs with scores
    pairs = []
    for i, r_sent in enumerate(resume_sentences):
        for j, jd_sent in enumerate(jd_sentences):
            score = float(sim_matrix[i][j])
            pairs.append((r_sent, jd_sent, round(score * 100, 2)))

    # Sort by score descending, deduplicate on JD sentences
    pairs.sort(key=lambda x: x[2], reverse=True)

    seen_jd = set()
    unique_pairs = []
    for pair in pairs:
        jd_sent = pair[1]
        if jd_sent not in seen_jd:
            seen_jd.add(jd_sent)
            unique_pairs.append(pair)
        if len(unique_pairs) == top_n:
            break

    return unique_pairs