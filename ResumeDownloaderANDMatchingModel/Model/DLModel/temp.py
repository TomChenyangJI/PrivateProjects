from sentence_transformers import SentenceTransformer

# Load a pre-trained sentence embedding model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Example sentence
sentences = ["This is an example sentence.", "Here's another sentence."]
sentence_embeddings = model.encode(sentences)

print(len(sentence_embeddings))
print(len(sentence_embeddings[0]))
print(sentence_embeddings[0])

