from dataclasses import asdict

from src.analytics import get_hot_devices, get_hot_products
from src.click_service import generate_and_store_clicks
from src.database import get_database, init_database, insert_many
from src.models import Collections
from src.seed import generate_products, generate_users


def main():
    # demonstração do fluxo do projeto
    db = get_database()
    init_database(db)

    products = [asdict(product) for product in generate_products(10)]
    users = [asdict(user) for user in generate_users(10)]
    insert_many(db, Collections.PRODUCTS.value, products)
    insert_many(db, Collections.USERS.value, users)

    generate_and_store_clicks(db, 100)

    for hot_product in get_hot_products(db, 5):
        print(hot_product)

    print("---")

    for hot_device in get_hot_devices(db, 5):
        print(hot_device)


if __name__ == "__main__":
    main()
