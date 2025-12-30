def compute_skill_overlap_score(resume_found, job_required):
    if not job_required:
        return 0.0, set()

    overlap = resume_found.intersection(job_required)

    overlap_score = len(overlap) / len(job_required)

    return overlap, round(overlap_score, 3)

def compute_combined_match_score(skill_score, tfidf_score, embed_score):
    skill_pct = skill_score * 100
    tfidf_pct = tfidf_score * 100

    final = (
        (skill_pct * 0.45) +
        (tfidf_pct * 0.25) +
        (embed_score * 0.30)
    )

    return round(final, 1)


