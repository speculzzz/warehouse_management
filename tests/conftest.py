import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from infrastructure.orm import Base

TEST_DB_URL = 'sqlite+pysqlite:///:memory:'


@pytest.fixture(scope='module', name='engine')
def db_engine():
    engine = create_engine(TEST_DB_URL, echo=False)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture(scope='function', name='session')
def universal_db_session(engine, request):
    # If @pytest.mark.use_savepoint specified for a test
    use_savepoint = request.node.get_closest_marker('use_savepoint') or getattr(request, 'param', False)

    if use_savepoint:
        # Activate SAVEPOINT mode
        @event.listens_for(engine, "connect")
        def do_connect(dbapi_connection, _connection_record):
            dbapi_connection.isolation_level = None
            dbapi_connection.execute("PRAGMA foreign_keys=ON")

        @event.listens_for(engine, "begin")
        def do_begin(conn):
            conn.exec_driver_sql("BEGIN")

    connection = engine.connect()
    connection.begin()
    session = sessionmaker(bind=connection)()
    yield session
    session.close()
    connection.close()
