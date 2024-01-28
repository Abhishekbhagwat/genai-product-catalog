import pandas as pd
from ..models import parse_row
from .config_utils import ConfigLoader
from ..chain_new import Command, Context


class CSVToRDMCommand(Command):
    def is_executable(self, context: Context) -> bool:
        return context.has_key('config') and context.has_key('csv_file_path')

    def execute(self, context: Context) -> None:
        config = context.get_value('config')
        csv_file_path = context.get_value('csv_file_path')

        df = pd.read_csv(csv_file_path) 

        products = []
        for index, row in df.iterrows():
            product = parse_row(row, pre_process=True)
            if product:
                products.append(product)

        context.add_value('rdm', products)