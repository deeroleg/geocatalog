from sqlalchemy import Column, ForeignKey, Integer, String

from geocatalog.models.base import BaseModel


class City(BaseModel):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    region_id = Column(Integer, ForeignKey("regions.id"))

    def __init__(self, name, region_id):
        self.name = name
        self.region_id = region_id

    def serialize(self, with_region=False):
        """Сериализация документа в json"""

        res = {
            'id': self.id,
            'name': self.name,
        }

        if with_region:
            res['region_id'] = self.region_id

        return res
