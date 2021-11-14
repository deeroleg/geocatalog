"""
 View для отображения дерева регионов и создания регионов
"""

from flask import jsonify, request, abort
from flask.views import View

from geocatalog.models.region import Region


class RegionView(View):

    methods = ['PUT', 'GET', 'DELETE']

    def dispatch_request(self, region_id):
        region = (
            Region.dm()
            .filter(Region.id == region_id)
            .first()
        )
        
        if not region:
            return abort(404)
        
        if request.method == 'PUT':
            return self._update_region(region)
        
        result = {'success': 'false'}
        if request.method == 'DELETE':
            if region.delete():
                result['success'] = True
        else:
            result = region.serialize(full=True)
        
        return jsonify(result)
    
    def _update_region(self, region):
        """Изменение региона из json тела запроса. 
        Подразумевается, что передано название и опционально parent_id, 
        если parent_id не передано, то регион станет регионом верхнего уровня
        Пример {"name": "Рязанская область", "parent_id": 1}
        """
        content = request.get_json(silent=True)
        
        if not content:
            return abort(404)
        
        result = {'success': 'false'}
        
        if not content.get('name'):
            result['error'] = 'Name not specified'
        if content.get('parent_id'):
            parent = (
                Region.dm()
                .filter(Region.id == content.get('parent_id'))
                .first()
            )
            
            if not parent:
                result['error'] = 'Invalid parent region id'
                
        
        if not result.get('error'):
            region.name = content.get('name')
            region.parent_id = content.get('parent_id')
            
            if region.store():
                result['success'] = True
            else:
                result['error'] = 'System error'
                
        return jsonify(result)
            
