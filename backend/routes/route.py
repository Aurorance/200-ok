from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from fastapi_pagination import Page, add_pagination, paginate, Params
from models.spirits import Spirits
from config.database import db
from schema.schemas import list_serial
from bson import ObjectId

router = APIRouter()

# Get request method with pagination
@router.get('/spirits')
async def get_spirit(size: int = 10, currentPage: int = 1):
    spirits = list_serial(db.spirits.find().skip(size* currentPage).limit(size))
    return spirits

# Add pagination support to the router
#add_pagination(spiritsRouter)


# Get request method for the most rare wines in the past 3 months based on stock
@router.get('/rare-wines')
async def get_rare_wines(size: int = 5):
    three_months_ago = datetime.now() - timedelta(days=90)
    wines = list_serial(
        db.hist_spirits.aggregate([
            {"$match": {"Date": {"$gte": str(three_months_ago)}}},
            {"$group": {"_id": "$spirit_name", "avg_stock": {"$avg": "$spirit_stock"}}},
            {"$sort": {"avg_stock": 1, "spirit_stock": -1, "price": -1}},
            {"$limit": size}
        ])
    )
    return wines

# Get request method for the most rare wine according to stock
@router.get('/most-rare-wine')
async def get_most_rare_wine():
    wine = list_serial(
        db.hist_spirits.find().sort([("price", -1), ("spirit_stock", 1)]).limit(1)
    )
    return list_serial(wine)