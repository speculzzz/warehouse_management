import pytest
from infrastructure.orm import ProductORM, OrderORM


# Create product
@pytest.mark.parametrize(
    "name, quantity, price",
    [
        ("Headphones", 15, 99.99),
        ("USB Cable", 100, 0.0),
        ("Adapter", 0, 9.99),
    ]
)
def test_product_creation(session, name, quantity, price):
    product = ProductORM(name=name, quantity=quantity, price=price)
    session.add(product)
    session.commit()

    assert product.id is not None
    assert session.query(ProductORM).count() == 1

    db_product = session.query(ProductORM).first()
    assert db_product.name == name
    assert db_product.quantity == quantity
    assert db_product.price == price


@pytest.mark.parametrize(
    "name, quantity, price",
    [
        ("", 1, 10),
        ("Headphones", 15, -99.99),
        ("USB Cable", -100, 0.0),
        ("Adapter", -1, -9.99),
    ]
)
def test_product_invalid_parameters(session, name, quantity, price):
    with pytest.raises(ValueError):
        ProductORM(name=name, quantity=quantity, price=price)


# Create empty order
def test_order_creation(session):
    order = OrderORM()
    session.add(order)
    session.commit()

    assert order.id is not None
    assert session.query(OrderORM).count() == 1


# Complex queries with join
def test_query_orders_with_products(session, sample_order):
    orders = session.query(OrderORM).join(OrderORM.products).filter(
        ProductORM.price > 75.0
    ).all()

    assert len(orders) == 1
    assert orders[0].id == sample_order.id


# Check relationship
def test_product_order_relationship(session, sample_order):
    order = session.query(OrderORM).first()
    assert len(order.products) == 2
    assert {p.name for p in order.products} == {"Keyboard", "Mouse"}

    # Check back relationship
    product = session.query(ProductORM).filter_by(name="Keyboard").first()
    assert product in order.products


# Check cascade deletion
def test_cascade_deletion(session):
    product = ProductORM(name="Monitor", quantity=3, price=199.99)
    order = OrderORM()
    order.products.append(product)
    session.add(order)
    session.commit()

    # Delete the order
    session.delete(order)
    session.commit()

    # Product must exist
    assert session.query(ProductORM).count() == 1
    assert session.query(OrderORM).count() == 0


@pytest.mark.use_savepoint
def test_transaction_rollback(session):
    initial_count = session.query(ProductORM).count()

    session.begin_nested()

    new_product = ProductORM(name="New Product", quantity=1, price=10.0)

    session.add(new_product)
    session.commit()
    assert session.query(ProductORM).count() == initial_count + 1

    session.rollback()
    assert session.query(ProductORM).count() == initial_count
