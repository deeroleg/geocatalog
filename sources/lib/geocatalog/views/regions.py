"""
 View для отображения дерева регионов и создания регионов
"""

from flask import jsonify, request, abort
from flask.views import View

from geocatalog.models.region import Region


class RegionsView(View):

    methods = ['POST', 'GET']

    def dispatch_request(self):
        if request.method == 'POST':
            return self._create_region()
        
        tree = Region.get_regions_tree()
        
        result = []
        
        for id, doc in tree.items():
            if not doc.parent_id:
                result.append(doc.serialize())

        return jsonify(result)
    
    def _create_region(self):
        """Создание региона из json тела запроса. 
        Подразумевается, что передано название и опционально parent_id
        Пример {'name': 'Рязанская область'}
        """

        content = request.get_json(silent=True)
        
        if not content:
            return abort(404)
        
        result = {'success': False}
        
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
            region = Region(name=content.get('name'), parent_id=content.get('parent_id'))
            if region.store():
                result['success'] = True
            else:
                result['error'] = 'System error'
                
        return jsonify(result)
            
