from providers.embedding_provider import get_embeddings

embedding_model = get_embeddings()

embedding = embedding_model.embed_query(
    "How many sick leaves are available?"
)

print("Embedding size:", len(embedding))
print(embedding[:10])