# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Optional

import vertexai
from vertexai.vision_models import (
    Image,
    MultiModalEmbeddingModel,
    MultiModalEmbeddingResponse,
)


def get_image_embeddings(
    project_id: str,
    location: str,
    image_path: str,
    contextual_text: Optional[str] = None,
    dimension: int = 1408,
) -> MultiModalEmbeddingResponse:
    """Example of how to generate multimodal embeddings from image and text.

    Args:
        project_id: Google Cloud Project ID, used to initialize vertexai
        location: Google Cloud Region, used to initialize vertexai
        image_path: Path to image (local or Google Cloud Storage) to generate embeddings for.
        contextual_text: Text to generate embeddings for.
        dimension: Dimension for the returned embeddings.
            https://cloud.google.com/vertex-ai/docs/generative-ai/embeddings/get-multimodal-embeddings#low-dimension
    """

    vertexai.init(project=project_id, location=location)

    model = MultiModalEmbeddingModel.from_pretrained("multimodalembedding")
    image = Image.load_from_file(image_path)

    embeddings = model.get_embeddings(
        image=image,
        contextual_text=contextual_text,
        dimension=dimension,
    )
    print(f"Image Embedding: {embeddings.image_embedding}")
    print(f"Text Embedding: {embeddings.text_embedding}")

if __name__ == "__main__":

    results = get_image_embeddings(
        project_id="customermod-genai-sa",
        location='us-central1',
        image_path="gs://cloud-samples-data/vertex-ai/llm/prompts/landmark1.png",
        contextual_text='FabHomeDecor Fabric Double Sofa Bed')