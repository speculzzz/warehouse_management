from typing import List
from .models import Product, Order
from .repositories import ProductRepository, OrderRepository

class WarehouseService:
    def __init__(self, product_repo: ProductRepository, order_repo: OrderRepository):
        self.product_repo=product_repo
        self.order_repo=order_repo

    def create_product(self, name: str, quantity: int, price: float) -> Product:
        product=Product(id=None, name=name, quantity=quantity,price=price)
        self.product_repo.add(product)
        return product

    def create_order(self, products: List[Product]) -> Order:
        order=Order(id=None, products=products)
        self.order_repo.add(order)
        return order

    def product_list(self) -> List[Product]:
        return self.product_repo.list()

    def order_list(self) -> List[Order]:
        return self.order_repo.list()

    def get_product(self, product_id: int) -> Product:
        return self.product_repo.get(product_id)

    def get_order(self, order_id: int) -> Order:
        return self.order_repo.get(order_id)
