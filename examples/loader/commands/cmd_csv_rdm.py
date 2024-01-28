import pandas as pd
from model import parse_row, Product

class CSVToRDMCommand:
    @staticmethod
    def load_csv_to_rdm(csv_file_path: str, pre_process: bool = False) -> list:
        df = pd.read_csv(csv_file_path)
        rdm = []
        for _, row in df.iterrows():
            product = parse_row(row, pre_process)
            if product is not None:
                rdm.append(product)
        return rdm