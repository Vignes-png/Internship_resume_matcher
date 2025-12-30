from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def compute_embedding_similarity(resume_text, job_text):

    # safety check
    if not resume_text.strip() or not job_text.strip():
        return 0.0

    resume_emb = model.encode(resume_text)
    job_emb = model.encode(job_text)

    sim = cosine_similarity(
        [resume_emb],
        [job_emb]
    )[0][0]

    # convert to percentage
    return round(float(sim * 100), 2)
