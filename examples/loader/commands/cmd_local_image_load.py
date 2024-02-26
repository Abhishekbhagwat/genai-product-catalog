class LocalImageStorageCommand:
    @staticmethod
    def store_locally(file_path: str, image_data: bytes):
        with open(file_path, 'wb') as f:
            f.write(image_data)