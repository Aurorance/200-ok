from datetime import datetime
from pydantic import BaseModel
from bson import ObjectId

class Spirits(BaseModel):
    id: ObjectId
    spirit_name: str
    spirit_price: int
    spirit_stock: int
    spirit_category: str
    Date: str

    class Config:
        arbitrary_types_allowed = True

