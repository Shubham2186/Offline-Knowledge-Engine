import re
import json
from pathlib import Path

# A small, hand-picked stopword list. Extend it if you have time.
STOPWORDS = {
    "the", "a", "an", "is", "are", "was", "were", "in", "on", "at", "of",
    "to", "and", "or", "for", "with", "this", "that", "it", "as", "by",
    "be", "from", "has", "have",
}


def tokenize(text: str) -> list:
    """
    Turn a blob of text into a list of lowercase word tokens.

    TODO (core task): this currently just lowercases + strips stopwords.
    Improve it if you have time — each of these meaningfully improves
    search quality:
      1. Basic stemming: turn "running"/"runs"/"ran" -> "run" so a
         search for "run" also matches documents that say "running".
         A cheap version: if a word ends in "ing", "ed", or "s" (and is
         longer than ~4 chars), strip the suffix.
      2. Handle hyphenated/underscored words (e.g. "machine-learning")
         by splitting them into separate tokens too.
    """
    text = text.lower()
    tokens = re.findall(r"[a-z0-9]+", text)
    tokens = [t for t in tokens if t not in STOPWORDS]
    return tokens


def process_document(filepath: Path, doc_id: int) -> dict:
    """Read one file and turn it into the standard document record."""
    text = filepath.read_text(encoding="utf-8", errors="ignore")
    tokens = tokenize(text)
    return {
        "doc_id": doc_id,
        "title": filepath.stem,
        "path": str(filepath),
        "tokens": tokens,
        "length": len(tokens),  # needed later for BM25-style normalization
    }


def process_folder(folder: str) -> list:
    """Walk a folder, process every .txt/.md file, return list of doc records."""
    docs = []
    doc_id = 0
    for filepath in sorted(Path(folder).rglob("*")):
        if filepath.suffix.lower() in (".txt", ".md"):
            docs.append(process_document(filepath, doc_id))
            doc_id += 1
    return docs


if __name__ == "__main__":
    import sys

    folder = sys.argv[1] if len(sys.argv) > 1 else "sample_docs"
    docs = process_folder(folder)
    print(f"Processed {len(docs)} documents.")
    Path("docs.json").write_text(json.dumps(docs, indent=2))
    print("Wrote docs.json -> hand this to the Database/Index engineer.")
