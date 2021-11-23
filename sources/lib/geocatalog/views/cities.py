"""
 View для создания городов
"""

from flask import jsonify, request, abort
from flask.views import View

from geocatalog.models import Region, City


class CitiesView(View):

    methods = ['GET', 'POST']

    def dispatch_request(self, region_id):
        region = (
            Region.dm()
            .filter(Region.id == region_id)
            .first()
        )

        if not region:
            return abort(404)

        if request.method == 'POST':
            return self._create_city(region)

        lst = region.list_cities()

        result = []

        if not len(lst):
            lst = region.list_childs_cities()

        for doc in lst:
            result.append(doc.serialize(with_region=True))

        return jsonify(result)

    def _create_city(self, region):
        """Создание города в регионе.
        """

        result = {'success': False}

        content = request.get_json(silent=True)

        if not content:
            return abort(404)

        result = {'success': False}

        if not content.get('name'):
            result['error'] = 'Name not specified'

        if not result.get('error'):
            city = City(name=content.get('name'), region_id=region.id)
            if city.store():
                result['success'] = True
            else:
                result['error'] = 'System error'

        return jsonify(result)
