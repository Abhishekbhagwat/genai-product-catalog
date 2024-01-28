import configparser
from google.cloud import bigquery

class VerifyAndConnectToBigQueryCommand:
    project_id: str = None

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('conf/app.toml')
        VerifyAndConnectToBigQueryCommand.project_id = config['project']['id']

    @staticmethod
    def connect_to_bigquery() -> bool:
        client = bigquery.Client(project=VerifyAndConnectToBigQueryCommand.project_id)
        print(f"Connected to BigQuery project: {client.project}")
        return True