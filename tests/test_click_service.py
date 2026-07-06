from dataclasses import asdict
from datetime import datetime, timezone

from bson import ObjectId

from src import click_service
from src.click_service import _generate_clicks, generate_and_store_clicks
from src.models import Collections, Devices

from conftest import FakeCollection, FakeDatabase


class FrozenDatetime(datetime):
    @classmethod
    def now(cls, tz=None):
        return cls(2026, 7, 6, 12, 0, tzinfo=tz)


def test_generate_clicks_creates_clicks_from_available_users_products_and_devices(
    monkeypatch,
):
    user_id = ObjectId()
    product_id = ObjectId()
    monkeypatch.setattr(click_service, "datetime", FrozenDatetime)
    monkeypatch.setattr(click_service, "randint", lambda start, end: 5)
    monkeypatch.setattr(click_service, "choice", lambda items: items[0])

    clicks = _generate_clicks(
        2,
        products=[{"_id": product_id}],
        users=[{"_id": user_id}],
    )

    assert len(clicks) == 2
    assert all(click.user_id == user_id for click in clicks)
    assert all(click.product_id == product_id for click in clicks)
    assert all(click.timestamp == FrozenDatetime(2026, 7, 1, 12, 0, tzinfo=timezone.utc) for click in clicks)
    assert all(click.device == Devices.SMARTPHONE.value for click in clicks)


def test_generate_and_store_clicks_reads_products_and_users_then_inserts_clicks(
    monkeypatch,
):
    product_id = ObjectId()
    user_id = ObjectId()
    db = FakeDatabase(
        {
            Collections.PRODUCTS.value: FakeCollection([{"_id": product_id}]),
            Collections.USERS.value: FakeCollection([{"_id": user_id}]),
            Collections.CLICKS.value: FakeCollection(),
        }
    )
    monkeypatch.setattr(click_service, "datetime", FrozenDatetime)
    monkeypatch.setattr(click_service, "randint", lambda start, end: 0)
    monkeypatch.setattr(click_service, "choice", lambda items: items[0])

    generate_and_store_clicks(db, num_clicks=1)

    inserted_clicks = db[Collections.CLICKS.value].inserted_many[0]
    assert inserted_clicks == [
        asdict(
            _generate_clicks(
                1,
                products=[{"_id": product_id}],
                users=[{"_id": user_id}],
            )[0]
        )
    ]
