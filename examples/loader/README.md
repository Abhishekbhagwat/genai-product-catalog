# Data Loader

## Introduction

The Data Loader uses Dataflow to process and load the data to prepare your catalog to start using the GenAI based features offered by this solution.

We use `Dataflow` and `Pub/Sub` to run this pipeline. The following steps illustrate the entire workflow for the pipeline.

## Prerequisites for the pipeline

1. Create a BigQuery table to store the Retail Data Model transformed dataset along with the embeddings

```sql
CREATE TABLE `<PROJECT_ID>.<DATASET_ID>.<TABLE_ID>`
(
  business_keys ARRAY<STRUCT<value STRING, name STRING>>,
  image_embedding ARRAY<FLOAT64>,
  text_embedding ARRAY<FLOAT64>,
  categories ARRAY<STRUCT<children ARRAY<STRUCT<children ARRAY<STRUCT<children ARRAY<STRUCT<children ARRAY<STRING>, name STRING, id STRING>>, name STRING, id STRING>>, name STRING, id STRING>>, name STRING, id STRING>>,
  base_price STRUCT<rounding_rule STRUCT<trim_insignificant_digits BOOL, relevant_decimal INT64>, value STRUCT<decimal INT64, whole INT64>, code STRING>,
  headers ARRAY<STRUCT<attribute_values ARRAY<STRING>, images ARRAY<STRUCT<url STRING, origin_url STRING>>, nlp_description STRING, locale STRING, long_description STRING, short_description STRING, brand STRING, name STRING>>
);
```

2. Place a CSV record of your product dataset under `/applied-ai/third_party/flipkart`

3. Create a GCS bucket with your `<BUCKET_NAME>` to store various metadata and images, etc.

4. Create a folder inside GCS named `dataflow` and upload the local file `streaming-beam.json` to that folder

5. Create a [Pub/Sub topic](https://cloud.google.com/pubsub/docs/create-topic#create_a_topic_2) and [subscription](https://cloud.google.com/pubsub/docs/create-subscription#create_a_pull_subscription) to publish messages (rows of data) and subscription to trigger the dataflow processing job. 

6. Remeber to keep track of the IDs of the resources created above to plug into the code snippets below.

## Create Dataflow Pipeline

The follwing steps illustrate how you can run the data procesing pipeline in various scenarios.


1. Build Container Image

```shell
export PROJECT=<PROJECT_ID>
export TEMPLATE_IMAGE="gcr.io/$PROJECT/dataflow/streaming-beam:latest"
gcloud builds submit --project $PROJECT --tag "$TEMPLATE_IMAGE" .
```

2. Build the Dataflow Flex template to run the pipeline

```shell
export BUCKET=<BUCKET_NAME>
export TEMPLATE_PATH="gs://$BUCKET/dataflow/templates/streaming-beam.json"

# Build the Flex Template.
gcloud dataflow flex-template build $TEMPLATE_PATH \
  --image "$TEMPLATE_IMAGE" \
  --sdk-language "PYTHON" \
  --metadata-file "metadata.json"
```

3. Submit the job to Google Cloud Dataflow Runner

```shell
export REGION="us-central1"

gcloud dataflow flex-template run "streaming-beam-<JOB_ID>-`date +%Y%m%d-%H%M%S`" \
    --template-file-gcs-location "$TEMPLATE_PATH" \
    --temp-location gs://<GCS_LOGS_BUCKET_NAME>/tmp/ \
    --project $PROJECT \
    --parameters input_subscription="projects/${PROJECT}/subscriptions/<SUBSCRIPTION_NAME>" \
    --parameters bucket="<BUCKET_NAME>" \
    --parameters bq-table-id="<DATASET_ID>.<TABLE_ID >" \
    --enable-streaming-engine \
    --region "$REGION"
```

4. [OPTIONAL] For local testing, you can use DirectRunner

```shell
python -m dataflow_loader \
    --region "${REGION}" \
    --runner DirectRunner \
    --project "${PROJECT}" \
    --input_subscription="projects/${PROJECT}/subscriptions/<SUBSCRIPTION_NAME>" \
    --bucket="${BUCKET}" \
    --bq-table-id="<DATASET_ID>.<TABLE_ID >" \
    --streaming \
    --temp-location gs://<GCS_LOGS_BUCKET_NAME>/tmp/
```

5. Run the python script to publish the dataset rows to `Pub/Sub`
```shell
 python3 publish_csv.py \
    --project=$PROJECT_ID \
    --topic=$TOPIC_NAME \
    --csv-path=$CSV_DATASET_PATH
```