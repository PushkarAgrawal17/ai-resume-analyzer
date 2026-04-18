from sentence_transformers import SentenceTransformer

# Load the model once — this is expensive, so we do it at module level
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text):
    """
    Takes a string of text.
    Returns a numerical vector (embedding) representing its meaning.
    """
    embedding = model.encode(text, convert_to_tensor=False)
    return embedding