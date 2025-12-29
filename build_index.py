import csv
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

def build_index():
    with open("docker_docs.csv", "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    texts = [r["content"] for r in rows]

    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    embeddings = model.encode(texts, show_progress_bar=True)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings.astype("float32"))

    faiss.write_index(index, "docker.index")
    with open("passages.pkl", "wb") as f:
        pickle.dump(rows, f)

    print("index built:", len(rows), "passages")

if __name__ == "__main__":
    build_index()
