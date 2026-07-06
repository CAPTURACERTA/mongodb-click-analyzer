from bson import ObjectId

from src.database import find_all, init_database, insert_many
from src.models import Collections, Product, User

from conftest import FakeCollection, FakeDatabase


def test_find_all_returns_all_documents_from_collection():
    documents = [{"_id": ObjectId(), "name": "Ada"}, {"_id": ObjectId(), "name": "Linus"}]
    db = FakeDatabase({Collections.USERS.value: FakeCollection(documents)})

    assert find_all(db, Collections.USERS.value) == documents


def test_insert_many_delegates_to_the_selected_collection():
    db = FakeDatabase()
    documents = [{"name": "USB Dock"}, {"name": "Standing Desk"}]

    insert_many(db, Collections.PRODUCTS.value, documents)

    assert db[Collections.PRODUCTS.value].inserted_many == [documents]


def test_init_database_seeds_products_and_users_when_collections_are_empty(
    monkeypatch,
):
    products = [
        Product(name="Keyboard", price=70.0),
        Product(name="Mouse", price=40.0),
    ]
    users = [User(name="Grace"), User(name="Katherine")]
    monkeypatch.setattr("src.database.generate_products", lambda records: products)
    monkeypatch.setattr("src.database.generate_users", lambda records: users)
    db = FakeDatabase()

    init_database(db, init_records=2)

    assert db[Collections.PRODUCTS.value].documents == [
        {"name": "Keyboard", "price": 70.0, "_id": products[0]._id},
        {"name": "Mouse", "price": 40.0, "_id": products[1]._id},
    ]
    assert db[Collections.USERS.value].documents == [
        {"name": "Grace", "_id": users[0]._id},
        {"name": "Katherine", "_id": users[1]._id},
    ]


def test_init_database_does_not_seed_existing_collections(monkeypatch):
    monkeypatch.setattr(
        "src.database.generate_products",
        lambda records: [Product(name="Generated Product", price=10.0)],
    )
    monkeypatch.setattr(
        "src.database.generate_users", lambda records: [User(name="Generated User")]
    )
    existing_product = {"_id": ObjectId(), "name": "Existing Product", "price": 99.0}
    existing_user = {"_id": ObjectId(), "name": "Existing User"}
    db = FakeDatabase(
        {
            Collections.PRODUCTS.value: FakeCollection([existing_product]),
            Collections.USERS.value: FakeCollection([existing_user]),
        }
    )

    init_database(db)

    assert db[Collections.PRODUCTS.value].documents == [existing_product]
    assert db[Collections.USERS.value].documents == [existing_user]
