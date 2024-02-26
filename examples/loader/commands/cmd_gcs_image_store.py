from google.cloud import storage

class GCSImageStorageCommand:
    @staticmethod
    def store_in_gcs(bucket_name: str, blob_name: str, image_data: bytes):
        client = storage.Client()
        bucket = client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_string(image_data)