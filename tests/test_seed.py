from src.models import Product, User
from src.seed import generate_products, generate_users


def test_generate_users_returns_the_requested_amount_of_users():
    users = generate_users(3)

    assert len(users) == 3
    assert all(isinstance(user, User) for user in users)
    assert all(user.name for user in users)


def test_generate_products_returns_products_with_names_and_prices_in_range():
    products = generate_products(5)

    assert len(products) == 5
    assert all(isinstance(product, Product) for product in products)
    assert all(product.name for product in products)
    assert all(10 <= product.price <= 100 for product in products)
