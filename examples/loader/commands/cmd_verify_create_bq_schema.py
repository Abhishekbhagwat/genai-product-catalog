import configparser
from google.cloud import bigquery

class VerifyAndOrCreateBigQuerySchemaCommand:
    project_id: str = None
    dataset_id: str = None

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('conf/app.toml')
        VerifyAndOrCreateBigQuerySchemaCommand.project_id = config['project']['id']
        VerifyAndOrCreateBigQuerySchemaCommand.dataset_id = config['big_query']['prefix']

    @staticmethod
    def create_bigquery_schema() -> bool:
        client = bigquery.Client(project=VerifyAndOrCreateBigQuerySchemaCommand.project_id)
        dataset = bigquery.Dataset(VerifyAndOrCreateBigQuerySchemaCommand.dataset_id)
        dataset = client.create_dataset(dataset)
        print(f"Created dataset: {dataset.dataset_id}")
        return True