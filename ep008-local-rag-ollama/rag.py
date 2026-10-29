# rag.py: chat with a PDF, 100% local (Ollama + pypdf)
# usage: python rag.py file.pdf "your question"
import sys, os, re, json, time
import ollama
from pypdf import PdfReader

EMBED, CHAT = "nomic-embed-text", "llama3.2:3b"
pdf, question = sys.argv[1], sys.argv[2]
index_file = pdf + ".index.json"

def chunks(path, size=800, overlap=150):
    for n, page in enumerate(PdfReader(path).pages, 1):
        text = " ".join((page.extract_text() or "").split())
        for i in range(0, len(text), size - overlap):
            piece = text[i:i + size]
            if len(piece) > 100:
                yield {"page": n, "text": piece}

# 1. INDEX (once): split the PDF, embed every chunk, save to disk
if not os.path.exists(index_file):
    t = time.time()
    docs = list(chunks(pdf))
    for i in range(0, len(docs), 32):
        batch = docs[i:i + 32]
        vecs = ollama.embed(model=EMBED, input=["search_document: " + d["text"] for d in batch])["embeddings"]
        for d, v in zip(batch, vecs):
            d["vec"] = v
    json.dump(docs, open(index_file, "w"))
    print(f"indexed {len(docs)} chunks in {time.time() - t:.0f} s")
docs = json.load(open(index_file))

# 2. RETRIEVE: embed the question, keep the 4 closest chunks
t = time.time()
q = ollama.embed(model=EMBED, input="search_query: " + question)["embeddings"][0]
rare = [w for w in set(re.findall(r"\w{4,}", question.lower()))
        if sum(w in d["text"].lower() for d in docs) < len(docs) * 0.02]   # rare words, like names
score = lambda d: sum(a * b for a, b in zip(d["vec"], q)) + 0.1 * sum(w in d["text"].lower() for w in rare)
top = sorted(docs, key=score, reverse=True)[:4]

# 3. GENERATE: answer only from those chunks, cite the page
context = "\n\n".join(f"[page {d['page']}] {d['text']}" for d in top)
prompt = ("Answer using ONLY the context below. Give the complete answer, "
          "then quote the exact sentence you used and its page number. "
          "If the answer is not in the context, say you don't know.\n\n"
          f"Context:\n{context}\n\nQuestion: {question}")
for part in ollama.chat(model=CHAT, messages=[{"role": "user", "content": prompt}], stream=True):
    print(part["message"]["content"], end="", flush=True)
print(f"\n\nsources: {', '.join('p.' + str(d['page']) for d in top)}  ({time.time() - t:.1f} s)")
