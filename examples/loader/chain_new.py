from typing import Dict, List, Any
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor

from model import Product, Image, Currency
from google.cloud import bigquery
import pandas as pd
import tomllib as toml

class Context:
    def __init__(self):
        self.values: Dict[str, Any] = {}

    def has_key(self, key: str) -> bool:
        return key in self.values and self.values[key] is not None

    def add_value(self, key: str, value: Any) -> None:
        self.values[key] = value

    def get_value(self, key: str) -> Any:
        return self.values[key] if self.has_key(key) else None

class Command(ABC):
    @abstractmethod
    def is_executable(self, context: Context) -> bool:
        return False

    @abstractmethod
    def execute(self, context: Context) -> None:
        pass

class Chain(Command, ABC):
    def __init__(self):
        self.commands: List[Command] = []

    def add_command(self, command: Command) -> None:
        self.commands.append(command)

class BaseChain(Chain):
    def __init__(self):
        super().__init__()

    def is_executable(self, context: Context) -> bool:
        return len(self.commands) > 0

    def execute(self, ctx: Context) -> None:
        for cmd in self.commands:
            if cmd.is_executable(ctx):
                cmd.execute(ctx)

class ParallelChain(Chain):
    def __init__(self):
        super().__init__()

    def execute(self, ctx: Context) -> None:
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(cmd.execute, ctx) for cmd in self.commands if cmd.is_executable(ctx)]
            for future in futures:
                future.result()  # Wait for all commands to complete

# Example concrete Command implementations
class VerifyEnvironmentCommand(Command):
    def is_executable(self, context: Context) -> bool:
        # Define logic to determine if the command should be executed
        return True

    def execute(self, context: Context) -> None:
        print("Executing VerifyEnvironmentCommand...")
        # Implement the actual command logic here

class CSVToRDMCommand(Command):
    # ... (Existing code remains the same)

    def execute(self, context: Context) -> None:
        csv_file_path = context.get_value('csv_file_path')
        df = pd.read_csv(csv_file_path)  # Assuming you use pandas 

        products = []
        for index, row in df.iterrows():
            product = parse_row(row)  # Using your RDM parsing logic
            if product:
                products.append(product)

class RDMReaderCommand(Command):
    def is_executable(self, context: Context) -> bool:
        return context.has_key('rdm')

    def execute(self, context: Context) -> None:
        rdm = context.get_value('rdm')
        # Process the RDM data ... 

class WriteProductsToBigQueryCommand(Command):  
    def is_executable(self, context: Context) -> bool:
        return context.has_key('rdm') and context.has_key('bigquery_client')

    def execute(self, context: Context) -> None:
        rdm = context.get_value('rdm')
        bigquery_client = context.get_value('bigquery_client')

        # Logic to construct BigQuery table rows from RDM products
        # ...

        # Use bigquery_client.load_table_from_rows(...)





class ConfigLoaderCommand(Command):
    """Loads the configuration from config.toml"""
    CONFIG_FILE_PATH = "conf/app.toml" 

    def is_executable(self, context: Context) -> bool:
        return not context.has_key('config')  # Load if config isn't present

    def execute(self, context: Context) -> None:
        with open(self.CONFIG_FILE_PATH, 'r') as f:
            config = toml.load(f)
        context.add_value('config', config)  

class VerifyAndConnectToBigQueryCommand(Command):
    def is_executable(self, context: Context) -> bool:
        # You might check for additional BigQuery credentials here
        return True  # For now, assume we want to connect

    def execute(self, context: Context) -> None:
        config = context.get_value('config')
        project_id = config['project']['id']
        client = bigquery.Client(project=project_id) 
        context.add_value('bigquery_client', client)


class VerifyAndOrCreateBigQuerySchema(Command):
    def is_executable(self, context: Context) -> bool:
        return context.has_key('bigquery_client') and context.has_key('target_dataset')

    def execute(self, context: Context) -> None:
        client = context.get_value('bigquery_client')
        dataset_id = context.get_value('target_dataset')

        # 1. Check if the dataset exists.
        # 2. If not, create it.
        # 3. Define your schema based on the RDM structure.
        # 4. Check if the table exists.
        # 5. If not, create it.


# Example usage
context = Context()
chain = BaseChain()
chain.add_command(VerifyEnvironmentCommand())
# Add other commands to the chain

chain.execute(context)
