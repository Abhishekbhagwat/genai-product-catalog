from google.cloud import bigquery

class BQEmbeddingLoaderCommand:
    @staticmethod
    def load_embeddings_to_bigquery(dataset_id: str, table_id: str, embeddings: str):
        client = bigquery.Client()
        table = client.dataset(dataset_id).table(table_id)
        rows_to_insert = [(embeddings,)]
        errors = client.insert_rows(table, rows_to_insert)
        if errors:
            print(f"Failed to load embeddings: {errors}")
            return False
        return True