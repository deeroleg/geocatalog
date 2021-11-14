from sqlalchemy import Column, Integer, String

from geocatalog.models.base import BaseModel
from geocatalog.models.city import City

class Region(BaseModel):
    __tablename__ = 'regions'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    parent_id = Column(Integer)

    def __init__(self, name, parent_id):
        self.name = name
        self.parent_id = parent_id
    
    def get_city_by_id(self, city_id):
        """Возвращает город из региона"""
        
        return (
            City.dm()
            .filter(City.id == city_id)
            .filter(City.region_id == self.id)
            .first()
        )
    
    def list_childs(self):
        """Возвращает список дочерних регионов"""
        
        if not hasattr(self, '_childs_'):
            childs = (
                Region.dm()
                .filter(Region.parent_id == self.id)
                .order_by(Region.id.asc())
                .all()
            )
            self._childs_ = childs
            
        return self._childs_
    
    def list_cities(self):
        """Возвращает список городов региона"""
        
        if not hasattr(self, '_cities_'):
            cities = (
                City.dm()
                .filter(City.region_id == self.id)
                .order_by(City.id.asc())
                .all()
            )
            self._cities_ = cities
            
        return self._cities_
    
    def serialize(self, full=False, with_childs=True):
        """Сериализация документа в json"""

        result = {
            'id': self.id, 
            'name': self.name,
        }
        
        if full:
            cities = self.list_cities()
            if len(cities):
                result['cities'] = []
                for doc in cities:
                    result['cities'].append(doc.serialize())
                
        if with_childs:
            childs = self.list_childs()
            if len(childs):
                result['childs'] = []
                for doc in childs:
                    result['childs'].append(doc.serialize(with_childs=False if full else True))
                
        return result
    
    @classmethod
    def get_regions_tree(self):
        """Строит дерево регионов"""
        
        lst = (
            Region.dm()
            .order_by(Region.id.asc())
            .all()
        )
        
        tree = {}

        for doc in lst:
            tree[doc.id] = doc
            doc._childs_ = []

        for doc in lst:
            if doc.parent_id and doc.parent_id in tree:
                tree[doc.parent_id]._childs_.append(doc)
        
        return tree
