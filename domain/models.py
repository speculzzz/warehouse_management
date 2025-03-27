from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Product:
    id: Optional[int]
    name: str
    quantity: int
    price: float

    def __post_init__(self):
        if not self.name:
            raise ValueError("Name cannot be empty")
        if self.quantity < 0:
            raise ValueError("Quantity cannot be negative")
        if self.price < 0:
            raise ValueError("Price cannot be negative")


@dataclass
class Order:
    id: Optional[int]
    products: List[Product] = field(default_factory=list)

    def add_product(self, product: Product):
        if not isinstance(product, Product):
            raise TypeError(f"Expected Product, got {type(product).__name__}")
        self.products.append(product)
