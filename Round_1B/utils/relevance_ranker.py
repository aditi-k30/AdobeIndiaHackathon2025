from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def rank_sections(sections, persona_job):
    query_text = (persona_job.get("persona", "") + " " + persona_job.get("job_to_be_done", "")).strip()
    if not query_text:
        return sections

    corpus = [sec["text"] for sec in sections]

    vectorizer = TfidfVectorizer(stop_words='english', max_features=10000)
    tfidf_matrix = vectorizer.fit_transform(corpus)
    query_vec = vectorizer.transform([query_text])

    sim_scores = cosine_similarity(query_vec, tfidf_matrix).flatten()

    for idx, score in enumerate(sim_scores):
        sections[idx]["relevance_score"] = float(score)
    ranked = sorted(sections, key=lambda x: x["relevance_score"], reverse=True)
    return ranked
