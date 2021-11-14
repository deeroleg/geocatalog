from sqlalchemy.ext.declarative import declarative_base

from geocatalog.service import get_service

Base = declarative_base()

class BaseModel(Base):

    __abstract__ = True

    @classmethod
    def dm(cls):
        return get_service('keeper').get_db_session().query(cls)

    def store(self, modified=[]):
        db_session = get_service('keeper').get_db_session()

        db_session.add(self)
        db_session.commit()

        return True

    def delete(self):
        db_session = get_service('keeper').get_db_session()

        db_session.delete(self)
        db_session.commit()

        return True
