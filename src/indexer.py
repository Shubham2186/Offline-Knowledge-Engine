import json
import hashlib
import re
from pathlib import Path


class Indexer:
    def __init__(self):
        self.inverted_index = {}
        self.documents = {}
        self.file_hashes = {}

    def tokenize(self, text):
        """Convert text into normalized words."""
        return re.findall(r"\b[a-zA-Z0-9]+\b", text.lower())

    def add_document(self, document_id, text, metadata=None):
        """Add a document or chunk to the inverted index."""
        metadata = metadata or {}

        self.documents[document_id] = {
            "text": text,
            "metadata": metadata
        }

        tokens = self.tokenize(text)

        for token in set(tokens):
            if token not in self.inverted_index:
                self.inverted_index[token] = set()

            self.inverted_index[token].add(document_id)

    def search(self, query):
        """Find documents matching the query."""
        tokens = self.tokenize(query)
        results = set()

        for token in tokens:
            results.update(
                self.inverted_index.get(token, set())
            )

        return list(results)

    def get_document(self, document_id):
        """Get stored information about a document."""
        return self.documents.get(document_id)

    def save(self, file_path):
        """Save the index to a JSON file."""
        data = {
            "inverted_index": {
                term: list(document_ids)
                for term, document_ids in self.inverted_index.items()
            },
            "documents": self.documents,
            "file_hashes": self.file_hashes
        }

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    def load(self, file_path):
        """Load an index from a JSON file."""
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.inverted_index = {
            term: set(document_ids)
            for term, document_ids
            in data.get("inverted_index", {}).items()
        }

        self.documents = data.get("documents", {})
        self.file_hashes = data.get("file_hashes", {})

    @staticmethod
    def calculate_file_hash(file_path):
        """Calculate SHA-256 hash of a file."""
        sha256 = hashlib.sha256()

        with open(file_path, "rb") as file:
            for chunk in iter(lambda: file.read(8192), b""):
                sha256.update(chunk)

        return sha256.hexdigest()

    def has_file_changed(self, file_path):
        """Check whether a file is new or has changed."""
        file_path = str(Path(file_path).resolve())

        current_hash = self.calculate_file_hash(file_path)
        old_hash = self.file_hashes.get(file_path)

        return old_hash != current_hash

    def update_file_hash(self, file_path):
        """Store the current file hash."""
        file_path = str(Path(file_path).resolve())

        self.file_hashes[file_path] = (
            self.calculate_file_hash(file_path)
        )