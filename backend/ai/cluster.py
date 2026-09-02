import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import AgglomerativeClustering
import numpy as np


class ThemeClusterer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words="english")

    def generate_embeddings(self, texts: list[str]) -> np.ndarray:
        return self.vectorizer.fit_transform(texts).toarray()

    def cluster_records(self, records: list[dict]) -> list[list[dict]]:
        if not records:
            return []

        # 1. Prepare texts for embedding
        texts = []
        for r in records:
            theme_cand = r.get("theme") or ""
            pain = r.get("purchase_barrier") or ""
            norm_text = r.get("text") or ""

            # Combine signals to give clustering algorithm semantic meat
            combined = f"Theme: {theme_cand}. Pain: {pain}. Text: {norm_text}"
            texts.append(combined)

        # 2. Get Embeddings
        print(f"Generating embeddings for {len(texts)} records...")
        embeddings = self.generate_embeddings(texts)

        # 3. Determine dynamic number of clusters
        # Since we have tiny data (e.g. 20 records), we shouldn't force 10 clusters.
        # We dynamically scale: max 3 clusters if < 10 records, else around len//5 up to 12.
        n_clusters = max(3, min(12, len(records) // 4))

        if len(records) <= n_clusters:
            n_clusters = max(1, len(records) // 2)

        print(f"Clustering into {n_clusters} clusters...")
        clustering = AgglomerativeClustering(
            n_clusters=n_clusters, metric="cosine", linkage="average"
        )
        labels = clustering.fit_predict(embeddings)

        # 4. Group records by cluster label
        clusters_dict = {}
        for idx, label in enumerate(labels):
            if label not in clusters_dict:
                clusters_dict[label] = []
            clusters_dict[label].append(records[idx])

        return list(clusters_dict.values())
