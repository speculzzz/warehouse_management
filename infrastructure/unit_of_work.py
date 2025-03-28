from sqlalchemy.exc import SQLAlchemyError
from domain.unit_of_work import UnitOfWork


class SqlAlchemyUnitOfWork(UnitOfWork):

    def __init__(self, session):
        self._session = session
        self._savepoint = []

    def __enter__(self):
        lvl = len(self._savepoint) + 1
        print(f"[BEGIN_NESTED {lvl}]")
        session = self._session.begin_nested()
        self._savepoint.append((lvl, session))
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        print("[EXIT]")
        try:
            if exception_type is None:
                self.commit()
            else:
                self.rollback()
        except SQLAlchemyError as exc:
            raise RuntimeError(f"Transaction failed: {str(exc)}") from exc

    def commit(self):
        if self._savepoint:
            lvl, session = self._savepoint.pop()
            print(f"[COMMIT {lvl}]")
            session.commit()
        else:
            print("[COMMIT]")
            self._session.commit()


    def rollback(self):
        if self._savepoint:
            lvl, session = self._savepoint.pop()
            print(f"[ROLLBACK {lvl}]")
            session.rollback()
        else:
            print("[ROLLBACK]")
            self._session.rollback()
