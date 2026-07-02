from src.click_generator import generate_clicks
from src.seed import generate_products, generate_users


def main():
    users = generate_users(3)
    products = generate_products(3)

    clicks = generate_clicks(3, products, users)

    print("---\nusers:")
    for user in users:
        print(user)
    print("---\nproducts:")
    for product in products:
        print(product)
    print("---\nclicks:")
    for click in clicks:
        print(click)


if __name__ == "__main__":
    main()
