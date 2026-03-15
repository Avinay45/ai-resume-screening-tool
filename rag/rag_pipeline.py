from models.embeddings import EmbeddingModel
from rag.vector_store import VectorStore


class RAGPipeline:

    def __init__(self):

        self.embedding_model = EmbeddingModel()

        self.vector_store = VectorStore(384)

    def index_resumes(self, resumes):

        vectors = []
        docs = []

        for resume_text in resumes:

            embedding = self.embedding_model.get_embedding(resume_text)

            vectors.append(embedding)

            docs.append(resume_text)

        self.vector_store.add_vectors(vectors, docs)

    def retrieve_candidates(self, job_description):

        query_embedding = self.embedding_model.get_embedding(job_description)

        results = self.vector_store.search(query_embedding)

        return results