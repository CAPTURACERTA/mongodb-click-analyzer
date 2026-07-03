from datetime import datetime, timedelta, timezone
from random import choice, randint

from .models import Click, Devices


def generate_clicks(
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
