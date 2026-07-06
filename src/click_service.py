from dataclasses import asdict
from datetime import datetime, timedelta, timezone
from random import choice, randint

from pymongo.database import Database

from .database import find_all, insert_many
from .models import Click, Collections, Devices


def _generate_clicks(
    num_clicks: int, products: list[dict], users: list[dict]
) -> list[Click]:
    clicks = []
    devices = [device.value for device in Devices]
    for _ in range(num_clicks):
        click = Click(
            user_id=choice(users)["_id"],
            product_id=choice(products)["_id"],
            timestamp=datetime.now(timezone.utc) - timedelta(days=randint(0, 30)),
            device=choice(devices),
        )
        clicks.append(click)
    return clicks


def generate_and_store_clicks(db: Database, num_clicks: int = 10):
    clicks = _generate_clicks(
        num_clicks,
        find_all(db, Collections.PRODUCTS.value),
        find_all(db, Collections.USERS.value),
    )
    clicks = [asdict(click) for click in clicks]
    insert_many(db, Collections.CLICKS.value, clicks)
