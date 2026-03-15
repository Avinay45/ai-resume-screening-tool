import faiss
import numpy as np


class VectorStore:

    def __init__(self, dimension):

        self.index = faiss.IndexFlatL2(dimension)
        self.documents = []

    def add_vectors(self, vectors, documents):

        vectors = np.vstack(vectors).astype("float32")

        self.index.add(vectors)

        self.documents.extend(documents)

    def search(self, query_vector, top_k=3):

        query_vector = np.array(query_vector).reshape(1, -1).astype("float32")

        distances, indices = self.index.search(query_vector, top_k)

        results = []

        for i in indices[0]:

            if i < len(self.documents):
                results.append(self.documents[i])

        return results