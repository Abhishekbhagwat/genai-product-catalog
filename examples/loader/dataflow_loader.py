import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io import ReadFromText, WriteToText
from apache_beam.io.gcp.gcsio import GcsIO
import jsonpickle
import pandas as pd

from google.cloud import storage
import requests
from io import BytesIO

from model import parse_row, FILE_COLUMNS  # Ensure this is the path to your data model module

from typing import Optional

import vertexai
from vertexai.vision_models import (
    Image,
    MultiModalEmbeddingModel,
    MultiModalEmbeddingResponse,
)

def get_multimodal_embeddings(
    image_path: str,
    contextual_text: Optional[str] = None,
    project_id: str = 'customermod-genai-sa',
    location: str = 'us-central1',
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

    return embeddings


def product_to_json(product):
    """
    Serialize a Product object to a JSON string using jsonpickle.
    
    Args:
        product: The Product object to serialize.
        
    Returns:
        A JSON string representing the serialized Product object.
    """
    # Setting unpicklable=False generates a JSON representation of the object
    # that can be easily converted back to a dictionary, but not necessarily back to the original object.
    print(product.headers[0].name)
    return jsonpickle.encode(product, unpicklable=False)


class ParseRow(beam.DoFn):
    def process(self, element):
        try:
            # Assuming 'element' is a dictionary representation of the CSV row
            product = parse_row(pd.Series(element), True)
            if product:
                # Yielding as a tuple (success indicator, data)
                print(product.headers[0].name)
                yield 'success', product
        except Exception as e:
            # Yielding as a tuple (failure indicator, error message)
            yield 'failure', str(e)

class DownloadImage(beam.DoFn):
    def process(self, element, bucket_name):
        # Create the storage client within the process method
        client = storage.Client()
        try:
            product = element  # Assuming element is the product object
            print(f"Processing product: {element.headers[0].name}")
            image_url = product.headers[0].images[0].origin_url
            print(image_url)
            print(product.headers[0].images)
            response = requests.get(image_url)
            if response.status_code == 200:
                blob_name = f'images/{product.pid}.jpg'
                bucket = client.bucket(bucket_name)
                blob = bucket.blob(blob_name)
                blob.upload_from_string(response.content, content_type='image/jpeg')
                gcs_url = f'gs://{bucket_name}/{blob_name}'
                product.headers[0].images[0].url = gcs_url
                print(product.headers[0].images[0].url)
                yield 'success', product
            else:
                yield 'failure', f'Failed to download image from {image_url}'
        except Exception as e:
            yield 'failure', str(e)



class CallEmbeddingAPI(beam.DoFn):
    def process(self, element, project_id, location):
        print(f"Embedding product: {element.headers[0].name}")
        try:
            product = element[1]  # Assuming element is a tuple (status, product)
            image_path = product.headers[0].images[0].url
            contextual_text = product.headers[0].name + product.headers[0].long_description + product.headers[0].brand
            embeddings = get_multimodal_embeddings(
                project_id=project_id,
                location=location,
                image_path=image_path,
                contextual_text=contextual_text
            )
            # Assuming you want to store or do something with the embeddings here
            # For simplicity, just printing the embeddings
            print(f"Embeddings for {product.product_name} obtained.")
            product.image_embedding = embeddings.image_embedding
            product.text_embedding = embeddings.text_embedding
            
            yield 'success', product
        except Exception as e:
            yield 'failure', str(e)

def partition_fn(element, num_partitions):
    return 0 if element[0] == 'success' else 1

def run():
    pipeline_options = PipelineOptions(
        # Your pipeline options
        runner='DirectRunner'
    )

    csv_file_path = '/usr/local/google/home/abhishekbhgwt/applied-ai/third_party/flipkart/ecommerce-sample_small.csv'
    bucket_name = 'pc-dataflow-test'
    output_file_path = '/usr/local/google/home/abhishekbhgwt/applied-ai/third_party/flipkart/output'

    with beam.Pipeline(options=pipeline_options) as p:
        raw_data = (
            p
            | 'Read CSV File' >> ReadFromText(csv_file_path, skip_header_lines=1)
            | 'Parse CSV Lines' >> beam.Map(lambda x: dict(zip(FILE_COLUMNS.keys(), x.split(','))))
        )

        parsed_data = (
            raw_data
            | 'Parse Row' >> beam.ParDo(ParseRow())
            | 'Partition by Parse Success' >> beam.Partition(partition_fn, 2)
        )

        success_data, failed_parse = parsed_data
        
        print(parsed_data)

        # Process successfully parsed data further
        processed_data = (
            success_data
            | 'Extract Success Data' >> beam.Map(lambda x: x[1])  # Extract the product object from the tuple
            | 'Download Image to GCS' >> beam.ParDo(DownloadImage(), bucket_name=bucket_name)
            | 'Partition by Download Success' >> beam.Partition(partition_fn, 2)
        )

        print(processed_data)

        success_downloads, failed_downloads = processed_data
        failed_downloads | 'Print Failed Data' >> beam.Map(print)


        # # Call Embedding API on successfully downloaded images
        embedding_results = (
            success_downloads
            | 'Extract Success Downloads' >> beam.Map(lambda x: x[1])  # Extract the product object from the tuple
            | 'Call Embedding API' >> beam.ParDo(CallEmbeddingAPI(), project_id='customermod-genai-sa', location='us-central1')
            | 'Convert to JSON' >> beam.Map(product_to_json)
            | 'Write to GCS' >> WriteToText(output_file_path, file_name_suffix='.json', shard_name_template='')
        )

        # Optionally, write failed records to some sink for inspection
        # (failed_parse, failed_downloads
        # | 'Merge Failure Collections' >> beam.Flatten()
        # | 'Write Failures to GCS' >> beam.io.WriteToText('gs://your-bucket/failures.txt')
        # )

if __name__ == '__main__':
    run()
