from __future__ import annotations

from datetime import date, timedelta
import sqlite3
from pathlib import Path
from typing import Iterable

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "sales.db"
REGIONS = ["North", "South", "East", "West", "Central"]
PAYMENT_METHODS = ["credit_card", "ach", "wire", "paypal"]


def generate_customers(count: int = 150) -> list[tuple[int, str, str, str]]:
    customers = []
    for idx in range(1, count + 1):
        name = f"Customer {idx:03d}"
        email = f"customer{idx:03d}@example.com"
        region = REGIONS[idx % len(REGIONS)]
        customers.append((idx, name, email, region))
    return customers


def generate_products() -> list[tuple[int, str, str, float]]:
    categories = [
        ("Hardware", 49.0, 399.0),
        ("Subscription", 99.0, 599.0),
        ("Services", 150.0, 850.0),
        ("Accessories", 19.0, 149.0),
    ]
    products: list[tuple[int, str, str, float]] = []
    product_id = 1
    for category, base_price, max_price in categories:
        for i in range(1, 11):
            price = round(base_price + (i * (max_price - base_price) / 10), 2)
            products.append((product_id, f"{category} Package {i}", category, price))
            product_id += 1
    return products


def generate_orders(
    customers: Iterable[tuple[int, str, str, str]],
    products: Iterable[tuple[int, str, str, float]],
    count: int = 220,
) -> tuple[list[tuple], list[tuple]]:
    product_lookup = {prod[0]: prod for prod in products}
    orders: list[tuple] = []
    payments: list[tuple] = []
    start_date = date(2024, 1, 1)
    customers_list = list(customers)
    products_list = list(products)

    for order_id in range(1, count + 1):
        customer_id = customers_list[order_id % len(customers_list)][0]
        product_id = products_list[order_id % len(products_list)][0]
        quantity = (order_id % 5) + 1
        price = product_lookup[product_id][3]
        total = round(price * quantity, 2)
        order_date = start_date + timedelta(days=order_id % 365)
        payment_date = order_date + timedelta(days=1)
        method = PAYMENT_METHODS[order_id % len(PAYMENT_METHODS)]

        orders.append(
            (
                order_id,
                customer_id,
                product_id,
                order_date.isoformat(),
                quantity,
                total,
            )
        )
        payments.append(
            (
                order_id,
                order_id,
                method,
                total,
                payment_date.isoformat(),
            )
        )

    return orders, payments


CUSTOMERS = generate_customers()
PRODUCTS = generate_products()
ORDERS, PAYMENTS = generate_orders(CUSTOMERS, PRODUCTS)


def init_db(path: Path = DB_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    cur = conn.cursor()

    cur.executescript(
        """
        PRAGMA foreign_keys = ON;
        DROP TABLE IF EXISTS payments;
        DROP TABLE IF EXISTS orders;
        DROP TABLE IF EXISTS products;
        DROP TABLE IF EXISTS customers;

        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            region TEXT NOT NULL
        );

        CREATE TABLE products (
            product_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL
        );

        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
            product_id INTEGER NOT NULL REFERENCES products(product_id),
            order_date TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            total_amount REAL NOT NULL
        );

        CREATE TABLE payments (
            payment_id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL REFERENCES orders(order_id),
            method TEXT NOT NULL,
            amount REAL NOT NULL,
            payment_date TEXT NOT NULL
        );
        """
    )

    cur.executemany(
        "INSERT INTO customers VALUES (?, ?, ?, ?)",
        CUSTOMERS,
    )
    cur.executemany(
        "INSERT INTO products VALUES (?, ?, ?, ?)",
        PRODUCTS,
    )
    cur.executemany(
        "INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?)",
        ORDERS,
    )
    cur.executemany(
        "INSERT INTO payments VALUES (?, ?, ?, ?, ?)",
        PAYMENTS,
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print(f"Database created at {DB_PATH}")
