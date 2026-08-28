# Knowledge Search

A lightweight, zero-dependency local document search tool.

The project allows users to index documents from a directory and search them using text queries. The system reads and processes documents, creates an inverted index, ranks matching results, and displays relevant snippets through a command-line interface.

## Project Goal

The basic flow of the project is:

```text
Documents
    |
    v
Document Ingestion
    |
    v
Cleaning and Chunking
    |
    v
Index and Storage
    |
    v
Search and Ranking
    |
    v
CLI
    |
    v
Search Results
```

For example:

```bash
knowledge index ./notes
```

After indexing, users can search:

```bash
knowledge search "deadlock prevention"
```

The command should return the most relevant documents or chunks along with useful snippets.

## Team Roles

### T1 - Document Ingestion

T1 handles the document ingestion part of the project.

Responsibilities:

* Find supported files in the given directory.
* Read and extract text from files.
* Clean and normalize the text.
* Split large documents into smaller chunks.
* Keep basic metadata such as file name and path.
* Handle unsupported files and file-reading errors.
* Provide clean and structured document data to T3.

Flow:

```text
Files
  |
  v
File Discovery
  |
  v
Text Extraction
  |
  v
Text Cleaning
  |
  v
Chunking
  |
  v
Structured Document Data
  |
  v
T3
```

Input:

```text
Directory containing documents
```

Output:

```text
Clean document chunks with metadata
```

### T2 - Search and Ranking

T2 handles query processing, searching and ranking.

Responsibilities:

* Process the user's search query.
* Normalize and tokenize the query.
* Search the index created by T3.
* Find matching documents or chunks.
* Calculate relevance scores.
* Rank the results.
* Return the top results.
* Generate useful snippets.

Flow:

```text
User Query
    |
    v
Query Processing
    |
    v
Index Lookup
    |
    v
Matching Results
    |
    v
Relevance Scoring
    |
    v
Ranking
    |
    v
Top Results and Snippets
```

### T3 - Index and Storage

T3 handles the inverted index and persistent storage.

Responsibilities:

* Receive processed document data from T1.
* Build the inverted index.
* Maintain mappings between terms and documents/chunks.
* Save the index to disk.
* Load the index when required.
* Detect file changes using hashing or another suitable method.
* Avoid unnecessary re-indexing.
* Provide the required data/interface to T2.

Example:

Documents:

```text
doc1 = "deadlock prevention"
doc2 = "deadlock detection"
doc3 = "memory management"
```

Inverted index:

```text
deadlock     -> doc1, doc2
prevention   -> doc1
detection    -> doc2
memory       -> doc3
management   -> doc3
```

### T4 - CLI, Testing and Integration

T4 handles the command-line interface, testing and integration of the complete project.

Responsibilities:

* Implement the CLI commands.
* Connect T1, T2 and T3.
* Test individual modules.
* Perform integration testing.
* Handle user-facing errors.
* Prepare documentation and README.
* Prepare the final demo.
* Check the final submission.

Main commands:

```bash
knowledge index ./notes
```

```bash
knowledge search "deadlock prevention"
```

## System Architecture

```text
                 User
                  |
                  v
             +---------+
             |   T4    |
             |   CLI   |
             +----+----+
                  |
          +-------+-------+
          |               |
          v               v
     +---------+      +---------+
     |   T1    |      |   T2    |
     | Ingest  |      | Search  |
     +----+----+      +----+----+
          |                |
          v                |
     +---------------------+
     |         T3          |
     |  Index and Storage  |
     +---------------------+
```

## Suggested Project Structure

```text
knowledge-search/
|
+-- src/
|   +-- ingest.py
|   +-- indexer.py
|   +-- search.py
|   +-- cli.py
|
+-- tests/
|   +-- test_ingest.py
|   +-- test_indexer.py
|   +-- test_search.py
|   +-- test_cli.py
|
+-- data/
|   +-- sample_documents/
|
+-- README.md
+-- .gitignore
```

The final structure can be changed if required during development.

## Module Interfaces

The team should agree on the interfaces between modules before implementation.

### T1 to T3

T1 should provide information such as:

```text
Document ID
File path
File name
Chunk ID
Cleaned text
Metadata
```

Conceptually:

```text
Document
  |
  +-- id
  +-- path
  +-- name
  +-- chunk_id
  +-- text
```

### T3 to T2

T3 should provide the information needed by T2 for searching.

For example:

```text
Term -> Matching document/chunk IDs
```

T2 can then use these results for scoring and ranking.

### T2 to T4

T2 should return structured search results containing information such as:

```text
Document name
Document path
Chunk information
Relevance score
Snippet
```

T4 will format these results for the CLI.

## MVP

The first goal is to get the complete basic pipeline working.

```text
Documents
    |
    v
T1
    |
    v
Clean Text
    |
    v
T3
    |
    v
Inverted Index
    |
    v
T2
    |
    v
Search and Ranking
    |
    v
T4
    |
    v
CLI Results
```

The MVP is complete when these commands work:

```bash
knowledge index ./notes
```

and:

```bash
knowledge search "deadlock prevention"
```

The system should return relevant results for the query.

## Development Plan

### Phase 1 - Basic MVP

* File discovery
* Text extraction
* Text cleaning
* Chunking
* Inverted index
* Basic search
* Basic ranking
* CLI

### Phase 2 - Reliability

* Error handling
* Empty files
* Unsupported files
* Invalid queries
* Missing index
* Duplicate documents

### Phase 3 - Performance

* Persistent index
* Efficient lookups
* File hashing
* Incremental indexing
* Avoid unnecessary re-processing

### Phase 4 - Search Improvements

* Better tokenization
* Better relevance scoring
* Improved ranking
* Better snippets
* Multi-word queries

### Phase 5 - Final Polish

* Clean CLI output
* Testing
* Documentation
* Demo dataset
* Performance testing
* Final README
* Submission preparation

## Testing

Each module should be tested separately before integration.

### T1 Tests

Test cases:

* Valid supported file
* Empty file
* Multiple files
* Nested directories
* Unsupported file
* File-reading error
* Large document
* Text containing punctuation
* Repeated whitespace

### T3 Tests

Test:

* Index creation
* Multiple terms
* Multiple documents
* Duplicate terms
* Empty documents
* Index persistence
* Loading an existing index
* File change detection
* Re-indexing changed files

### T2 Tests

Test:

* Single-word query
* Multi-word query
* Unknown query
* Empty query
* Multiple matching documents
* Ranking order
* Snippet generation

### T4 Tests

Test:

```bash
knowledge index ./notes
knowledge search "deadlock"
```

Also test:

* Invalid commands
* Missing directories
* Missing index
* Empty queries
* Queries with no results

## Git Workflow

Each team member should work on their own branch.

Example:

```bash
git checkout -b feature/t1-ingestion
```

Other branches can follow the same pattern:

```text
feature/t2-search
feature/t3-indexer
feature/t4-cli
```

Recommended workflow:

```text
Create Branch
     |
     v
Implement
     |
     v
Test
     |
     v
Commit
     |
     v
Push
     |
     v
Pull Request
     |
     v
Review
     |
     v
Merge
```

Avoid pushing unfinished work directly to the main branch.

## Pre-Hackathon Rules

Before the official hackathon starts, the team should not write or commit the actual implementation.

Allowed before kickoff:

* Read the reference files.
* Understand the architecture.
* Study `ingest.py`, `search.py`, `indexer.py` and `cli.py`.
* Design functions and interfaces.
* Create the GitHub repository.
* Create folders and branches if allowed.
* Write pseudocode.
* Prepare test cases.
* Discuss the architecture.
* Study Python standard-library documentation.

Not allowed before kickoff:

* Copying the reference implementation.
* Using the reference implementation as the final submission.
* Writing or committing the actual project implementation.
* Adding unnecessary dependencies.

The `files.zip` provided by Claude is only a reference or skeleton. It should be used to understand the expected direction of the project, not copied directly into the final submission.

## Zero Dependency

The project should avoid external dependencies unless they are explicitly allowed by the hackathon rules.

Python's standard library should be preferred where possible.

Possible modules include:

```text
pathlib
os
re
json
hashlib
argparse
collections
math
```

The final list of modules will depend on the implementation.

## Team Coordination

The main goal is to keep the interfaces between the four modules clear.

T1 and T3 should agree on the document and chunk data format.

T2 and T3 should agree on the index structure and search interface.

T2 and T4 should agree on the search result format and CLI output.

T4 should make sure that all modules work together before the final submission.

## Definition of Done

The project is ready for submission when:

* [ ] Supported documents can be discovered.
* [ ] Documents can be read successfully.
* [ ] Text can be cleaned and chunked.
* [ ] The inverted index can be created.
* [ ] The index can be saved and loaded.
* [ ] Search queries work.
* [ ] Results are ranked.
* [ ] Useful snippets are displayed.
* [ ] CLI commands work.
* [ ] Errors are handled properly.
* [ ] Tests pass.
* [ ] All modules are integrated.
* [ ] README is complete.
* [ ] The project works from a clean environment.
* [ ] No unnecessary dependencies are used.
* [ ] Final code has been reviewed by the team.

## Final Goal

The final system should provide a simple local document search experience:

```text
Documents
    |
    v
Ingestion
    |
    v
Indexing
    |
    v
Search
    |
    v
Ranking
    |
    v
CLI
    |
    v
Relevant Results
```

The priority is to get the MVP working first and then improve performance, search quality, reliability and user experience.
