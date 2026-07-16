# 12 - Clustering With Embeddings

## Introduction

Search (chapter 10) answers "what's relevant to this query." Clustering
answers a different question: "what groups naturally exist in this
data, with no query at all?" This is genuinely useful on its own — the
first time I ran this against a pile of incident titles with no labels
and watched it group them by root cause, it was one of the more
immediately convincing demonstrations of what embeddings are actually
good for.

## Learning Objectives

After this chapter I should be able to:

-   Explain how clustering uses the same vector space as search, for a
    different purpose.
-   Group a set of text items into clusters using k-means.
-   Interpret and label clusters after the fact.

------------------------------------------------------------------------

# From "Find Similar to This" to "Find Groups"

Search compares one query vector against many stored vectors.
Clustering compares **every vector against every other vector**, and
groups the ones that are close together — no query needed at all.

``` text
Incident titles (no labels given):
  "checkout service returning 500s"
  "payment API throwing 500 errors"
  "disk full on db-primary-02"
  "database disk usage critical"
  "login page slow to load"
  "auth service high latency"

After clustering (k=3):
  Cluster 1: "checkout service returning 500s", "payment API throwing 500 errors"
  Cluster 2: "disk full on db-primary-02", "database disk usage critical"
  Cluster 3: "login page slow to load", "auth service high latency"
```

Nobody told the algorithm these topics — it inferred them purely from
vector proximity.

## K-Means, in Plain Terms

``` text
1. Pick k (how many clusters you want)
2. Randomly place k "center" points in the vector space
3. Assign every vector to its nearest center
4. Move each center to the average position of its assigned vectors
5. Repeat steps 3-4 until centers stop moving meaningfully
```

``` python
import requests
import numpy as np
from sklearn.cluster import KMeans

def embed(text):
    r = requests.post("http://localhost:11434/api/embeddings", json={"model": "nomic-embed-text", "prompt": text})
    return r.json()["embedding"]

titles = [
    "checkout service returning 500s",
    "payment API throwing 500 errors",
    "disk full on db-primary-02",
    "database disk usage critical",
    "login page slow to load",
    "auth service high latency",
]

vectors = np.array([embed(t) for t in titles])
kmeans = KMeans(n_clusters=3, n_init="auto", random_state=42).fit(vectors)

for title, cluster_id in zip(titles, kmeans.labels_):
    print(f"cluster {cluster_id}: {title}")
```

**Platform analogy:** this is unsupervised anomaly grouping — the same
idea behind clustering metrics or log patterns to surface "these 40
alerts are probably the same underlying issue" without anyone having
pre-defined categories. Clustering finds the categories that already
exist in the data instead of requiring them to be defined upfront.

## Choosing K, and Labeling Clusters After the Fact

K-means needs `k` (the number of clusters) chosen upfront, and it
doesn't know what to *call* each cluster — that's still a human (or a
follow-up LLM call) step:

``` python
def label_cluster(client, model, titles_in_cluster: list[str]) -> str:
    prompt = f"In 3 words or fewer, what do these have in common?\n" + "\n".join(titles_in_cluster)
    r = client.chat.completions.create(model=model, messages=[{"role": "user", "content": prompt}], temperature=0)
    return r.choices[0].message.content.strip()
```

This is a nice small example of chapter 12 from module 02 (prompt
chaining) in action — clustering (an embeddings technique) handing off
to a chat model for the one thing embeddings alone can't do: naming
what it found.

## Hands-on: Cluster a Bigger, Messier Set

Take 15-20 real (or realistic) incident titles from your own work,
mixed across 3-4 genuine topics, run them through the k-means example
above with `k` set to your best guess at the topic count, and check
whether the clusters line up with how you'd have grouped them by hand.
Try `k` one higher and one lower than your guess and see how the
groupings shift.

## Common Misconceptions

❌ Clustering requires labeled training data.
(It's unsupervised — it finds structure in the data with no labels at
all, which is exactly what makes it useful for discovering categories
you didn't already know to look for.)

❌ K-means will figure out the "right" number of clusters on its own.
(`k` has to be chosen — there are techniques to help estimate a good
value (like the elbow method), but it's not fully automatic.)

✔ Clustering and search use the exact same embeddings — the difference
is entirely in what you do with the vectors afterward, not in how
they're generated.

## Interview Questions

1.  How is clustering different from semantic search, given they use
    the same underlying vectors?
2.  Walk through the basic steps of the k-means algorithm.
3.  Why can't k-means tell you what a cluster is "about"?
4.  Give a real infrastructure/ops use case for clustering text with
    no labels.

## Summary

Clustering groups embeddings by proximity with no query and no labels
required, surfacing structure that already exists in the data — the
same underlying vectors used for search, put to a different purpose.
K-means is the standard approach: pick a cluster count, assign points
to the nearest center, and iterate; labeling what each cluster
represents is a separate, usually human or LLM-assisted, step.

## Next Chapter

➡️ `13-Deduplication-With-Embeddings.md`
