from dataclasses import asdict

import pytest
from domain.models import Product,Order


@pytest.mark.parametrize(
    "idx, name, quantity, price",
    [
        (7, "Headphones", 20, 99.99),
        (8, "Webcam", 0, 29.99),
        (9, "USB Cable", 100, 0.0),
    ]
)
def test_products_creation(idx, name, quantity, price):
    product = Product(id=idx, name=name, quantity=quantity, price=price)
    assert product.id == idx
    assert product.name == name
    assert product.quantity == quantity
    assert product.price == price


@pytest.mark.parametrize(
    "idx, name, quantity, price",
    [
        (1, "", 1, 10),
        (2, "Headphones", 15, -99.99),
        (3, "USB Cable", -100, 0.0),
        (4, "Adapter", -1, -9.99),
    ]
)
def test_product_invalid_parameters(idx, name, quantity, price):
    with pytest.raises(ValueError):
        Product(id=idx, name=name, quantity=quantity, price=price)


# Check transformation into a dictionary
def test_product_asdict():
    product = Product(id=2, name="Phone", quantity=5, price=499.99)
    product_dict = asdict(product)

    assert product_dict == {
        "id": 2,
        "name": "Phone",
        "quantity": 5,
        "price": 499.99
    }


# Product comparison
def test_product_equality():
    product1 = Product(id=3, name="Tablet", quantity=7, price=299.99)
    product2 = Product(id=3, name="Tablet", quantity=7, price=299.99)

    assert product1 == product2


def test_order_initialization():
    order = Order(id=1)
    assert order.id == 1
    assert order.products == []


def test_add_products_to_order():
    order = Order(id=1)
    p1 = Product(id=1, name="Phone", quantity=2, price=499.99)
    p2 = Product(id=2, name="Case", quantity=1, price=19.99)

    order.add_product(p1)
    order.add_product(p2)

    assert len(order.products) == 2
    assert p1 in order.products
    assert p2 in order.products


@pytest.mark.parametrize(
    "product",
    [None, {"name": "Invalid"}, 123]
)
def test_add_invalid_product_type(product):
    order = Order(1)
    with pytest.raises(TypeError):
        order.add_product(product)
