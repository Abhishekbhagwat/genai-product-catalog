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
    try: 
        response = category.retrieve_and_rank(
            desc=product.description,
            image=product.image_uri,
            base64=False,
            filters=product.category
        )
    except Exception as e:
        print(f"ERROR: Product Category Retrieve and Ranking Error: -> {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
    return response