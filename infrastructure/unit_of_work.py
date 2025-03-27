from domain.unit_of_work import UnitOfWork


class SqlAlchemyUnitOfWork(UnitOfWork):

    def __init__(self, session):
        self.session = session
        self.committed = False

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        if exception_type is None and not self.committed:
            self.commit()
        elif exception_type is not None:
            self.rollback()

    def commit(self):
        self.session.commit()
        self.committed = True

    def rollback(self):
        self.session.rollback()
        self.committed = True
