import faiss
import pickle
from sentence_transformers import SentenceTransformer

class DocRetriever:
    def __init__(self):
        self.index = faiss.read_index("docker.index")
        with open("passages.pkl", "rb") as f:
            self.passages = pickle.load(f)
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    def search(self, query, top_k=3):
        q_emb = self.model.encode([query])
        D, I = self.index.search(q_emb.astype("float32"), top_k)
        results = []
        for idx, dist in zip(I[0], D[0]):
            p = self.passages[idx]
            results.append(
                {
                    "content": p["content"],
                    "url": p["source_url"],
                    "score": float(1 / (1 + dist)),
                }
            )
        return results

if __name__ == "__main__":
    r = DocRetriever()
    res = r.search("Docker BuildKit")
    for i, item in enumerate(res, 1):
        print(f"[{i}] {item['score']:.3f} {item['url']}")
        print(item["content"][:200], "\n")
