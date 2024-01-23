from fastapi import APIRouter, HTTPException
from models.common_model import (
    Product,
    ProductAttributes,
    MarketingRequest,
    TextValue
)
from models.checks_model import Status

from google.cloud.ml.applied.attributes import attributes
from google.cloud.ml.applied.marketing import marketing
from google.cloud.ml.applied.embeddings import search

router = APIRouter()

@router.post('/api/v1/genai/products/attributes')
def suggest_attributes(
    product: Product
) -> ProductAttributes:
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
        desc=product.description,
        category=product.category,
        image=product.image_uri,
        base64=False,
        filters=product.category
    )


@router.post('/api/v1/genai/products/marketing')
def generate_marketing_copy(
     marketing_request: MarketingRequest
) -> TextValue:
    """
    Generate Marketing Copy for a product based on its description, image and/or
    categories.
    """
    return marketing.generate_marketing_copy(marketing_request)


@router.post('/api/v1/genai/products')
def product_create_index(
    product: Product
) -> Status:
    
    search.upsert_dp(
        prod_id=product.id,
        desc=product.description,
        image=product.image_uri,
        cat=product.category
    )

    return Status(status='OK')


@router.put('/api/v1/genai/products/{product_id}')
def update_vector_search_index(
    product_id: str,
    product: Product
) -> Status:
    """
    Adding the new/updated product info into already built&deployed
        Vector Search Index
    """
    search.upsert_dp(
        prod_id=product.id,
        desc=product.description,
        image=product.image_uri,
        cat=product.category
    )

    return Status(status='OK')

@router.delete('/api/v1/genai/products/{product_id}')
def remove_product_from_vector_search(
    product_id: str
) -> None:
    """
    Removing the product from already built&deployed Vector Search Index

    Params:
    product_id: The unique id of the product.

    Returns:
    If successful, the response body is empty[https://cloud.google.com/vertex-ai/docs/reference/rest/v1/projects.locations.indexes/removeDatapoints}
    """
    search.delete_dp(prod_id=product_id)
    return None