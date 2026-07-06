from src.analytics import get_hot_products
from src.click_service import generate_and_store_clicks
from src.database import get_database


def main():
    db = get_database()
    # generate_and_store_clicks(db, 1000)
    for hot in get_hot_products(db, 5):
        print(hot)


if __name__ == "__main__":
    main()
