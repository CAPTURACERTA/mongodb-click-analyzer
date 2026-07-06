from bson import ObjectId

from src.analytics import get_hot_devices, get_hot_products
from src.models import Collections

from conftest import FakeCollection, FakeDatabase


def test_get_hot_products_adds_product_names_and_preserves_click_order():
    product_a = ObjectId()
    product_b = ObjectId()
    missing_product = ObjectId()
    db = FakeDatabase(
        {
            Collections.CLICKS.value: FakeCollection(
                aggregate_result=[
                    {
                        "product_id": product_a,
                        "product_name": None,
                        "click_count": 8,
                    },
                    {
                        "product_id": missing_product,
                        "product_name": None,
                        "click_count": 4,
                    },
                    {
                        "product_id": product_b,
                        "product_name": None,
                        "click_count": 2,
                    },
                ]
            ),
            Collections.PRODUCTS.value: FakeCollection(
                [
                    {"_id": product_b, "name": "Noise Cancelling Headphones"},
                    {"_id": product_a, "name": "Mechanical Keyboard"},
                ]
            ),
        }
    )

    result = get_hot_products(db, limit=3)

    assert result == [
        {
            "product_id": product_a,
            "product_name": "Mechanical Keyboard",
            "click_count": 8,
        },
        {
            "product_id": missing_product,
            "product_name": "Unknown Product",
            "click_count": 4,
        },
        {
            "product_id": product_b,
            "product_name": "Noise Cancelling Headphones",
            "click_count": 2,
        },
    ]


def test_get_hot_products_returns_empty_list_when_there_are_no_clicks():
    db = FakeDatabase({Collections.CLICKS.value: FakeCollection()})

    assert get_hot_products(db) == []


def test_get_hot_products_uses_the_requested_limit_in_the_pipeline():
    db = FakeDatabase({Collections.CLICKS.value: FakeCollection()})

    get_hot_products(db, limit=2)

    assert db[Collections.CLICKS.value].pipeline[-1] == {"$limit": 2}


def test_get_hot_devices_returns_aggregated_devices():
    db = FakeDatabase(
        {
            Collections.CLICKS.value: FakeCollection(
                aggregate_result=[
                    {"device": "Laptop", "click_count": 10},
                    {"device": "Smartphone", "click_count": 7},
                ]
            )
        }
    )

    assert get_hot_devices(db, limit=2) == [
        {"device": "Laptop", "click_count": 10},
        {"device": "Smartphone", "click_count": 7},
    ]


def test_get_hot_devices_uses_the_requested_limit_in_the_pipeline():
    db = FakeDatabase({Collections.CLICKS.value: FakeCollection()})

    get_hot_devices(db, limit=4)

    assert db[Collections.CLICKS.value].pipeline[-1] == {"$limit": 4}
