import requests
from bs4 import BeautifulSoup
import csv

URLS = [
    "https://docs.docker.com/build/",
    "https://docs.docker.com/build/guide/",
]

def crawl():
    passages = []
    for url in URLS:
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.content, "html.parser")
        main = soup.find("main") or soup.body
        for p in main.find_all(["p", "h2", "h3"]):
            text = p.get_text(strip=True)
            if len(text) > 50:
                passages.append(
                    {"content": text, "source_url": url, "version": "latest"}
                )
    with open("docker_docs.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["content", "source_url", "version"])
        writer.writeheader()
        writer.writerows(passages)
    print("saved", len(passages), "rows")

if __name__ == "__main__":
    crawl()
