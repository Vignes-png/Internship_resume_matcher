from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def compute_tfidf_similarity(text1, text2):
    docs = [text1, text2]

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(docs)

    similarity = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]

    return round(float(similarity), 3)
