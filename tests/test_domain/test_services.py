import pytest
from sqlalchemy.exc import NoResultFound
from domain.models import Product


def test_create_product(service):
    service.create_product(name="Product1", quantity=10, price=9.99)


@pytest.mark.parametrize(
    "name, quantity, price",
    [
        ("", 1, 10),
        ("Headphones", 15, -99.99),
        ("USB Cable", -100, 0.0),
        ("Adapter", -1, -9.99),
    ]
)
def test_create_invalid_product(service, name, quantity, price):
    with pytest.raises(ValueError):
        service.create_product(name=name, quantity=quantity, price=price)


def test_create_order_with_products(service):
    p1 = service.create_product(name="Product1", quantity=10, price=9.99)
    p2 = service.create_product(name="Product2", quantity=3, price=91.99)
    p3 = service.create_product(name="Product3", quantity=100, price=0.93)

    products = service.product_list()
    assert len(products) == 3
    assert p1 in products
    assert p2 in products
    assert p3 in products

    o1 = service.create_order(products)

    orders = service.order_list()
    assert len(orders) == 1
    assert o1 in orders
    assert p1 in orders[0].products
    assert p2 in orders[0].products
    assert p3 in orders[0].products

    gp2 = service.get_product(p2.id)
    assert gp2 == p2

    go1 = service.get_order(o1.id)
    assert go1 == o1


def test_create_order_with_unregistered_product(service):
    registered_product = service.create_product(name="Product1", quantity=10, price=9.99)
    unregistered_product = Product(id=77, name="Unregistered product", quantity=3, price=91.99)

    with pytest.raises(NoResultFound):
        service.create_order([registered_product, unregistered_product])
