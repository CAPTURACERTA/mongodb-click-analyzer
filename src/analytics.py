from pymongo.database import Database

from src.models import Collections


def get_hot_products(db: Database, limit: int = 5) -> list[dict]:
    pipeline = [
        {
            "$group": {
                "_id": "$product_id",
                "click_count": {"$sum": 1},
            }
        },
        {
            "$project": {
                "_id": 0,
                "product_id": "$_id",
                "product_name": {"$literal": None},
                "click_count": 1,
            }
        },
        {"$sort": {"click_count": -1}},
        {"$limit": limit},
    ]
    hot_products = list(db[Collections.CLICKS.value].aggregate(pipeline))

    if not hot_products:
        return []

    product_ids = [item["product_id"] for item in hot_products]

    products_cursor = db[Collections.PRODUCTS.value].find(
        {"_id": {"$in": product_ids}}, {"name": 1}
    )

    product_name_map = {doc["_id"]: doc["name"] for doc in products_cursor}

    for item in hot_products:
        item["product_name"] = product_name_map.get(
            item["product_id"], "Unknown Product"
        )

    return hot_products
