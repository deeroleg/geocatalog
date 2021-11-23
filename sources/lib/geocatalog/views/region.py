"""
 View для редактирования регионов и просмотра городов региона
"""

from flask import jsonify, request, abort
from flask.views import View
from geocatalog.models import Region


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

        result = {'success': False}
        if request.method == 'DELETE':
            childs = region.list_childs()
            cities = region.list_cities()
            if len(childs) or len(cities):
                result['error'] = 'Region already has cties or childs regions'
            elif region.delete():
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
            else:
                tree = Region.get_regions_tree()
                pid = int(content.get('parent_id'))
                while pid:
                    if pid == region.id:
                        result['error'] = 'Cirdular reference for parent region id'
                        break
                    else:
                        pid = tree.get(pid).parent_id if tree.get(pid) else None

        if not result.get('error'):
            region.name = content.get('name')
            region.parent_id = content.get('parent_id')

            if region.store():
                result['success'] = True
            else:
                result['error'] = 'System error'

        return jsonify(result)
