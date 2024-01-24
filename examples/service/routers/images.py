from fastapi import APIRouter, HTTPException
from models.common_model import (
    ImageRequest,
    TextValue,
    ProductAttributes
)

from google.cloud.ml.applied.images import image_to_text

router = APIRouter()


@router.post('/api/v1/genai/images/attributes')
def generate_attributes(
    image_request: ImageRequest
) -> ProductAttributes:
    """
    Extracts attributes detected from product's image.
    """
    return image_to_text.image_to_attributes(image_request)


@router.post('/api/v1/genai/images/descriptions')
def generate_description(
    image_request: ImageRequest
) -> TextValue:
    """
    Generates a product description from an image of product.
    """
    return image_to_text.image_to_product_description(image_request.image)