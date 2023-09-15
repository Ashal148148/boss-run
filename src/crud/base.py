from sqlalchemy.orm import Session

class CRUDBase:
    def read(self, session: Session):
        pass

    def read_many(self, session: Session):
        pass

    def update(self, session: Session):
        pass

    def create(self, session: Session):
        pass

    def delete(self, session: Session):
        pass
