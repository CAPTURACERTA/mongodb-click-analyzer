from dataclasses import asdict
from typing import Iterable

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import ServerSelectionTimeoutError

from .config import DB_NAME, URI
from .models import Collections
from .seed import generate_products, generate_users


def init_database(db: Database, init_records: int = 10):
    products = db[Collections.PRODUCTS.value]
    if products.count_documents({}) == 0:
        products_records = [
            asdict(record) for record in generate_products(init_records)
        ]
        products.insert_many(products_records)

    users = db[Collections.USERS.value]
    if users.count_documents({}) == 0:
        users_records = [asdict(record) for record in generate_users(init_records)]
        users.insert_many(users_records)


def get_database(name: str = DB_NAME) -> Database:
    try:
        client = MongoClient(URI, serverSelectionTimeoutMS=2000)

        db = client[name]
        return db

    except ServerSelectionTimeoutError:
        raise RuntimeError(
            "##Could not connect to MongoDB. Is your local server running?"
        )


def find_all(db: Database, collection: Collections) -> list[dict]:
    return list(db[collection].find({}))


def insert_many(db: Database, collection: Collections, data: Iterable[dict]):
    db[collection].insert_many(data)
