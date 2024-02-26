from google.cloud import bigquery
from google.cloud.exceptions import NotFound

from .config_utils import ConfigLoader 
from ..chain_new import Command, Context

class VerifyAndOrCreateBigQuerySchemaCommand(Command):
    def is_executable(self, context: Context) -> bool:
        return context.has_key('bigquery_client') and context.has_key('target_dataset') and context.has_key('data_source_uri')

    def execute(self, context: Context) -> None:
        client = context.get_value('bigquery_client')
        dataset_id = context.get_value('target_dataset')
        table_id = context.get_value('target_table') # Added for table ID
        data_source_uri = context.get_value('data_source_uri')

        dataset_ref = client.dataset(dataset_id)

        # 1. Check if the dataset exists
        try:
            client.get_dataset(dataset_ref)  
        except NotFound:
            print(f"Dataset {dataset_id} does not exist. Creating...")
            dataset = bigquery.Dataset(dataset_ref)
            dataset.location = "US"  # Adjust location as needed
            client.create_dataset(dataset)  

        # 2. Create table with auto-detection
        table_ref = dataset_ref.table(table_id)
        job_config = bigquery.LoadJobConfig(autodetect=True)

        try: 
            client.get_table(table_ref)
            print(f"Table {table_id} already exists in dataset {dataset_id}")
        except NotFound:
            load_job = client.load_table_from_uri(
                data_source_uri, table_ref, job_config=job_config 
            )  
            load_job.result()  # Waits for table creation

            print(f"Table {table_id} created in dataset {dataset_id}")
