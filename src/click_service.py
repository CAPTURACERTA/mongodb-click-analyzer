from dataclasses import asdict

from pymongo.database import Database

from .click_generator import generate_clicks
from .database import find_all, insert_many
from .models import Collections


def generate_and_store_clicks(db: Database, num_clicks: int = 10):
    clicks = generate_clicks(
        num_clicks,
        find_all(db, Collections.PRODUCTS.value),
        find_all(db, Collections.USERS.value),
    )
    clicks = [asdict(click) for click in clicks]
    insert_many(db, Collections.CLICKS.value, clicks)
