from sklearn.cluster import AffinityPropagation, KMeans
from sklearn.mixture import GaussianMixture

import numpy as np
import pandas as pd


# Clustering functions
def kmeans_cluster(X, n_clusters=5):
    model = KMeans(n_clusters=n_clusters).fit(X)
    # return model.labels_
    return model.cluster_centers_


def gmm_cluster(X, n_clusters=5):
    model = GaussianMixture(n_components=n_clusters).fit(X)
    return model.means_


def affinity_propagation_cluster(X, damping=0.85, batch_size=10000):
    X = pd.DataFrame(X)
    n_samples = X.shape[0]
    labels = np.empty(n_samples, dtype=int)

    # Initialize clusters for each batch separately
    start_idx = 0
    end_idx = min(batch_size, n_samples)

    # Initialize cluster centers
    cluster_centers = np.zeros((1, X.shape[1]), dtype=X.dtypes)

    # Initialize AffinityPropagation with the first batch
    model = AffinityPropagation(
        damping=damping, preference=-50
    )  # You can adjust the preference value
    model.cluster_centers_ = cluster_centers
    labels[start_idx:end_idx] = model.fit_predict(X[start_idx:end_idx])

    # Update model for subsequent batches
    for start_idx, end_idx in zip(
        range(batch_size, n_samples, batch_size),
        range(2 * batch_size, n_samples + batch_size, batch_size),
    ):
        current_batch = X[start_idx:end_idx]

        # Update cluster centers
        cluster_centers = np.vstack([cluster_centers, current_batch])
        model.cluster_centers_ = cluster_centers

        # Fit and predict on the current batch
        labels[start_idx:end_idx] = model.fit_predict(current_batch)

    return labels
