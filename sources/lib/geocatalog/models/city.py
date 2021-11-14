from sqlalchemy import Column, Integer, String

from geocatalog.models.base import BaseModel

class City(BaseModel):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    region_id = Column(Integer)

    def __init__(self, name, region_id):
        self.name = name
        self.region_id = region_id

    def serialize(self):
        """Сериализация документа в json"""

        return {
            'id': self.id, 
            'name': self.name,
        }
