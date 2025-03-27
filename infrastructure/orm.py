from sqlalchemy import Column, Integer, String, Float, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, validates

Base = declarative_base()


class ProductORM(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name=Column(String)
    quantity=Column(Integer)
    price=Column(Float)

    def __repr__(self):
        return f"Product(id={self.id!r}, name={self.name!r}, quantity={self.quantity!r}, price={self.price!r})"

    @validates('name')
    def validate_empty(self, key, value):
        if not value:
            raise ValueError(f"{key} cannot be empty")
        return value

    @validates('quantity', 'price')
    def validate_positive(self, key, value):
        if value < 0:
            raise ValueError(f"{key} must be positive")
        return value


class OrderORM(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)

    def __repr__(self):
        products_repr = getattr(self, 'products', 'UNDEFINED')
        return f"Product(id={self.id!r}, products={products_repr!r}"


order_product_associations = Table(
    'order_product_associations', Base.metadata,
    Column('order_id', ForeignKey('orders.id')),
    Column('product_id', ForeignKey('products.id'))
)

OrderORM.products = relationship("ProductORM", secondary=order_product_associations)
