from google.cloud import bigquery
from google.cloud.exceptions import NotFound

from ..chain_new import Command, Context

from config_utils import ConfigLoader

class VerifyAndConnectToBigQueryCommand(Command):
    def is_executable(self, context: Context) -> bool:
        # You might add additional checks based on your configuration
        return True 

    def execute(self, context: Context) -> None:
        config_loader = ConfigLoader()
        config = config_loader.get_config()

        project_id = config['gcp']['project_id']
        client = bigquery.Client(project=project_id) 
        context.add_value('bigquery_client', client)
