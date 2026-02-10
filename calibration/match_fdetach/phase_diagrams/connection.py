""""
Some functions for handling cell connections.
=============================================
Create by Wei Wang, 2025.
"""

import numpy as np

# for computing connected components
from scipy.sparse.csgraph import connected_components
from scipy.sparse import csr_matrix


def rebuild_connection_matrix(N, connect):
    i, j = connect[:, 0], connect[:, 1]
    rows = np.concatenate([i, j])
    cols = np.concatenate([j, i])
    data = np.ones(len(rows), dtype=bool)
    connect_matrix = csr_matrix((data, (rows, cols)), shape=(N, N))

    return connect_matrix


def select_daughter_cluster(N, connect):
    """Select a daughter cluster randomly from the connected components."""
    n_components, labels = connected_components(csgraph=rebuild_connection_matrix(N, connect), directed=False)

    # Randomly select a daughter cluster
    if n_components > 1:
        selected_idx = np.random.randint(n_components)
        selected_cells = np.where(labels == selected_idx)[0]
        N = len(selected_cells)

        selected_mask = np.isin(connect[:, 0], selected_cells) & np.isin(connect[:, 1], selected_cells)
        selected_connect = connect[selected_mask]

        # Use searchsorted to map global → local index
        selected_connect_local = np.searchsorted(selected_cells, selected_connect)

        return selected_cells, N, selected_connect_local
    else:
        return None, N, connect


def get_cluster_sizes(N, connect):
    n_components, labels = connected_components(csgraph=rebuild_connection_matrix(N, connect), directed=False)

    cluster_sizes = np.bincount(labels)
    
    return cluster_sizes, n_components, labels
