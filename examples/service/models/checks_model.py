from pydantic import BaseModel
from typing import Optional

class Status(BaseModel):
    status: str
    
class Liveliness(BaseModel):
    message: str
