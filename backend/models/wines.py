from datetime import datetime
from pydantic import BaseModel
from bson import ObjectId

class Wine(BaseModel):
    id: ObjectId
    wine_name: str
    wine_price: int
    wine_stock: int
    wine_category: str
    Date: str

    class Config:
        arbitrary_types_allowed = True

