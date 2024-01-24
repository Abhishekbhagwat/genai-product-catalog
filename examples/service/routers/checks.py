from fastapi import APIRouter, HTTPException
from examples.services.models.checks_model import (
    Liveliness,
    Status
)

router = APIRouter()

@router.get('/readiness_check')
def readiness_check() -> Status:
    return Status(status='ready')

@router.get('/liveness_check')
def liveness_check() -> Liveliness:
    return Liveliness(message='ready')