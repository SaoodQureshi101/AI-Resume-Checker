from sklearn.metrics.pairwise import cosine_similarity


def compute_similarity(embedding1, embedding2):
    return cosine_similarity([embedding1], [embedding2])[0][0]
