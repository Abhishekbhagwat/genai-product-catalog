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


"""Expose REST API for product cataloging functionality."""

import attributes
import category
import domain_model as m
import image_to_text
import marketing
import update_search_index
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

app = FastAPI()

origins = [
    "http://localhost:4000",
    "http://localhost:8080",
    "https://retail-shared-demos.uc.r.appspot.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
def home_page() -> str:
    """ Home Page """
    return """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
  <title>Catalog Enrichment GenAI services</title>
</head>
<body class="d-flex flex-column h-100">

<main class="flex-shrink-0">
    <div class="container">
        <h6>Google Catalog Enrichment Services</h6>
        <ul>
        <li><a href="/docs">Documentation</a></li>
        </ul>
    </div>
</main>
<footer class="footer mt-auto py-3 bg-light">
    <div class="text-center p-4" style="background-color: rgba(0, 0, 0, 0.05);">
    © 2023 Copyright: 
    <a class="text-reset fw-bold" href="https:/google.com/">Google LLC</a>
    </div>
</footer>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
</body>
</html>
"""


@app.get("/readiness_check")
def readiness_check() -> m.Status:
    """ Required for AppEngine """
    return m.Status(status='ready')


@app.get("/liveness_check")
def liveness_check() -> m.Liveliness:
    """ Required for AppEngine """
    return m.Liveliness(message='ready')


@app.post("/api/v1/genai/categories", tags=["Categories"])
def suggest_categories(product: m.Product) -> m.CategoryList:
    """
      Suggest categories for product based on the product description
      and image (if present).
    """
    return category.retrieve_and_rank(
        product.description,
        product.image_uri,
        base64=False,
        filters=product.category)


@app.post("/api/v1/genai/images/attributes", tags=["Images"])
def generate_attributes(image_request: m.ImageRequest) -> m.ProductAttributes:
    """
    Extracts attributes detected from product's image.
    """
    return image_to_text.image_to_attributes(image_request)


@app.post("/api/v1/genai/images/descriptions", tags=["Images"])
def generate_description(image_request: m.ImageRequest) -> m.TextValue:
    """
    Generates a product description from an image of product.
    """
    return image_to_text.image_to_product_description(image_request.image)


@app.post("/api/v1/genai/products/attributes", tags=['Products'])
def suggest_attributes(product: m.Product) -> m.ProductAttributes:
    """
    Uses Vertex AI to create attribute suggestions for product.

    ## Attributes
    Are a one (product) to many attribute relationship that allows for
    better searching and categorization. Attributes are generally defined
    at the category level, then inherited by a product belonging to that
    category. This is done to make the shopping experience consistent for
    the customer.

    """
    return attributes.retrieve_and_generate_attributes(
        product.description,
        product.category,
        product.image_uri,
        base64=False,
        filters=product.category)


@app.post("/api/v1/genai/products/marketing",
          status_code=200, tags=['Products'])
def generate_marketing_copy(model: m.MarketingRequest) -> m.TextValue:
    """
    Generate Marketing Copy for a product based on its description, image and/or
    categories.
    """
    return marketing.generate_marketing_copy(model)


@app.post("/api/v1/genai/products", status_code=202, tags=['Products'])
def product_create_index(product: m.Product) -> m.Status:
    update_search_index.upsert_dp(product.id,
                                  product.description,
                                  product.image_uri,
                                  product.category)
    return m.Status(status='OK')


@app.put("/api/v1/genai/products/{product_id}",
         status_code=202,
         tags=['Products'])
def update_vector_search_index(product_id: str, product: m.Product) -> m.Status:
    """
    Adding the new/updated product info into already built&deployed
        Vector Search Index
    """
    update_search_index.upsert_dp(product_id,
                                  product.description,
                                  product.image_uri,
                                  product.category)
    return m.Status(status="OK")


@app.delete("/api/v1/genai/products/{product_id}",
            status_code=204,
            tags=['Products'])
def remove_product_from_vector_search(product_id: str) -> None:
    """
    Removing the product from already built&deployed Vector Search Index

    Params:
    product_id: The unique id of the product.

    Returns:
    If successful, the response body is empty[https://cloud.google.com/vertex-ai/docs/reference/rest/v1/projects.locations.indexes/removeDatapoints}
    """
    update_search_index.delete_dp(product_id)
    return None
