import pytest
from domain.services import WarehouseService
from infrastructure.repositories import SqlAlchemyOrderRepository, SqlAlchemyProductRepository


@pytest.fixture(name='service')
def warehouse_service(session):
    product_repo = SqlAlchemyProductRepository(session)
    order_repo = SqlAlchemyOrderRepository(session)
    service = WarehouseService(product_repo, order_repo)
    return service
