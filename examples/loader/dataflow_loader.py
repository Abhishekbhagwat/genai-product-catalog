import apache_beam as beam
import argparse
import pandas as pd
import jsonpickle
import json
import requests
import vertexai

from apache_beam.io import BigQueryDisposition, ReadFromPubSub, WriteToBigQuery
from apache_beam.io.gcp.bigquery_tools import RetryStrategy
from apache_beam.options.pipeline_options import PipelineOptions

from google.cloud import bigquery, storage
# import google.cloud.logging
from models.model import parse_row, FILE_COLUMNS
from typing import Optional

from vertexai.vision_models import (
    Image,
    MultiModalEmbeddingModel,
    MultiModalEmbeddingResponse,
)

# logger = google.cloud.logging.Client()
# logger.setup_logging()

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

    embedding_model = MultiModalEmbeddingModel.from_pretrained("multimodalembedding@001")

    image = Image.load_from_file(image_path)

    embeddings = embedding_model.get_embeddings(
        image=image,
        contextual_text=contextual_text,
        dimension=dimension,
    )
    print(f"Image Embedding: {embeddings.image_embedding[0:10]}")
    print(f"Text Embedding: {embeddings.text_embedding[0:10]}")

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
    json_str = jsonpickle.encode(product, unpicklable=False)
    # print(json_str)
    return json_str # jsonpickle.encode(product, unpicklable=False)


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
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name

    def process(self, element):
        # Create the storage client within the process method
        client = storage.Client()
        try:
            product = element  # Assuming element is the product object
            print(f"Processing product: {element.headers[0].name}")
            image_url = product.headers[0].images[0].origin_url
            print("===")
            print(image_url)
            print(product.business_keys[0].name)
            print(product.business_keys[0].value)
            print("===")
            response = requests.get(image_url)
            if response.status_code == 200:
                blob_name = f'images/{product.business_keys[0].value}.jpg'
                bucket = client.bucket(self.bucket_name)
                blob = bucket.blob(blob_name)
                blob.upload_from_string(response.content, content_type='image/jpeg')
                gcs_url = f'gs://{self.bucket_name}/{blob_name}'
                product.headers[0].images[0].url = gcs_url
                yield 'success', product
            else:
                print(f"[Error]{image_url}")
                yield 'failure', f'Failed to download image from {image_url}'
        except Exception as e:
            yield 'failure', str(e)



class CallEmbeddingAPI(beam.DoFn):
    def __init__(self, project_id, location):
        self.project_id = project_id
        self.location = location

    def process(self, element):
        print(f"Embedding product: {element.headers[0].name}")
        try:
            product = element  # Assuming element is a tuple (status, product)
            image_path = product.headers[0].images[0].url
            contextual_text = product.headers[0].name + product.headers[0].long_description + product.headers[0].brand
            embeddings = get_multimodal_embeddings(
                project_id=self.project_id,
                location=self.location,
                image_path=image_path,
                contextual_text=contextual_text
            )
            # Assuming you want to store or do something with the embeddings here
            # For simplicity, just printing the embeddings
            product.image_embedding = embeddings.image_embedding
            product.text_embedding = embeddings.text_embedding
            print("embedding finished")
            
            yield 'success', product
        except Exception as e:
            print(f"[CallEmbeddingAPI][Error]{e}")
            yield 'failure', str(e)

def partition_fn(element, num_partitions):
    print(f"...partition_fn...{num_partitions}:{element}")
    return 0 if element[0] == 'success' else 1

class AggregateToList(beam.CombineFn):
    def create_accumulator(self):
        return []

    def add_input(self, accumulator, input):
        json_input = json.loads(input)
        accumulator.append(json_input)
        # accumulator.append(input)
        return accumulator

    def merge_accumulators(self, accumulators):
        return [item for sublist in accumulators for item in sublist]

    def extract_output(self, accumulator):
        return accumulator


class WriteJsonToBigQuery(beam.DoFn):
    def __init__(self, project_id:str, bq_table_id:str):
        self.project_id = project_id
        self.fully_qualified_table = bq_table_id

    def process(self, element):
        json_data = json.loads(element)
        print(f"[WriteJsonToBigQuery]element:{element[0:100]}")
        status, data = json_data
        print(f"* status={status}")
        if status == "success":
            print(f"[WriteJsonToBigQuery]data:{json.dumps(data)[0:100]}")
            bq_client = bigquery.Client(self.project_id)
            table = bq_client.get_table(self.fully_qualified_table)
            result = bq_client.insert_rows_json(table, [data])
            print(f"[WriteJsonToBigQuery]Insert [{self.fully_qualified_table}] Completed:{result}")

        return element


class WriteToGCS(beam.DoFn):
    def __init__(self, project_id, bucket, file_name):
        self.project_id = project_id
        self.bucket = bucket
        self.file_name = file_name

    def process(self, element):
        print(f"[WriteToGCS]:{self.bucket} | {self.file_name}")
        client = storage.Client(self.project_id)
        bucket = client.get_bucket(self.bucket)
        blob = bucket.blob(self.file_name)
        blob.upload_from_string(f"{element}")


def get_schema():
    result = []
    with open(file="./schema/bq-pdc.json", mode="r") as f:
        columns = json.load(f)
        for column in columns:
            result.append(bigquery.SchemaField(column['name'], column['type']))

        return result
        for field in schema:
            result.append(f"{field['name']}:{field['type']}")
    schema_result = ",".join([line.strip() for line in result])
    print(schema_result)
    return schema_result


def run(argv=None, save_main_session=True):
    """Main entry point; defines and runs the wordcount pipeline."""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input_subscription",
        dest="subscription",
        help="Input PubSub subscription of the form "
        '"projects/<PROJECT>/subscriptions/<SUBSCRIPTION>."',
    )
    parser.add_argument(
        '--bucket',
        dest='bucket',
        required=True,
        help='GCS Bucket name for storing product images and information.')
    parser.add_argument(
        '--bq-table-id',
        dest='bq_table_id',
        required=True,
        help='Full qualified BigQuery dataset id in <DATASET_ID>.<TABLE_ID> format.')

    known_args, pipeline_args = parser.parse_known_args(argv)

    # We use the save_main_session option because one or more DoFn's in this
    # workflow rely on global context (e.g., a module imported at module level).
    pipeline_options = PipelineOptions(
        pipeline_args,
        save_main_session=True,
        streaming=True,
        setup_file="/template/setup.py")

    project_id = ""

    if "--project" in pipeline_args:
        project_id = pipeline_args[pipeline_args.index("--project") + 1]
    elif "-p" in pipeline_args:
        project_id = pipeline_args[pipeline_args.index("-p") + 1]
    else:
        items = [item for item in pipeline_args if item.startswith("--project=")]
        if len(items) > 0:
            project_id = items[0].split("=")[1]


    subscription_id = known_args.subscription
    bucket_name = known_args.bucket
    bq_table_id = f"{project_id}.{known_args.bq_table_id}"

    print(f"*** project_id={project_id}")
    with beam.Pipeline(options=pipeline_options) as p:
        print(f"** Starting pipeline...{subscription_id}")
        # raw_data = (
        #     p
        #     | 'Read Pub/Sub' >> beam.io.ReadFromPubSub(subscription=subscription_id).with_output_types(bytes)
        #     | "UTF-8 bytes to string" >> beam.Map(lambda msg: msg.decode("utf-8"))
        #     | 'Parse CSV Lines' >> beam.Map(lambda x: dict(zip(FILE_COLUMNS.keys(), x.split(','))))
        # )
        print(f"""FILE_COLUMNS={FILE_COLUMNS}""")
        raw_data = (
            p
            | 'Read Pub/Sub' >> beam.io.gcp.pubsub.ReadStringsFromPubSub(subscription=subscription_id)
            | 'Parse CSV Lines' >> beam.Map(lambda x: dict(zip(FILE_COLUMNS.keys(), x.split(','))))
        )
        print(f"Reading...${raw_data}")
        parsed_data = (
            raw_data
            | 'Parse Row' >> beam.ParDo(ParseRow())
            | 'Partition by Parse Success' >> beam.Partition(partition_fn, 2)
        )

        success_data, failed_parse = parsed_data
        
        print(f"Processing...${success_data}")
        print(f"bucket_name...${bucket_name}")
        # Process successfully parsed data further
        processed_data = (
            success_data
            | 'Extract Success Data' >> beam.Map(lambda x: x[1])  # Extract the product object from the tuple
            | 'Download Image to GCS' >> beam.ParDo(DownloadImage(bucket_name=bucket_name))
            | 'Partition by Download Success' >> beam.Partition(partition_fn, 2)
        )

        success_downloads, failed_downloads = processed_data
        
        # # Call Embedding API on successfully downloaded images
        embedding_results = (
            success_downloads
            | 'Extract Success Downloads' >> beam.Map(lambda x: x[1])  # Extract the product object from the tuple
            | 'Call Embedding API' >> beam.ParDo(CallEmbeddingAPI(project_id=project_id, location='us-central1'))
            | 'Convert to JSON' >> beam.Map(product_to_json)
            # | 'Write to BigQuery' >> WriteToBigQuery(
            #     bq_table_id,
            #     create_disposition=BigQueryDisposition.CREATE_IF_NEEDED,
            #     write_disposition=BigQueryDisposition.WRITE_APPEND,
            #     insert_retry_strategy=RetryStrategy.RETRY_ON_TRANSIENT_ERROR,
            #     schema=get_schema(),
            #     additional_bq_parameters={
            #     },
            # )
            | 'Write to BigQuery' >> beam.ParDo(WriteJsonToBigQuery(project_id=project_id, bq_table_id=bq_table_id))
            # | 'Aggregate to List' >> beam.CombineGlobally(AggregateToList())
        )

        # Optionally, write failed records to some sink for inspection
        # (failed_parse, failed_downloads
        # | 'Merge Failure Collections' >> beam.Flatten()
        # | 'Write Failures to GCS' >> beam.io.WriteToText('gs://your-bucket/failures.txt')
        # )

if __name__ == '__main__':
    run()
