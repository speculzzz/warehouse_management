from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import sessionmaker

from domain.services import WarehouseService
from infrastructure.orm import Base
from infrastructure.repositories import SqlAlchemyProductRepository, SqlAlchemyOrderRepository
from infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from infrastructure.database import DATABASE_URL


# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
SessionFactory=sessionmaker(bind=engine)

# Activate SAVEPOINT mode
@event.listens_for(engine, "connect")
def do_connect(dbapi_connection, _connection_record):
    dbapi_connection.isolation_level = None
    dbapi_connection.execute("PRAGMA foreign_keys=ON")

@event.listens_for(engine, "begin")
def do_begin(conn):
    conn.exec_driver_sql("BEGIN")

session = SessionFactory()
product_repo = SqlAlchemyProductRepository(session)
order_repo = SqlAlchemyOrderRepository(session)
warehouse_service = WarehouseService(product_repo, order_repo)
worker = SqlAlchemyUnitOfWork(session)


def show_products():
    print("\n=== Product List ===")
    products = warehouse_service.product_list()
    if len(products) == 0:
        print("*** Empty ***")
        return

    print(f"{'ID':>4} | {'Name':<15} | {'Quantity':<8} | {'Price':<6}")
    print("-" * 42)
    for product in products:
        print(f"{product.id:4} | {product.name:15} | {product.quantity:8} | {product.price:6.2f}")


def show_orders():
    print("\n=== Order History ===")
    orders = warehouse_service.order_list()
    if len(orders) == 0:
        print("*** Empty ***")
        return

    for order in orders:
        print(f"\nOrder #{order.id}:")
        for product in order.products:
            print(f"  - {product.name} (ID: {product.id}) - ${product.price*product.quantity:.2f}")


def add_product():
    print("\n=== Add New Product ===")
    name = input("Product name: ")
    quantity = int(input("Quantity: "))
    price = float(input("Price: "))

    try:
        with worker:
            warehouse_service.create_product(name=name, quantity=quantity, price=price)
            print("✅ Product added successfully!")

        session.commit()
    except Exception as exc:
        print(f"🔴 Error adding product: {exc}")


def clear_database():
    confirmation = input("Are you sure you want to clear ALL data? (yes/no): ").lower()
    if confirmation == 'yes':
        try:
            # Disable foreign keys for SQLite
            if engine.dialect.name == 'sqlite':
                session.execute(text("PRAGMA foreign_keys=OFF"))

            # Clear all tables
            for table in reversed(Base.metadata.sorted_tables):
                session.execute(table.delete())

            # Re-enable foreign keys
            if engine.dialect.name == 'sqlite':
                session.execute(text("PRAGMA foreign_keys=ON"))

            session.commit()
            print("✅ Database cleared successfully!")
        except Exception as exc:
            print(f"🔴 Error clearing database: {exc}")
    else:
        print("Operation cancelled")


def create_order():
    show_products()
    product_ids = input("\nEnter product IDs (comma separated): ").split(',')

    try:
        with worker:
            products = []
            for pid in product_ids:
                product = warehouse_service.get_product(int(pid))
                products.append(product)

            warehouse_service.create_order(products)
            print("✅ Order created successfully!")

        session.commit()
    except Exception as exc:
        print(f"🔴 Error creating order: {exc}")


def main_menu():
    while True:
        print("\n=== Warehouse Management ===")
        print("1. Show products")
        print("2. Add product")
        print("3. Create order")
        print("4. Show orders")
        print("5. Clear database")
        print("6. Exit")

        choice = input("> ")

        if choice == "1":
            show_products()
        elif choice == "2":
            add_product()
        elif choice == "3":
            create_order()
        elif choice == "4":
            show_orders()
        elif choice == "5":
            clear_database()
        elif choice == "6":
            session.close()
            break
        else:
            print("Invalid input!")


def main():
    print("[BEGIN]")
    session.begin()

    main_menu()

    session.close()
    print("[END]")


if __name__ == "__main__":
    main()
