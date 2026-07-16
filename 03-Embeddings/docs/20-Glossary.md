# 20 - Glossary

## Introduction

Every term from this module, alphabetical, defined the way I actually
think about it, with the analogy that made it stick attached.

------------------------------------------------------------------------

**Centroid** — The average vector position of a group of embeddings,
used to represent a cluster or a labeled category more robustly than
any single example. See
[14-Classification-With-Embeddings.md](14-Classification-With-Embeddings.md).

**Chunking** — Splitting a document into smaller pieces before
embedding, so each vector represents one coherent idea instead of a
blurry average of a whole document. See
[07-Chunking-Before-Embedding.md](07-Chunking-Before-Embedding.md).

**Clustering** — Grouping embeddings by proximity with no query and no
labels, surfacing structure that already exists in the data. See
[12-Clustering-With-Embeddings.md](12-Clustering-With-Embeddings.md).

**Contrastive Training** — The training method behind most embedding
models: pulling related text pairs' vectors closer together and pushing
unrelated pairs' vectors farther apart, across millions of examples.
See
[02-How-Embedding-Models-Are-Trained.md](02-How-Embedding-Models-Are-Trained.md).

**Cosine Similarity** — A similarity metric measuring the angle between
two vectors, ignoring magnitude — the standard default for text
embedding comparison. See
[05-Similarity-Metrics.md](05-Similarity-Metrics.md).

**Dimension** — One number/axis in an embedding vector; total dimension
count drives storage size and directly affects compute cost. See
[04-Vector-Space-and-Dimensionality.md](04-Vector-Space-and-Dimensionality.md).

**Dot Product** — A similarity metric sensitive to both angle and
magnitude, sometimes preferred over cosine for models trained/
normalized specifically for it. See
[05-Similarity-Metrics.md](05-Similarity-Metrics.md).

**Embedding** — A fixed-length vector representing the meaning of a
piece of text, positioned so semantically similar text lands nearby in
vector space. See
[01-What-Are-Embeddings.md](01-What-Are-Embeddings.md).

**Embedding Drift** — The silent quality degradation that occurs when
vectors from different embedding model versions are mixed in the same
index. See
[11-Embedding-Drift-and-Model-Versioning.md](11-Embedding-Drift-and-Model-Versioning.md).

**Euclidean Distance** — The straight-line geometric distance between
two vectors — sensitive to magnitude, less commonly used for text
similarity than cosine. See
[05-Similarity-Metrics.md](05-Similarity-Metrics.md).

**Hybrid Search** — Combining semantic (embedding) search with keyword
search into one blended ranking, covering semantic search's structural
weakness on exact identifiers. See
[15-Hybrid-Search.md](15-Hybrid-Search.md).

**K-Means** — An unsupervised clustering algorithm that iteratively
assigns points to the nearest of k centers and recomputes those
centers. See
[12-Clustering-With-Embeddings.md](12-Clustering-With-Embeddings.md).

**Linear Scan** — Comparing a query vector against every stored vector
one by one — correct at any scale, fast only at small-to-medium scale.
See
[10-Building-Semantic-Search-From-Scratch.md](10-Building-Semantic-Search-From-Scratch.md).

**Nearest-Neighbor Classification** — Classifying text by comparing its
embedding to labeled example embeddings and taking the closest match's
label — a lighter-weight alternative to an LLM prompt for simple,
high-volume categorization. See
[14-Classification-With-Embeddings.md](14-Classification-With-Embeddings.md).

**Recall@K** — The fraction of eval queries where the correct document
appeared within the top k search results — the standard metric for
search quality. See
[16-Evaluating-Embedding-Quality.md](16-Evaluating-Embedding-Quality.md).

**Semantic Deduplication** — Finding near-duplicate text based on
meaning rather than exact string match, using embedding similarity
above a tuned threshold. See
[13-Deduplication-With-Embeddings.md](13-Deduplication-With-Embeddings.md).

**Semantic Search** — Retrieving documents ranked by embedding
similarity to a query, rather than by exact keyword match. See
[10-Building-Semantic-Search-From-Scratch.md](10-Building-Semantic-Search-From-Scratch.md).

------------------------------------------------------------------------

## Module Complete

That closes out all 20 chapters of **03-Embeddings**. Next up per the
[root README](../../README.md) roadmap:

➡️ `04-Vector-Databases`
