import pytest
from infrastructure.orm import ProductORM, OrderORM


@pytest.fixture
def sample_products(session):
    products = [
        ProductORM(name="Keyboard", quantity=10, price=100.0),
        ProductORM(name="Mouse", quantity=5, price=50.0),
    ]
    session.add_all(products)
    session.commit()
    return products


@pytest.fixture
def sample_order(session, sample_products):
    order = OrderORM()
    order.products.extend(sample_products)
    session.add(order)
    session.commit()
    return order
