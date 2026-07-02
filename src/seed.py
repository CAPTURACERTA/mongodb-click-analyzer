from random import uniform

from faker import Faker

from .models import Product, User

fake = Faker()


def generate_users(num_users: int) -> list[User]:
    users = []
    for _ in range(num_users):
        user = User(name=fake.name())
        users.append(user)
    return users


def generate_products(num_products: int) -> list[Product]:
    products = []
    for _ in range(num_products):
        product = Product(
            name=f"{fake.color_name()} {fake.bs().title()} {fake.bothify('##??').upper()}",
            price=round(uniform(10, 100), 2),
        )
        products.append(product)
    return products
