from model import Product

class RTVerifyCommand:
    @staticmethod
    def verify_real_time(product: Product) -> bool:
        # Implement your real-time verification logic here
        # For example, check if the product has a valid SKU and non-empty name
        if product.business_keys and product.headers:
            sku_valid = any(bk.name == "SKU" and bk.value for bk in product.business_keys)
            name_valid = product.headers[0].name.strip() != ""
            return sku_valid and name_valid
        return False