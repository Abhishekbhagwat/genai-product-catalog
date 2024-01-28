from model import Product

class RDMReaderCommand:
    @staticmethod
    def read_rdm(rdm: list, index: int) -> Product:
        try:
            return rdm[index]
        except IndexError:
            print(f"No product found at index {index}")
            return None