#  Copyright 2023 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

# TODO - This should be refactored into the INI file


"""All backend config variables.

Update as needed to match your environment
"""
# GCP
PROJECT = 'solutions-2023-mar-107'
LOCATION = 'us-central1'
ENDPOINT = '{}-aiplatform.googleapis.com'.format(LOCATION)

# Vertex Vector Search
INDEX_ID = "projects/411826505131/locations/us-central1/indexes/924016377843417088"
FILTER_CATEGORIES = [  # List of category filter names from root to leaf
    'L0',
    'L1',
    'L2',
    'L3'
]
ENDPOINT_ID = '4968248843222122496'
DEPLOYED_INDEX = 'flipkart_streaming_with_filters'
NUM_NEIGHBORS = 7

# BigQuery
PRODUCT_REFERENCE_TABLE = 'solutions-2023-mar-107.flipkart.preprocessed_data'
COLUMN_ID = 'id'
COLUMN_CATEGORIES = [  # List of category column names from root to leaf
    'c0_name',
    'c1_name',
    'c2_name',
    'c3_name'
]
COLUMN_ATTRIBUTES = 'attributes'
COLUMN_DESCRIPTION = 'description'
ALLOW_TRAILING_NULLS = True  # whether to allow trailing category levels to be unspecified e.g (only top-level category is specified)

# Category
CATEGORY_DEPTH = len(
    COLUMN_CATEGORIES)  # number of levels in category hierarchy to consider

# Testing - Update these for unit tests to run properly
# TEST_PRODUCT_ID = '8f87b1af1e8ab42c1d559f2f9caf70bb' # Any valid product ID in reference table
TEST_PRODUCT_ID = 'dbdac18a8ee5a8a48238b9685c96e90a'  # Any valid product ID in reference table
TEST_CATEGORY_L0 = 'Watches'  # Any valid top level category. Case sensitive
TEST_DESCRIPTION = 'Timewel 1100-N1949_S Analog Watch - For Women - Buy Timewel 1100-N1949_S Analog Watch - For Women 1100-N1949_S Online at Rs.855 in India Only at Flipkart.com. - Great Discounts, Only Genuine Products, 30 Day Replacement Guarantee, Free Shipping. Cash On Delivery!'
TEST_GCS_IMAGE = "gs://genai-product-catalog/flipkart_20k_oct26/dbdac18a8ee5a8a48238b9685c96e90a_0.jpg"
TEST_IMAGE_URL = "http://img5a.flixcart.com/image/watch/t/p/r/1100-n1949-s-timewel-1100x1360-imaefy3pr4cwvduj.jpeg"
# ["http://img5a.flixcart.com/image/watch/t/p/r/1100-n1949-s-timewel-1100x1360-imaefy3pr4cwvduj.jpeg", "http://img5a.flixcart.com/image/watch/t/p/r/1100-n1949-s-timewel-original-imaefy3pr4cwvduj.jpeg", "http://img6a.flixcart.com/image/watch/t/p/r/1100-n1949-s-timewel-original-imaefy3psr6njbmz.jpeg", "http://img5a.flixcart.com/image/watch/t/p/r/1100-n1949-s-timewel-original-imaefy3p72fxknqz.jpeg", "http://img5a.flixcart.com/image/watch/t/p/r/1100-n1949-s-timewel-original-imaefy3pxcxrkd9m.jpeg"]
