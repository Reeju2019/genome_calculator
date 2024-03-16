import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

img_path = "./Data/image"
color = ["red", "blue", "green", "purple", "black"]
labels = ["Aves", "Crustacea", "Mammalia", "Molusca", "Osteichthyes"]


# Plotting functions
def plot_clusters(X, y, labels, algorithm):
    xs = [x[0] for x in X]
    ys = [x[1] for x in X]

    # 2D scatter plot
    plt.figure(figsize=(8, 6))
    plt.scatter(xs, ys, s=2, c=labels, cmap="viridis")
    # plt.scatter(xs, ys, c=y, cmap="viridis")
    plt.title(f"{algorithm} - 2D Plot")
    plt.xlabel("Feature 1")
    plt.ylabel("Feature 2")
    plt.savefig(f"{img_path}/{algorithm.lower()}_plot_2d.png")
    plt.close()

    # 3D scatter plot
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")
    zs = [x[2] for x in X]
    ax.scatter(xs, ys, zs, s=2, c=labels, cmap="viridis")
    # ax.scatter(xs, ys, zs, c=y, cmap="viridis")
    ax.set_title(f"{algorithm} - 3D Plot")
    ax.set_xlabel("Feature 1")
    ax.set_ylabel("Feature 2")
    ax.set_zlabel("Feature 3")
    plt.savefig(f"{img_path}/{algorithm.lower()}_plot_3d.png")
    plt.close()

    return True


def plot_clusters_2d(x, labels=labels, colorSet=color, algorithm=""):
    try:
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111)
        for index, data in enumerate(x):
            x2d = [i[0] for i in data]
            y2d = [i[1] for i in data]
            ax.scatter(x2d, y2d, c=colorSet[index], label=labels[index], cmap="viridis")
        ax.set_xlabel("ENC")
        ax.set_ylabel("GC3")
        ax.legend(loc="best")
        plt.title(f"{algorithm} - 2D Plot")
        plt.savefig(f"{img_path}/{algorithm.lower()}_plot_2d.png")
        plt.close()
        return True
    except Exception as e:
        print(e)
        return e


def plot_clusters_3d(x, labels=labels, colorSet=color, algorithm=""):
    try:
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection="3d")
        for index, data in enumerate(x):
            x3d = [i[1] for i in data]
            y3d = [i[2] for i in data]
            z3d = [i[3] for i in data]
            ax.scatter(
                x3d, y3d, z3d, c=colorSet[index], label=labels[index], cmap="viridis"
            )
        ax.set_xlabel("GC1")
        ax.set_ylabel("GC2")
        ax.set_zlabel("GC3")
        ax.legend(loc="best")
        plt.title(f"{algorithm} - 3D Plot")
        plt.savefig(f"{img_path}/{algorithm.lower()}_plot_3d.png")
        plt.close()
        return True
    except Exception as e:
        print(e)
        return e


def save_cluster_correlation_matrix(labels_dict, img_path):
    """
    Calculate the correlation matrix between clustering labels and save it as an image.

    Parameters:
    - labels_dict: A dictionary where keys are algorithm names and values are corresponding labels.
    - img_path: Path to save the correlation matrix image.

    Returns:
    - correlation_matrix: Pandas DataFrame representing the correlation matrix.
    """
    df_labels = pd.DataFrame(labels_dict)

    correlation_matrix = df_labels.corr()

    # Plotting and saving the correlation matrix as an image
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Cluster Correlation Matrix")
    plt.savefig(f"{img_path}/cluster_correlation_matrix.png")
    plt.close()
