# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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