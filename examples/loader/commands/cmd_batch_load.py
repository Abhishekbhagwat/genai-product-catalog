import os
import json
from model import Product

class BatchLoadCommand:
    @staticmethod
    def batch_load(rdm: list, images_dir: str, embeddings_dir: str) -> bool:
        # Store images and embeddings in local file system
        for product in rdm:
            if product.headers[0].images:
                image_url = product.headers[0].images[0].url
                image_name = os.path.basename(image_url)
                image_path = os.path.join(images_dir, image_name)
                # Download and save the image to the local file system
                # This is a placeholder and you'll need to replace it with actual image downloading code
                print(f"Downloading image from {image_url} to {image_path}")

            if product.headers[0].nlp_description:
                embedding_text = product.headers[0].nlp_description
                embedding_file = os.path.join(embeddings_dir, f"{product.business_keys[0].value}.txt")
                with open(embedding_file, 'w') as f:
                    f.write(embedding_text)

        # Load data via a batch processor
        # This is a placeholder and you'll need to replace it with actual batch loading code
        print(f"Loading batch of {len(rdm)} products.")

        return True