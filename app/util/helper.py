from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
def text_to_vector(text):
    vector = model.encode(text)
    return vector.tolist()