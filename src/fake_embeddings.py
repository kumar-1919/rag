import numpy as np

class FakeEmbeddings:
    def embed_documents(self, texts):
        return [np.random.rand(768).tolist() for _ in texts]

    def embed_query(self, text):
        return np.random.rand(768).tolist()
