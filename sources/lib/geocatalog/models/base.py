from geocatalog import db


class BaseModel(db.Model):

    __abstract__ = True

    @classmethod
    def dm(cls):
        return cls.query

    def store(self):
        db.session.add(self)
        db.session.commit()

        return True

    def delete(self):
        db.session.delete(self)
        db.session.commit()

        return True
