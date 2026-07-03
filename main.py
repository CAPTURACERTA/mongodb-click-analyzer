from src.database import find_all, get_database
from src.models import Collections


def main():
    db = get_database()
    for record in find_all(db, Collections.PRODUCTS.value):
        print(record)


if __name__ == "__main__":
    main()
