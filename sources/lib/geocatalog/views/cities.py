"""
 View для создания городов
"""

from flask import jsonify, request, abort
from flask.views import View

from geocatalog.models.region import Region
from geocatalog.models.city import City


class CitiesView(View):

    methods = ['POST']

    def dispatch_request(self, region_id):
        """Создание города в регионе. 
        """

        region = (
            Region.dm()
            .filter(Region.id == region_id)
            .first()
        )
        
        if not region:
            return abort(404)
        
        result = {'success': 'false'}

        content = request.get_json(silent=True)
        
        if not content:
            return abort(404)
        
        result = {'success': 'false'}
        
        if not content.get('name'):
            result['error'] = 'Name not specified'
        
        if not result.get('error'):
            city = City(name=content.get('name'), region_id=region.id)
            if city.store():
                result['success'] = True
            else:
                result['error'] = 'System error'
                
        return jsonify(result)
            
