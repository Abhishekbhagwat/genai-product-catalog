from fastapi import APIRouter, HTTPException
from models.common_model import (
    Product,
    CategoryList
)

from google.cloud.ml.applied.categories import category

router = APIRouter()

@router.post('/api/v1/genai/categories')
def suggest_categories(
    product: Product
) -> CategoryList:
    """
      Suggest categories for product based on the product description
      and image (if present).
    """
    return category.retrieve_and_rank(
        desc=product.description,
        image=product.image_uri,
        base64=False,
        filters=product.category
    )