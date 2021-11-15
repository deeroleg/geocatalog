"""
 View для редактирования города
"""

from flask import jsonify, request, abort
from flask.views import View

from geocatalog.models.region import Region


class CityView(View):

    methods = ['PUT', 'DELETE']

    def dispatch_request(self, region_id, city_id):
        region = (
            Region.dm()
            .filter(Region.id == region_id)
            .first()
        )
        
        if not region:
            return abort(404)
        
        city = region.get_city_by_id(city_id)

        if not city:
            return abort(404)
        
        if request.method == 'PUT':
            return self._update_city(city)
        
        result = {'success': 'false'}
        if city.delete():
            result['success'] = True
        
        return jsonify(result)
    
    def _update_city(self, city):
        """Изменение города из json тела запроса. 
        Подразумевается, что передано название и опционально region_id, 
        если region_id не передано, то регион не изменится
        Пример {"name": "Рязань", "region_id": 2}
        """
        content = request.get_json(silent=True)
        
        if not content:
            return abort(404)
        
        result = {'success': 'false'}
        
        if not content.get('name'):
            result['error'] = 'Name not specified'
        if content.get('region_id'):
            region = (
                Region.dm()
                .filter(Region.id == content.get('region_id'))
                .first()
            )
            
            if not region:
                result['error'] = 'Invalid parent region id'
                
        
        if not result.get('error'):
            city.name = content.get('name')
            if content.get('region_id'):
                city.region_id = content.get('region_id')
            
            if city.store():
                result['success'] = True
            else:
                result['error'] = 'System error'
                
        return jsonify(result)
            
