class LocalEmbeddingStorageCommand:
    @staticmethod
    def store_embeddings_locally(file_path: str, embeddings: str):
        with open(file_path, 'w') as f:
            f.write(embeddings)