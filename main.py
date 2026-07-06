from src.analytics import get_hot_devices, get_hot_products
from src.click_service import generate_and_store_clicks
from src.database import get_database, init_database


def main():
    db = get_database()
    init_database(db)
    generate_and_store_clicks(db, 1)
    # for hot in get_hot_products(db, 2):
    #     print(hot)
    for hot_device in get_hot_devices(db, 10):
        print(hot_device)


if __name__ == "__main__":
    main()
