from datetime import datetime, timedelta, timezone
from random import choice, randint

from .models import Click, Devices, Product, User


def generate_clicks(
    num_clicks: int, products: list[Product], users: list[User]
) -> list[Click]:
    clicks = []
    for _ in range(num_clicks):
        click = Click(
            user_id=choice(users)._id,
            product_id=choice(products)._id,
            timestamp=datetime.now(timezone.utc) - timedelta(days=randint(0, 30)),
            device=choice(list(Devices)),
        )
        clicks.append(click)
    return clicks
